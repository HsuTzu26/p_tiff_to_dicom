from split_tiff_layers_to_jpg_files import split_tiff_layers_to_jpg_files
from preprocess_images import preprocess_images

tiff_file = "input/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).tiff"
jpg_folder = "temp/jpgfiles"
output_path = "output/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).dcm"
tag_file_path = "input/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).txt"

split_tiff_layers_to_jpg_files(tiff_file, "temp/jpgfiles/", target_layer=1)
preprocess_images(jpg_folder, output_path, tag_file_path)

### 如果有多張tiff檔案，可以使用以下程式碼 ###
### Process mutiple files ###
# import os
# import json
# # 讀取 config.json 檔案
# with open('config.json', 'r', encoding='utf-8') as config_file:
#     config = json.load(config_file)

# TIFF_PATH = config['INPUT_FOLDER']
# DCM_PATH = config['OUTPUT_FOLDER']
# # print(os.listdir(TIFF_PATH))
# extension = os.path.splitext(TIFF_PATH)

# tiff_files=[]
# tag_files=[]
# dcm_files=[]

# path = os.getcwd() + '/openslide'

# for path in os.listdir(TIFF_PATH):
#     extension = os.path.splitext(path)
#     # print(extension[1])
#     if extension[1] == '.tiff': # PHILIPS
#         tiff_file_path = TIFF_PATH + '\\' + path
#         tmp = DCM_PATH + '\\' + path
#         dcm_file_path = tmp.replace('.tiff', '.dcm')

#         tiff_files.append(tiff_file_path)
#         dcm_files.append(dcm_file_path)

#     if extension[1] == '.mrxs': # 3DHISTECH
#         tiff_file_path = TIFF_PATH + '\\' + path
#         tmp = DCM_PATH + '\\' + path
#         dcm_file_path = tmp.replace('.mrxs', '.dcm')

#         tiff_files.append(tiff_file_path)
#         dcm_files.append(dcm_file_path)

#     if extension[1] == '.txt':
#         tag_file_path = TIFF_PATH + '\\' + path
#         tag_files.append(tag_file_path)


# for tiff_file, tag_file_path, output_path in zip(tiff_files, tag_files, dcm_files):
#     jpg_folder = "temp/jpgfiles"
    
#     split_tiff_layers_to_jpg_files(tiff_file, "temp/jpgfiles/", target_layer=1)
#     preprocess_images(jpg_folder, output_path, tag_file_path)