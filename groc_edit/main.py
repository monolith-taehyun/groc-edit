import os
import cv2
from utils import get_filename_without_extension
from image_processing import process_image
from background_remove import remove_background
from image_merging import merge_with_background

def process_images(input_folder, output_folder, target_size=(713, 673), remove_bg=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Start Processing: {filename}")

            image_path = os.path.join(input_folder, filename)

            # 이미지 리사이즈, 크롭
            processed, face_detected = process_image(image_path, target_size)

            if not face_detected:
                print(f"No face detected in: {filename}")
                continue

            output_path = os.path.join(output_folder, "step1_resize_crop", f"resized_{filename}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, processed)
            print(f"\t[STEP 1] Resize and Cropped: {filename} -> {output_path}")

            # 배경 제거
            if remove_bg:
                filenameonly = get_filename_without_extension(filename)
                bg_removed_output_path = os.path.join(output_folder, "step2_remove_bg", f"transparent_{filenameonly}.png")
                os.makedirs(os.path.dirname(bg_removed_output_path), exist_ok=True)

                processed = remove_background(processed)
                cv2.imwrite(bg_removed_output_path, processed)
                print(f"\t[STEP 2] Removed BG: {filename} -> {bg_removed_output_path}")

                # 프로필 이미지 제작을 위한 배경 합성
                merge_with_background(bg_removed_output_path, output_folder)

if __name__ == "__main__":
    input_folder = "input_images"
    output_folder = "output_images"
    process_images(input_folder, output_folder, remove_bg=True)
