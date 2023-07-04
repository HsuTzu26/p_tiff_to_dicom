import os

# The path can also be read from a config file, etc.
OPENSLIDE_PATH = r'D:\Programming\python\tiff-to-dicom\openslide-win64-20230414\openslide-win64-20230414\bin'

import os
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        from openslide import OpenSlide
else:
    from openslide import OpenSlide
from PIL import Image


"""
在本次處理的檔案中，只有第一個圖層為整個主要的部份，剩下的部分為放大後的部分。
請注意，圖層編號從 1 開始，因此如果要輸出的是第一個圖層，則 target_layer 應該設為 1。
如果你省略 target_layer 參數，則會輸出所有圖層的區域圖像。
"""
def split_tiff_layers_to_jpg_files(input_file, output_folder, target_layer=None):
    # 建立輸出資料夾
    os.makedirs(output_folder, exist_ok=True)

    # 開啟TIFF圖像
    slide = OpenSlide(input_file)

    # 獲取圖層數量
    num_layers = slide.level_count

    # 確定目標圖層的範圍
    if target_layer is not None:
        if target_layer < 1 or target_layer > num_layers:
            print("錯誤：指定的目標圖層超出範圍。")
            slide.close()
            return

        start_layer = target_layer - 1
        end_layer = target_layer
    else:
        start_layer = 0
        end_layer = num_layers

    # 逐層寫入JPG檔案
    for i in range(start_layer, end_layer):
        # 獲取圖層大小
        width, height = slide.level_dimensions[i]

        # 計算分割區域的大小（將圖層大小除以10）
        region_width = width // 10
        region_height = height // 10

        # 計算分割區域的數量
        num_regions_x = (width + region_width - 1) // region_width
        num_regions_y = (height + region_height - 1) // region_height

        # 逐區域寫入JPG檔案
        for y in range(num_regions_y):
            for x in range(num_regions_x):
                # 計算區域的左上角座標
                region_x = x * region_width
                region_y = y * region_height

                # 計算區域的寬度和高度（最後一個區域可能不到設定的大小）
                region_w = min(region_width, width - region_x)
                region_h = min(region_height, height - region_y)

                # 讀取區域
                region = slide.read_region((region_x, region_y), i, (region_w, region_h))

                # 轉換為 RGB 模式
                region = region.convert("RGB")

                # 構建檔案路徑
                filename = f"{output_folder}/圖層{i + 1}_區域{y}_{x}.jpg"

                # 寫入JPG檔案
                region.save(filename, "JPEG")

                print(f"已寫入檔案：{filename}")

    # 關閉圖像
    slide.close()


split_tiff_layers_to_jpg_files("input.tiff", "output", target_layer=1)