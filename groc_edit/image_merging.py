import os
import numpy as np
from PIL import Image

# 배경 합성
def merge_with_background(foreground_path, output_folder):
    background = Image.open("assets/profile_bg.png").convert("RGBA")
    foreground = Image.open(foreground_path).convert("RGBA")
    foreground = foreground.resize(background.size, Image.LANCZOS)

    bg_array = np.array(background)
    fg_array = np.array(foreground)

    bg_alpha = bg_array[:, :, 3]
    fg_alpha = fg_array[:, :, 3]

    result = np.zeros_like(bg_array)

    # 배경의 오른쪽 사선 이내에만 전경 이미지가 들어오도록 283 픽셀 이상의 y좌표(테두리 상단)에서는 가장 오른쪽 불투명 픽셀(테두리)까지만 전경을 복사한다.
    for y in range(bg_array.shape[0]):
        rightmost_opaque = 713
        if y > 283:
            for x in range(bg_array.shape[1] - 1, -1, -1):
                if bg_alpha[y, x] > 0:
                    rightmost_opaque = x
                    break

        result[y, :] = bg_array[y, :]

        mask = (fg_alpha[y, :] > 0) & (np.arange(bg_array.shape[1]) <= rightmost_opaque)
        result[y, :rightmost_opaque-2][mask[:rightmost_opaque-2]] = fg_array[y, :rightmost_opaque-2][mask[:rightmost_opaque-2]]

    combined = Image.fromarray(result)
    output_path = os.path.join(output_folder, "step3_merge_bg", f"merged_{os.path.basename(foreground_path)}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.save(output_path)
    print(f"\t[STEP 3] Merged: {output_path}")
