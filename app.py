import os
import time
import cv2
import logging
from threading import Timer

ENABLE_DUMP = os.getenv("ENABLE_DUMP", True)
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))
EQUIPMENT = os.getenv('EQUIPMENT', 'espumamento')
INTERVAL = int(os.getenv('INTERVAL', 300))
CODEC = os.getenv('CODEC', 'MJPG')  # Default to MJPG, can set to 'H264' via environment

# Define a custom logging level
IMPORTANT = 25
logging.addLevelName(IMPORTANT, "IMPORTANT")

def important(self, message, *args, **kws):
    if self.isEnabledFor(IMPORTANT):
        self._log(IMPORTANT, message, args, **kws)

# Add the custom level to the Logger class
logging.Logger.important = important

# Set up logging to use the custom level
logging.basicConfig(level=IMPORTANT, format='%(asctime)s - %(levelname)s - %(message)s')

# Base directory to save images
BASE_IMAGE_SAVE_PATH = './data'

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def initialize_camera(camera_index=0):
    # Set the codec based on environment variable
    fourcc = cv2.VideoWriter_fourcc(*CODEC)
    cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    if not cap.isOpened():
        logging.error(f"Failed to open video device {camera_index} with codec {CODEC}.")
        return None
    return cap

def take_picture(cap):
    if ENABLE_DUMP:
        for _ in range(10):
            cap.read()

    directory_path = os.path.join(BASE_IMAGE_SAVE_PATH, EQUIPMENT)
    ensure_directory(directory_path)

    ret, frame = cap.read()
    if ret:
        timestamp = time.strftime("%d.%m.%Y_%H.%M.%S")
        image_path = os.path.join(directory_path, f'{timestamp}.png')
        try:
            cv2.imwrite(image_path, frame)
            logging.getLogger().important(f"Image successfully saved: {image_path}")
        except Exception as e:
            logging.getLogger().important(f"Failed to save image: {e}")
    else:
        logging.getLogger().important("Failed to capture image")

def continuous_capture():
    cap = initialize_camera(CAMERA_INDEX)
    if cap:
        try:
            while True:
                take_picture(cap)
                time.sleep(INTERVAL)
        finally:
            cap.release()
    else:
        logging.error("Camera initialization failed. Exiting application.")

if __name__ == '__main__':
    continuous_capture()