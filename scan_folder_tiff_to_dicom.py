from split_tiff_layers_to_jpg_files import split_tiff_layers_to_jpg_files
from preprocess_images import preprocess_images
import os
import json

# 檢查檔案副檔名
def check_file_extension(filename, extension):
    return filename.lower().endswith(extension.lower())

# 檢查檔案副檔名及名稱結尾
def check_file_metadata_and_extension(filename, metadata_suffix, desired_extension):
    # 取得不包含副檔名的檔案名稱
    file_name_without_extension = filename[:filename.rfind('.')]
    
    # 檢查是否結尾為 "_metadata"
    if file_name_without_extension.lower().endswith(metadata_suffix.lower()):
        # 確認檔案名稱長度要比 metadata_suffix 還要長
        if len(file_name_without_extension) > len(metadata_suffix):
            # 檢查檔案名稱是否以期望的副檔名結尾
            if filename.lower().endswith(desired_extension.lower()):
                return True
    return False

def scan_folder_tiff_to_dicom(folder_path, output_folder):
    # 列出資料夾中的所有檔案和子資料夾
    dataFolders = os.listdir(folder_path)

    # 頂層隨機命名的資料夾
    for i in range(0, len(dataFolders), 1):

        # 輸入變數
        tiff_file = ""
        jpg_folder = "temp/jpgfiles"
        output_path = ""
        tag_file_path = ""

        pyDir = folder_path + "\\" + dataFolders[i]
        pyFolder = os.listdir(pyDir)
        output_path = output_folder + "\\" + dataFolders[i] + '.dcm'
        # 各個資料夾內檢查是否有pathology資料夾
        for j in range(0,len(pyFolder),1):
            if pyFolder[j] == 'pathology':
                pathDir = pyDir + "\\" + pyFolder[j]
                pathFolder = os.listdir(pathDir)
                # 檢查是否有wsi資料夾
                for k in range(0,len(pathFolder),1):
                    wsiDir = pathDir + "\\" + pathFolder[k]
                    wsiFolder = os.listdir(wsiDir)
                    # 取得tiff路徑
                    for l in range(0,len(wsiFolder),1):
                        if (tiff_file == '') and (check_file_extension(wsiFolder[l], 'tiff') == True):
                            #print('tiff檔案:' + wsiFolder[l])
                            tiff_file = wsiDir + "\\" + wsiFolder[l]
                        if wsiFolder[l] == 'metadata':
                            metaFolder = os.listdir(wsiDir + "\\" + wsiFolder[l])
                            for m in range(0,len(metaFolder),1):
                                if  (tag_file_path == '') and (check_file_metadata_and_extension(metaFolder[m], '_metadata', '.txt') == True):
                                    #print('metadata檔案:' + metaFolder[m])
                                    tag_file_path = wsiDir + "\\" + wsiFolder[l] + "\\" +metaFolder[m]
                                pass
                            pass
                        pass
                    pass
                pass
            pass
        pass

        print('==========================')
        print('tiff檔案:' +  tiff_file)
        print('metadata檔案:' +  tag_file_path)
        print('-                        -')
        print('開始轉換')
        split_tiff_layers_to_jpg_files(tiff_file, "temp/jpgfiles/", target_layer=1)
        preprocess_images(jpg_folder, output_path, tag_file_path)
        print('轉換完成')
        print('-                        -')
        print('dicom檔案:' +  output_path)
        print('==========================')

    pass
pass

# 讀取 config.json 檔案
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# 從 config 中提取數值
input_folder = config["INPUT_FOLDER"]
output_folder = config["OUTPUT_FOLDER"]

# 使用提取的數值呼叫函數
scan_folder_tiff_to_dicom(input_folder, output_folder)
