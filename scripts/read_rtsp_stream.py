import cv2
import threading
from time import sleep
import os

# === RTSP stream URL ===
rtsp_url = 'rtsp://admin:Olfk$1234@192.168.40.206/22'

# === Threaded Video Capture Class ===
class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        self.ret, self.frame = self.cap.read()
        self.stopped = False
        self.lock = threading.Lock()

        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while not self.stopped:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                with self.lock:
                    self.ret, self.frame = ret, frame

    def read(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else (False, None)

    def stop(self):
        self.stopped = True
        self.cap.release()

# === Start Video Stream ===
stream = VideoStream(rtsp_url)
sleep(1)  # Let the stream warm up

# === Main Loop ===
while True:
    ret, frame = stream.read()
    if not ret or frame is None:
        sleep(0.1)
        continue

    # Resize and predict
    frame = cv2.resize(frame, (640, 480))
    cv2.imshow('YOLO V8 Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
stream.stop()
cv2.destroyAllWindows()
