import os
from split_tiff_layers_to_jpg_files import split_tiff_layers_to_jpg_files, split_tiff_layers_to_jpg_files_slice 
from preprocess_images import preprocess_images
from check import check_single_file, dcmtk_process

# tiff_file = "input/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).tiff"
# jpg_folder = "temp/jpgfiles"
# output_path = "output/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).dcm"
# tag_file_path = "input/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).txt"

# split_tiff_layers_to_jpg_files(tiff_file, "temp/jpgfiles/", target_layer=1)
# preprocess_images(jpg_folder, output_path, tag_file_path)

### 如果有多張tiff檔案，可以使用以下程式碼 ###
### Process mutiple files ###
import os
import json
# 讀取 config.json 檔案
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

### 病理切片影像路徑, DCM 儲存路徑, Metadata 路徑設置 ###
# TIFF_PATH = config['INPUT_FOLDER']
# DCM_PATH = config['OUTPUT_FOLDER']
# # print(os.listdir(TIFF_PATH))
# extension = os.path.splitext(TIFF_PATH)

# tiff_files, tag_files, dcm_files = [], [], []

# path = os.getcwd() + '/openslide'

# for path in os.listdir(TIFF_PATH):
#     extension = os.path.splitext(path)
#     # print(extension[1])
#     if extension[1] == '.tiff': # PHILIPS 北榮影像
#         tiff_file_path = TIFF_PATH + '\\' + path
#         tmp = DCM_PATH + '\\' + path
#         dcm_file_path = tmp.replace('.tiff', '.dcm')

#         tiff_files.append(tiff_file_path)
#         dcm_files.append(dcm_file_path)

#     if extension[1] == '.mrxs': # 3DHISTECH 成大影像
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

### 成大影像 ###
jpg_folder = "temp/jpgfiles"
metadata_folder = 'D:\\AUUFFC_cylab\\DITTO\\p_tiff_to_dicom\\tiff'
metadata_path = [os.path.join(metadata_folder, _) for _ in os.listdir(metadata_folder) if _.endswith('.txt')]

ncku_image_folder = 'D:\\AUUFFC_data\\wsi\\ncku_wsi_nash\\image'
ncku_mrxs_path = [os.path.join(ncku_image_folder, _) for _ in os.listdir(ncku_image_folder) if _.endswith('.mrxs')]


ncku_dcm_opt_folder = "D:\\AUUFFC_cylab\\DITTO\\p_tiff_to_dicom\\dcm"
ncku_dcm_path = []
for _ in ncku_mrxs_path:
    extension = os.path.splitext(_)
    ncku_dcm_path.append(os.path.join(ncku_dcm_opt_folder, _.split('\\')[-1].replace(extension[1], '.dcm')))

### muti-files processing ###
# for mrxs, dcm, tag in zip(ncku_mrxs_path, ncku_dcm_path, metadata_path):

#       ## 設定處理後的 DCM 儲存路徑 ###
#     output_file = os.path.join(ncku_dcm_opt_folder, 'opt_' + dcm.split('\\')[-1])
#     # print(output_file)

#     # split_tiff_layers_to_jpg_files(mrxs, "temp/jpgfiles/", target_layer=1, scale_ratio=0.01,image_width=10000, image_height=10000) 

#     split_tiff_layers_to_jpg_files_slice(mrxs, "temp/jpgfiles/", target_layer=6, num_blocks=10)
#     preprocess_images(jpg_folder, dcm, tag) 
#     check_single_file(dcm, output_file)
#     dcmtk_process(output_file)

print(ncku_mrxs_path[6], ncku_dcm_path[6], metadata_path[6])

output_file = os.path.join(ncku_dcm_opt_folder, 'opt_' + ncku_dcm_path[6].split('\\')[-1])

split_tiff_layers_to_jpg_files_slice(ncku_mrxs_path[6], "temp/jpgfiles/", target_layer=3, num_blocks=10)
preprocess_images(jpg_folder, ncku_dcm_path[6], metadata_path[6]) 
check_single_file(ncku_dcm_path[6], output_file)
dcmtk_process(output_file)

