import json
# 讀取 config.json 檔案
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
OPENSLIDE_PATH = config["OPENSLIDE_PATH"] + "\\bin"

# print(OPENSLIDE_PATH)

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        from openslide import OpenSlide
else:
    from openslide import OpenSlide

# input_file="D:\\AUUFFC_data\\wsi\\Mirax2-Fluorescence-1\\Mirax2-Fluorescence-1.mrxs"

# input_file="D:\\AUUFFC_data\\wsi\\ncku_wsi_nash\\image\\19-00001-HE.mrxs"
# input_file="D:\\AUUFFC_data\\wsi\\Mirax2.2-1\\Mirax2.2-1.mrxs"
input_file="D:\\AUUFFC_data\\wsi\\20-00010-HE\\20-00010-HE.mrxs"


slide = OpenSlide(input_file)

# print(slide.properties)


# with open('./slideproperties', 'w') as f:
#     for k, v in slide.properties.items():
#         f.write(f"{k}: {v}\n")


# # 高倍率到低倍率
# level_count = slide.level_count
# print('level_count:', level_count)

# # dimensions
# [m, n] = slide.dimensions
# print(m,n)

level=0
size=(0,0)

#級別k，且k必須是整數，下採樣因子與k有關
for i in range(slide.level_count):    
    [m,n] = slide.level_dimensions[i]                      # 每一个级别对应的长和宽
    slide_level_downsamples = slide.level_downsamples[i]   # 下采样因子对应一个倍率
    print (f"k={i}時的長和寬{m,n}和下採樣倍率{slide_level_downsamples}") 
    if i==4:
        level=i
        size=(m,n)
slide_downsamples = slide.get_best_level_for_downsample(2.0)  # 选定倍率返回下采样级别
print (slide_downsamples)

# # read_region(location, level, size) 返回一個 RGBA 圖像, 包含指定區域的內容 
# # # location 指 0 級別下左上角的座標, 元組, level 指定級別, 整數, size 指定寬和高是元組
# tile = np.array(slide.read_region((0,0),6, (1366, 3218)))
# plt.figure()
# plt.imshow(tile)
# plt.show()
#上述程式碼可以得到左上角座標（0,0）,6 级别下，大小是（1366, 3218）的图

# # # #get_thumbnail(size) 返回一個縮略圖，size是一個元組，指定縮略圖的寬和高
# region = slide.read_region(location=(0,0), level=level, size=size)
# # slide_thumbnail = slide.get_thumbnail((4770, 10685))

# # tile = np.array(slide_thumbnail)
# # plt.imshow(slide_thumbnail)
# # plt.imshow(tile)
# # plt.show()

# # # print(region.split())
# r, g, b, a = region.split()

# # g_mask = g.point(lambda x: x)

# # # 合併通道
# # bgr_image = Image.merge("RGB", (r.point(lambda x: 0), g_mask, b.point(lambda x: 0)))
# bgr_image = Image.merge("RGB", (b,g,r))

# # 顯示BGR影像
# bgr_image.show()

suffix=input_file.split('\\')[-1].replace('.mrxs','')
output_path = f'./{suffix}.png'
# bgr_image.save(output_path)

# import cv2
# img_path = "D:\AUUFFC_cylab\DITTO\p_tiff_to_dicom\dcm\Mirax2.2.1_jpg\\test.jpg.223.jpg"
# # img_path = "D:\AUUFFC_cylab\DITTO\p_tiff_to_dicom\dcm\Mirax2-Fluorescence-1_jpg\.130.jpg"
# # img = cv2.imread(img_path)
# img = Image.open(img_path)

# r,g,b= img.split()
# img = Image.merge("RGB", (b,r,g))
# img.show()

# alpha = 1.0  # Contrast control (1.0 means no change)
# beta = 50   # Brightness control (0 means no change)
# g = cv2.convertScaleAbs(g, alpha=alpha, beta=beta)

# Create a green mask
# green_mask = np.ones_like(g) * 100  # Fully opaque green mask

# Apply the green mask to the green channel
# g = cv2.bitwise_and(g, g, mask=green_mask)

# b = np.zeros_like(b)
# r = np.zeros_like(r)

# img = cv2.merge([g,r,b])

# plt.imshow(img)
# plt.show()