import pickle

import cv2
import face_recognition
import numpy as np

THRESHOLD = 0.5


def _largest_location(locations):
    def area(loc):
        top, right, bottom, left = loc
        return (right - left) * (bottom - top)
    return max(locations, key=area)


def extract_embedding(frame_bgr):
    if frame_bgr is None:
        return None
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb, model="hog")
    if not locations:
        return None
    encodings = face_recognition.face_encodings(rgb, [_largest_location(locations)])
    return encodings[0] if encodings else None


def serialize_embedding(embedding):
    return pickle.dumps(np.asarray(embedding, dtype=np.float64), protocol=4)


def deserialize_embedding(blob):
    return np.asarray(pickle.loads(blob), dtype=np.float64)


def register_face(frame_bgr):
    embedding = extract_embedding(frame_bgr)
    if embedding is None:
        raise ValueError("Wajah tidak terdeteksi")
    return serialize_embedding(embedding)


def verify_face(frame_bgr, known_embedding, threshold=THRESHOLD):
    unknown = extract_embedding(frame_bgr)
    if unknown is None:
        return False, None
    distance = float(face_recognition.face_distance([known_embedding], unknown)[0])
    return distance <= threshold, distance


def identify_face(frame_bgr, candidates, threshold=THRESHOLD):
    unknown = extract_embedding(frame_bgr)
    if unknown is None or not candidates:
        return None
    ids = [c[0] for c in candidates]
    encodings = [c[1] for c in candidates]
    distances = face_recognition.face_distance(encodings, unknown)
    idx = int(np.argmin(distances))
    distance = float(distances[idx])
    if distance > threshold:
        return None
    return {"id_siswa": ids[idx], "distance": distance}
