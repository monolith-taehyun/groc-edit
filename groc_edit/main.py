import cv2
import os
from rembg import remove
from PIL import Image
import numpy as np
from utils import detect_face, crop_and_resize, get_filename_without_extension

def process_images(input_folder, output_folder, target_size=(300, 400), remove_bg=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Start Processing: {filename}")
            
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Failed to load image: {filename}")
                continue
            
            face = detect_face(image)
            
            if face is None:
                print(f"No face detected in: {filename}")
                continue
            
            print(f"Face detected in: {filename}")
            
            processed = crop_and_resize(image, face, target_size)

            output_path = os.path.join(output_folder, "step1_resize_crop", f"resized_{filename}")
            cv2.imwrite(output_path, processed)
            print(f"End Processed: {filename} -> {output_path}")
            
            if remove_bg:
                print(f"Removing background from: {filename}")
                pil_image = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
                
                output = remove(pil_image)
                
                processed = cv2.cvtColor(np.array(output), cv2.COLOR_RGBA2BGRA)

                filenameonly = get_filename_without_extension(filename)
            
                output_path = os.path.join(output_folder, "step2_remove_bg", f"transparent_{filenameonly}.png")
                cv2.imwrite(output_path, processed)
                print(f"End Processed: {filename} -> {output_path}")

if __name__ == "__main__":
    input_folder = "input_images"
    output_folder = "output_images"
    process_images(input_folder, output_folder, remove_bg=True)