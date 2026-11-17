import queue
import re
import threading
import time

import serial

UID_RE = re.compile(r"^[0-9A-Fa-f]{8,14}$")


class SerialListener(threading.Thread):
    def __init__(self, port, baudrate=115200, uid_queue=None, on_uid=None, debounce_seconds=3.0):
        super().__init__(daemon=True, name="serial-listener")
        self.port = port
        self.baudrate = baudrate
        self.uid_queue = uid_queue or queue.Queue()
        self.on_uid = on_uid
        self.debounce_seconds = debounce_seconds
        self._stop = threading.Event()
        self._last_seen = {}
        self.ser = None

    def run(self):
        while not self._stop.is_set():
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
                while not self._stop.is_set():
                    try:
                        line = self.ser.readline()
                    except serial.SerialException:
                        break
                    if not line:
                        continue
                    uid = line.decode("utf-8", errors="ignore").strip().upper()
                    if not UID_RE.match(uid):
                        continue
                    now = time.monotonic()
                    if now - self._last_seen.get(uid, 0.0) < self.debounce_seconds:
                        continue
                    self._last_seen[uid] = now
                    self.uid_queue.put(uid)
                    if self.on_uid:
                        self.on_uid(uid)
            except (serial.SerialException, OSError):
                time.sleep(2)
            finally:
                if self.ser is not None:
                    try:
                        self.ser.close()
                    except Exception:
                        pass
                    self.ser = None

    def stop(self):
        self._stop.set()
