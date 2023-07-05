OPENSLIDE_PATH = r'D:\Programming\python\p_tiff_to_dicom\openslide-win64-20230414\openslide-win64-20230414\bin'

import os
from PIL import Image
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        from openslide import OpenSlide
else:
    from openslide import OpenSlide


def split_tiff_layers_to_jpg_files(input_file, output_folder, target_layer=None, scale_ratio=0.1, image_width=10000, image_height=10000):
    """
    在本次處理的檔案中，只有第一個圖層為整個主要的部份，剩下的部分為放大後的部分。
    請注意，圖層編號從 1 開始，因此如果要輸出的是第一個圖層，則 target_layer 應該設為 1。
    如果你省略 target_layer 參數，則會輸出所有圖層的區域圖像。

    :param input_file: 輸入的TIFF檔案名稱
    :param output_folder: 輸出的資料夾
    :param target_layer: 目標圖層編號，預設為 None，表示輸出所有圖層
    :param image_width: 圖片寬度，預設為 1000
    :param image_height: 圖片高度，預設為 1000
    """

    # 建立輸出資料夾
    os.makedirs(output_folder, exist_ok=True)

    # 刪除輸出資料夾底下的所有檔案
    file_list = os.listdir(output_folder)
    for file_name in file_list:
        file_path = os.path.join(output_folder, file_name)
        os.remove(file_path)

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

        # 計算水平和垂直方向上的切割數量
        num_regions_x = max((width + image_width - 1) // image_width, 1)
        num_regions_y = max((height + image_height - 1) // image_height, 1)
        num_regions = max(num_regions_x,num_regions_y)

        # 逐區域寫入JPG檔案
        for y in range(num_regions):
            for x in range(num_regions):
                # 計算區域的左上角座標
                region_x = x * image_width
                region_y = y * image_height

                # 計算區域的寬度和高度（最後一個區域可能不到設定的大小）
                region_w = image_width
                region_h = image_height

                # 讀取區域
                region = slide.read_region((region_x, region_y), i, (region_w, region_h))

                # 轉換為 RGB 模式
                region = region.convert("RGB")

                # 建立目標大小的白色底圖
                target_image = Image.new("RGB", (image_width, image_height), color="white")

                # 貼上區域圖像
                target_image.paste(region, (0, 0))

                # 建立檔案路徑
                filename = f"{output_folder}/layer_{i + 1}_region_{y}_{x}.jpg"

                # 寫入JPG檔案
                target_image = target_image.resize(tuple([int(image_width * scale_ratio), int(image_height * scale_ratio)]))
                target_image.save(filename, "JPEG")

                print(f"已寫入檔案：{filename}")

    # 關閉圖像
    slide.close()