import os
import time
import cv2
import logging
from threading import Timer

ENABLE_DUMP = os.getenv("ENABLE_DUMP",True)
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 1))
EQUIPMENT = os.getenv('EQUIPMENT', 'espumamento')
INTERVAL = int(os.getenv('INTERVAL', 300))

def list_resolutions(camera_index=1):
    cap = cv2.VideoCapture(camera_index)
    resolutions = set()
    for width in range(640, 3840, 160):
        for height in range(480, 2160, 120):
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            resolutions.add((actual_width, actual_height))
    cap.release()
    return sorted(resolutions)

print(list_resolutions(CAMERA_INDEX))
