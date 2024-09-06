# background_removal.py
from rembg import remove
from PIL import Image
import cv2
import numpy as np

def remove_background(processed_image):
    pil_image = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
    output = remove(pil_image)
    processed = cv2.cvtColor(np.array(output), cv2.COLOR_RGBA2BGRA)
    return processed
