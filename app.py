import os
from functions import catch_img_file, create_metadata
from preprocess_images import preprocess_images
from split_tiff_layers_to_jpg_files import split_tiff_layers_to_jpg_files, split_tiff_layers_to_jpg_files_slice 

### Process mutiple files ###
import json
# 讀取 config.json 檔案
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

### 病理切片影像路徑, DCM 儲存路徑, Metadata 路徑設置 ###
IMG_PATH = config['INPUT_FOLDER']
DCM_PATH = config['OUTPUT_FOLDER']

jpg_folder = "temp/jpgfiles"
""" 北榮影像 """
img_files, tag_files, dcm_files = catch_img_file(IMG_PATH=IMG_PATH, DCM_PATH=DCM_PATH, IMG_endwith='tiff') # set IMG_endwith as tiff or mrxs
create_metadata(IMG_PATH=IMG_PATH, IMG_endwith='tiff')
for tiff_file, tag_file_path, output_path in zip(img_files, tag_files, dcm_files):
    split_tiff_layers_to_jpg_files(tiff_file, "temp/jpgfiles/", target_layer=1)
    preprocess_images(jpg_folder, output_path, tag_file_path)

""" 成大影像 """
img_files, tag_files, dcm_files = catch_img_file(IMG_PATH=IMG_PATH, DCM_PATH=DCM_PATH, IMG_endwith='mrxs') # set IMG_endwith as tiff or mrxs
for mrxs, dcm, tag in zip(img_files, tag_files, dcm_files):
    split_tiff_layers_to_jpg_files_slice(mrxs, "temp/jpgfiles/", target_layer=1, num_blocks=100)
    preprocess_images(jpg_folder, dcm, tag) 

