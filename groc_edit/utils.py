import cv2
import dlib
import numpy as np
import os

def detect_face(image):
    if image.dtype != np.uint8:
        raise ValueError("Image must be 8-bit")
    
    if len(image.shape) == 2:
        pass
    elif len(image.shape) == 3 and image.shape[2] == 3:
        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("Image must be grayscale or RGB")
    
    detector = dlib.get_frontal_face_detector()
    faces = detector(image, 1)
    if len(faces) > 0:
        return faces[0]
    return None

def crop_and_resize(image, face, target_size=(300, 400)):
    face_height = face.bottom() - face.top()
    face_width = face.right() - face.left()
    
    scale = min(target_size[0] / (face_width * 4.1), target_size[1] / (face_height * 4.1))
    
    new_height = int(image.shape[0] * scale)
    new_width = int(image.shape[1] * scale)
    
    resized = cv2.resize(image, (new_width, new_height))
    
    face_center_x = int((face.left() + face.right()) / 2 * scale)
    face_center_y = int((face.top() + face.bottom()) / 2 * scale)
    
    left = max(face_center_x - target_size[0] // 2, 0)
    top = max(face_center_y - target_size[1] // 3, 0)
    right = min(left + target_size[0], new_width)
    bottom = min(top + target_size[1], new_height)
    
    cropped = resized[top:bottom, left:right]
    
    final = cv2.resize(cropped, target_size)
    
    return final

def get_filename_without_extension(filename):
    head, tail = os.path.split(filename)
    base, ext = os.path.splitext(tail)
    return base