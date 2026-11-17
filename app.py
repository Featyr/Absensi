import json
import os
import queue
import re
import threading
import time
from datetime import datetime
from functools import wraps

import cv2
from flask import Flask, Response, jsonify, redirect, render_template, request, session, url_for

import database as db
from face_engine import THRESHOLD, deserialize_embedding, identify_face, register_face, verify_face
from serial_listener import SerialListener

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ganti-secret-key-ini")
SERIAL_PORT = os.environ.get("SERIAL_PORT", "COM3" if os.name == "nt" else "/dev/ttyUSB0")
# Simulation path for the prototype without an RC522 module: a UID typed in
# the dashboard is put into the same queue the serial listener uses, so it
# goes through exactly the same process_uid() logic as a real tap.
UID_RE = re.compile(r"^[0-9A-F]{8,14}$")

camera_lock = threading.Lock()


class Camera:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def read_frame(self):
        with camera_lock:
            ok, frame = self.cap.read()
        return cv2.flip(frame, 1) if ok else None

    def jpeg_bytes(self):
        frame = self.read_frame()
        if frame is None:
            return None
        ok, buf = cv2.imencode(".jpg", frame)
        return buf.tobytes() if ok else None


camera = Camera()
uid_queue = queue.Queue()
listener = SerialListener(SERIAL_PORT, uid_queue=uid_queue)

state_lock = threading.Lock()
rfid_state = {"version": 0, "uid": None, "status": "idle", "siswa": None,
              "message": "Tempelkan kartu RFID", "distance": None, "timestamp": None}
pending_lock = threading.Lock()
pending_candidate = None


def update_rfid_state(status, uid=None, siswa=None, message="", distance=None):
    with state_lock:
        rfid_state.update({"version": rfid_state["version"] + 1, "uid": uid,
                           "status": status, "siswa": siswa, "message": message,
                           "distance": distance, "timestamp": datetime.now().isoformat(timespec="seconds")})


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "petugas_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def get_payload():
    """Terima JSON maupun form-encoded.

    Di PowerShell, JSON lewat curl.exe sering rusak karena tanda kutip
    dan spasi, sehingga get_json() mengembalikan {}. Form-encoded
    (curl -d "nis=001&nama_lengkap=...") tidak punya masalah itu.
    """
    data = request.get_json(silent=True)
    if isinstance(data, dict) and data:
        return data
    if request.form:
        return request.form.to_dict()
    try:
        raw = request.get_data(as_text=True) or ""
        parsed = json.loads(raw) if raw.strip() else {}
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return {}


def process_uid(uid):
    siswa = db.get_siswa_by_uid(uid)
    if siswa is None:
        update_rfid_state("error", uid=uid, message="Kartu tidak dikenal / tidak aktif")
        return
    if db.sudah_absen(siswa["id_siswa"]):
        update_rfid_state("duplicate", uid=uid, siswa=siswa, message="Siswa sudah absen hari ini")
        return
    blob = db.get_face_template_by_siswa(siswa["id_siswa"])
    if blob is None:
        update_rfid_state("error", uid=uid, siswa=siswa, message="Template wajah belum terdaftar")
        return
    frame = camera.read_frame()
    if frame is None:
        update_rfid_state("error", uid=uid, siswa=siswa, message="Webcam tidak tersedia")
        return
    matched, distance = verify_face(frame, deserialize_embedding(blob), THRESHOLD)
    if not matched:
        update_rfid_state("mismatch", uid=uid, siswa=siswa,
                          message="Wajah tidak cocok dengan pemilik kartu", distance=distance)
        return
    absen_id = db.catat_absensi(siswa["id_siswa"], "RFID")
    if absen_id is None:
        update_rfid_state("duplicate", uid=uid, siswa=siswa, message="Siswa sudah absen hari ini")
        return
    update_rfid_state("success", uid=uid, siswa=siswa,
                      message=f"Absensi tercatat: {siswa['nama_lengkap']}", distance=distance)


