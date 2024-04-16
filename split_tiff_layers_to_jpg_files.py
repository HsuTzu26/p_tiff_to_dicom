import json
# 讀取 config.json 檔案
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
OPENSLIDE_PATH = config["OPENSLIDE_PATH"] + "\\bin"

# import os
# open_slide_path = os.getcwd() + "\\openslide\\bin"
# os.environ['PATH'] = open_slide_path + ';' + os.environ['PATH']
# from openslide import OpenSlide

import os
import gc
from PIL import Image
import numpy as np

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
    # slide = OpenSlide(input_file)
    slide = OpenSlide(input_file)

    # 獲取圖層數量
    num_layers = slide.level_count
    print(f"numlayers={num_layers}")
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

        print(num_regions_x, num_regions_y)

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


def split_tiff_layers_to_jpg_files_slice(input_file, output_folder, target_layer=0, num_blocks=1):
    """
    input_file: 輸入的TIFF檔案路徑。
    output_folder: 輸出JPG檔案的資料夾路徑。
    target_layer: 從TIFF檔案中提取的層索引。
    num_blocks: 將圖像分割成的方塊數量。
    """

    # 建立輸出資料夾
    os.makedirs(output_folder, exist_ok=True)\

    # 刪除輸出資料夾底下的所有檔案
    file_list = os.listdir(output_folder)
    for file_name in file_list:
        file_path = os.path.join(output_folder, file_name)
        os.remove(file_path)


    # 開啟TIFF檔案
    slide = OpenSlide(input_file)
    
    # 獲取指定層的尺寸
    width, height = slide.level_dimensions[target_layer]
    print(f"全圖大小為:[{width}, {height}]")
    
    # 取得第0層的大小(位置用到)
    fwidth, fheight = slide.level_dimensions[0]
    print(f"第0層全圖大小為:[{fwidth}, {fheight}]")
    
    # 計算每個區塊的寬度和高度
    block_size = max(width, height) // num_blocks
    fblock_size = max(fwidth, fheight) // num_blocks

    # 逐個區塊處理
    for j in range(num_blocks):
        for i in range(num_blocks):
            # 計算當前區塊的位置和尺寸
            x_position = i * fblock_size
            y_position = j * fblock_size
            block_dimensions = (block_size, block_size)
            
            # 讀取對應於當前區塊的區域
            region = np.array(slide.read_region((x_position, y_position), target_layer, block_dimensions))
            
            # 將區域轉換為RGBA格式
            region_rgba = Image.fromarray(region, 'RGBA')
            
            # 如果輸出資料夾不存在，則創建之
            os.makedirs(output_folder, exist_ok=True)
            
            # 定義輸出檔案路徑
            output_file = os.path.join(output_folder, f"layer_{target_layer}_region_{j}_{i}.jpg")
            
            # 用白色填充透明部分
            region_rgba = fill_transparent_with_white(region_rgba)
            
            # 將區塊保存為JPG檔案
            region_rgba.save(output_file, "JPEG")
            print(f"已保存區塊({j}, {i})至{output_file}")

            del region_rgba
            gc.collect()


    # 關閉圖像
    slide.close()

def fill_transparent_with_white(img):
    """
    使用白色填充RGBA圖片的透明部分。
    img: RGBA模式的PIL圖片對象。
    返回填充透明部分後的新PIL圖片對象。
    """
    # 創建白色背景圖片
    background = Image.new('RGBA', img.size, (255, 255, 255, 255))
    
    # 在白色背景上合成原始圖片
    new_img = Image.alpha_composite(background, img)
    
    # 轉換為RGB模式
    new_img = new_img.convert('RGB')
    
    return new_img
