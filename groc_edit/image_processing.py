import cv2
from utils import detect_face, crop_and_resize

# 이미치 처리: 리사이즈, 크롭
def process_image(image_path, target_size=(713, 673)):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None, False

    # 얼굴 조회
    face = detect_face(image)
    if face is None:
        return None, False

    print(f"\tFace detected in: {image_path}")
    processed = crop_and_resize(image, face, target_size)
    return processed, True
