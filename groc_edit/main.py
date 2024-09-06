import cv2
import os
from rembg import remove
from PIL import Image
import numpy as np
from utils import detect_face, crop_and_resize, get_filename_without_extension

def process_images(input_folder, output_folder, target_size=(713, 673), remove_bg=True):
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
            
            print(f"\tFace detected in: {filename}")
            
            processed = crop_and_resize(image, face, target_size)

            output_path = os.path.join(output_folder, "step1_resize_crop", f"resized_{filename}")
            cv2.imwrite(output_path, processed)
            print(f"\t[STEP 1] Resize and Croped: {filename} -> {output_path}")
            
            if remove_bg:
                pil_image = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
                
                output = remove(pil_image)
                
                processed = cv2.cvtColor(np.array(output), cv2.COLOR_RGBA2BGRA)

                filenameonly = get_filename_without_extension(filename)
            
                output_path = os.path.join(output_folder, "step2_remove_bg", f"transparent_{filenameonly}.png")
                cv2.imwrite(output_path, processed)
                print(f"\t[STEP 2] Removed BG: {filename} -> {output_path}")

                # 배경과 합치기
                merge_with_background(output_path, output_folder)

def merge_with_background(foreground_path, output_folder):
    # 배경 이미지 로드
    background = Image.open("assets/profile_bg.png").convert("RGBA")
    
    # 전경 이미지 로드
    foreground = Image.open(foreground_path).convert("RGBA")
    
    # 배경 이미지 크기에 맞게 전경 이미지 리사이즈
    foreground = foreground.resize(background.size, Image.LANCZOS)
    
    # 이미지를 numpy 배열로 변환
    bg_array = np.array(background)
    fg_array = np.array(foreground)
    
    # 알파 채널 추출
    bg_alpha = bg_array[:, :, 3]
    fg_alpha = fg_array[:, :, 3]
    
    # 결과 이미지 초기화
    result = np.zeros_like(bg_array)
    
    # 각 행마다 처리
    for y in range(bg_array.shape[0]):
        rightmost_opaque = 713
        if y > 283:
            # 현재 행에서 가장 오른쪽 불투명 픽셀의 x 좌표 찾기
            for x in range(bg_array.shape[1] - 1, -1, -1):
                if bg_alpha[y, x] > 0:
                    rightmost_opaque = x
                    break
            
        # 배경 이미지 복사
        result[y, :] = bg_array[y, :]


        # print(f"Processing y: {y}, x: {rightmost_opaque}")
        
        # 전경 이미지의 왼쪽 부분만 복사 (배경의 가장 오른쪽 불투명 픽셀까지)
        mask = (fg_alpha[y, :] > 0) & (np.arange(bg_array.shape[1]) <= rightmost_opaque)
        result[y, :rightmost_opaque-2][mask[:rightmost_opaque-2]] = fg_array[y, :rightmost_opaque-2][mask[:rightmost_opaque-2]]

    # 결과를 PIL Image로 변환
    combined = Image.fromarray(result)
    
    # 결과 저장
    output_path = os.path.join(output_folder, "step3_merge_bg", f"merged_{os.path.basename(foreground_path)}")
    combined.save(output_path)
    print(f"\t[STEP 3]Merged: {output_path}")


if __name__ == "__main__":
    input_folder = "input_images"
    output_folder = "output_images"
    process_images(input_folder, output_folder, remove_bg=True)