def rfid_worker():
    while True:
        process_uid(uid_queue.get())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        admin = db.verify_admin(request.form.get("username", ""), request.form.get("password", ""))
        if admin:
            session["petugas_id"] = admin["id_petugas"]
            session["nama_petugas"] = admin["nama_petugas"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Username / password salah"), 401
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", nama_petugas=session.get("nama_petugas"))


def gen_frames():
    while True:
        data = camera.jpeg_bytes()
        if data is None:
            time.sleep(0.1)
            continue
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + data + b"\r\n"
        time.sleep(0.03)


@app.route("/video_feed")
@login_required
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/api/rfid_status")
@login_required
def rfid_status():
    def generate():
        last_version = -1
        while True:
            with state_lock:
                snapshot, version = dict(rfid_state), rfid_state["version"]
            if version != last_version:
                last_version = version
                yield f"data: {json.dumps(snapshot)}\n\n"
            else:
                yield ": heartbeat\n\n"
            time.sleep(0.5)
    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/api/simulate_tap", methods=["POST"])
@login_required
def simulate_tap():
    data = get_payload()
    uid = str(data.get("uid_kartu") or data.get("uid") or "").strip().upper()
    if not UID_RE.match(uid):
        return jsonify({"status": "error", "message": "UID tidak valid, pakai 8-14 karakter heksadesimal, contoh A1B2C3D4"}), 400
    uid_queue.put(uid)
    return jsonify({"status": "queued", "uid": uid})


@app.route("/api/manual_scan", methods=["POST"])
@login_required
def manual_scan():
    global pending_candidate
    frame = camera.read_frame()
    if frame is None:
        return jsonify({"status": "error", "message": "Webcam tidak tersedia"}), 503
    candidates = [(sid, deserialize_embedding(blob)) for sid, blob in db.get_all_face_templates()]
    result = identify_face(frame, candidates, THRESHOLD)
    if result is None:
        return jsonify({"status": "not_found", "message": "Wajah tidak dikenali"}), 404
    siswa = db.get_siswa_by_id(result["id_siswa"])
    with pending_lock:
        pending_candidate = {"id_siswa": siswa["id_siswa"], "distance": result["distance"]}
    return jsonify({"status": "found", "candidate": siswa, "distance": result["distance"]})


@app.route("/api/confirm_alternative", methods=["POST"])
@login_required
def confirm_alternative():
    global pending_candidate
    data = get_payload()
    try:
        id_siswa = int(data.get("id_siswa"))
    except (TypeError, ValueError):
        id_siswa = data.get("id_siswa")
    with pending_lock:
        candidate = pending_candidate
        pending_candidate = None
    if candidate is None or candidate["id_siswa"] != id_siswa:
        return jsonify({"status": "error", "message": "Konfirmasi kedaluwarsa, scan ulang"}), 409
    if db.sudah_absen(id_siswa):
        return jsonify({"status": "duplicate", "message": "Siswa sudah absen hari ini"}), 409
    absen_id = db.catat_absensi(id_siswa, "Alternatif", id_petugas=session["petugas_id"])
    if absen_id is None:
        return jsonify({"status": "duplicate", "message": "Siswa sudah absen hari ini"}), 409
    return jsonify({"status": "success", "id_absensi": absen_id})


@app.route("/api/absensi_today")
@login_required
def absensi_today():
    return jsonify(db.get_absensi_hari_ini())


@app.route("/api/siswa")
@login_required
def api_siswa():
    return jsonify(db.list_siswa())


@app.route("/api/siswa", methods=["POST"])
@login_required
def api_add_siswa():
    data = get_payload()
    if not data.get("nis") or not data.get("nama_lengkap") or not data.get("kelas"):
        return jsonify({"status": "error", "message": f"Field tidak lengkap, data yang diterima: {data}"}), 400
    try:
        sid = db.add_siswa(data["nis"], data["nama_lengkap"], data["kelas"])
    except Exception as e:
        # Jangan sembunyikan penyebab aslinya: sebelumnya semua error
        # dilabeli "NIS sudah terdaftar", padahal bisa jadi error lain.
        print(f"api_add_siswa error: {type(e).__name__}: {e}", flush=True)
        if "UNIQUE" in str(e).upper():
            return jsonify({"status": "error", "message": "NIS sudah terdaftar"}), 409
        return jsonify({"status": "error", "message": f"Gagal tambah siswa: {type(e).__name__}: {e}"}), 500
    return jsonify({"status": "success", "id_siswa": sid}), 201


@app.route("/api/register_face", methods=["POST"])
@login_required
def api_register_face():
    data = get_payload()
    frame = camera.read_frame()
    if frame is None:
        return jsonify({"status": "error", "message": "Webcam tidak tersedia"}), 503
    try:
        blob = register_face(frame)
    except ValueError:
        return jsonify({"status": "error", "message": "Wajah tidak terdeteksi"}), 422
    db.save_face_template(data["id_siswa"], blob)
    return jsonify({"status": "success"})


@app.route("/api/assign_card", methods=["POST"])
@login_required
def api_assign_card():
    data = get_payload()
    try:
        kid = db.add_kartu(data["id_siswa"], data["uid_kartu"].strip().upper())
    except Exception as e:
        print(f"api_assign_card error: {type(e).__name__}: {e}", flush=True)
        if "UNIQUE" in str(e).upper():
            return jsonify({"status": "error", "message": "UID sudah terdaftar"}), 409
        return jsonify({"status": "error", "message": f"Gagal assign kartu: {type(e).__name__}: {e}"}), 500
    return jsonify({"status": "success", "id_kartu": kid}), 201


if __name__ == "__main__":
    db.init_db()
    if db.count_admin() == 0:
        db.create_admin("Petugas", os.environ.get("ADMIN_USERNAME", "petugas"),
                        os.environ.get("ADMIN_PASSWORD", "admin123"), role="admin")
    listener.start()
    threading.Thread(target=rfid_worker, daemon=True, name="rfid-worker").start()
    app.run(host="127.0.0.1", port=5000, threaded=True)
