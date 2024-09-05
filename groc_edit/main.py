import cv2
import dlib
import os
from utils import detect_face, crop_and_resize

def process_images(input_folder, output_folder, target_size=(300, 400)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        print(f"Processing: {filename}")
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Failed to load image: {filename}")
                continue
            
            face = detect_face(image)
            
            if face is None:
                print(f"No face detected in: {filename}")
                continue
            
            processed = crop_and_resize(image, face, target_size)
            
            output_path = os.path.join(output_folder, f"processed_{filename}")
            cv2.imwrite(output_path, processed)
            print(f"Processed: {filename} -> {output_path}")

if __name__ == "__main__":
    input_folder = "input_images"
    output_folder = "output_images"
    process_images(input_folder, output_folder)