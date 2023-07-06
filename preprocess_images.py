import os
from PIL import Image
import pydicom
from pydicom import FileDataset
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from pydicom.uid import generate_uid
from pydicom.encaps import encapsulate

def parse_tag_file(tag_file):
    """
    解析標籤文字檔案，獲取標籤字典。
    Args:
        tag_file: 標籤檔案的路徑
    Returns:
        tags: 標籤字典
    """
    tags = {}
    with open(tag_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                tag_line = line.split(': ', 1)
                tag_name = tag_line[0]
                tag_value = tag_line[1] if len(tag_line) > 1 else ""
                tags[tag_name] = tag_value
    return tags

def resize_and_fill(image, target_size):
    """
    將圖像縮放並填充到指定的目標大小。
    Args:
        image: PIL圖像對象
        target_size: 目標大小 (寬度, 高度)
    Returns:
        new_image: 縮放並填充後的圖像
    """
    # 創建一個空白的圖像
    new_image = Image.new("RGB", target_size, color="black")

    # 縮放圖像
    resized_image = image.resize(target_size)
    
    # 將縮放後的圖像粘貼到新圖像中
    new_image.paste(resized_image, (0, 0))
    
    return new_image

def preprocess_images(input_folder, output_file, tag_file):
    """
    將一堆jpg依照命名規則的圖檔，加上文字檔的tag，生成multiframe DICOM文件。
    Args:
        input_folder: 輸入圖像的文件夾
        output_file: 輸出的DICOM文件路徑
        tag_file: 標籤檔案的路徑
    """
    # 創建一個空的DICOM數據集
    file_meta = Dataset()
    ds = FileDataset(output_file, {}, file_meta=file_meta, preamble=b'\0'*128)
    
    # 設置DICOM數據集的初始屬性
    ds.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
    ds.StudyInstanceUID = generate_uid() 
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.77.1.6.1'
    ds.SOPInstanceUID = generate_uid()
    ds.PatientID = "aaaaaawer"
    ds.Modality = 'SM'
    ds.PatientName = 'Anonymous'
    ds.PatientSex = 'M'
    ds.PatientBirthDate = '19600101'
    ds.StudyDate = '20210623'
    ds.StudyTime = '181944.786966'

    ds.ImagedVolumeWidth = 0.00025
    ds.ImagedVolumeHeight = 0.00025
    ds.TotalPixelMatrixOriginSequence = Sequence([Dataset()])
    ds.TotalPixelMatrixOriginSequence[0].XOffsetInSlideCoordinateSystem = 0
    ds.TotalPixelMatrixOriginSequence[0].YOffsetInSlideCoordinateSystem = 0

    ds.ImageType = 'VOLUME'
    ds.LossyImageCompression = '01'
    ds.PlanarConfiguration = 0
    ds.SamplesPerPixel = 3
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PhotometricInterpretation = 'RGB'
    ds.PixelRepresentation = 0
    
    # 解析標籤文字檔案，獲取標籤字典
    tags = parse_tag_file(tag_file)

    # 將標籤填入 DICOM 資料集中
    ds.PatientID = tags.get('Patient ID', '')
    ds.PatientName = tags.get('Patient Name', '')
    ds.PatientBirthDate = tags.get('Patient Birth Date', '')
    ds.PatientSex = tags.get('Patient Sex', '')
    ds.StudyInstanceUID = tags.get('Study Instance UID', '')
    ds.AccessionNumber = tags.get('Accession Number', '')
    ds.StudyDate = tags.get('Study Date', '')
    ds.StudyTime = tags.get('Study Time', '')
    ds.StudyLastModifiedDate = tags.get('Study Last Modified Date', '')
    ds.StudyScheduledPathologistName = tags.get('Study Scheduled Pathologist Name', '')
    ds.SecondPathologistName = tags.get('Second Pathologist Name', '')
    ds.SeriesInstanceUID = tags.get('Series Instance UID', '')
    ds.Modality = tags.get('Modality', '')
    ds.Manufacturer = tags.get('Manufacturer', '')
    ds.InstitutionName = tags.get('Institution Name', '')
    ds.InstitutionalDepartmentName = tags.get('Institutional Department Name', '')
    ds.DeviceSerialNumber = tags.get('Device Serial Number', '')
    ds.SoftwareVersions = tags.get('Software Versions', '')
    ds.LastCalibrationDate = tags.get('Last Calibration Date', '')
    ds.LastCalibrationTime = tags.get('Last Calibration Time', '')
    ds.SecondaryCaptureDeviceManufacturer = tags.get('Secondary Capture Device Manufacturer', '')
    ds.SecondaryCaptureDeviceManufacturerModelName = tags.get('Secondary Capture Device Manufacturer\'s Model Name', '')
    ds.SecondaryCaptureDeviceSoftwareVersions = tags.get('Secondary Capture Device Software Versions', '')
    ds.SOPInstanceUID = tags.get('SOP Instance UID', '')
    ds.PixelSpacing = [float(x) for x in tags['Pixel Spacing'].split(', ')]
    ds.LossyImageCompression = tags.get('Lossy Image Compression', '')
    ds.LossyImageCompressionRatio = tags.get('Lossy Image Compression Ratio', '')
    ds.LossyImageCompressionMethod = tags.get('Lossy Image Compression Method', '')
    ds.Barcode = tags.get('Barcode', '')
    ds.ScannerCalibrationStatus = tags.get('Scanner Calibration Status', '')
    ds.ContainerIdentifier = tags.get('Container Identifier', '')
    ds.BlockIdentifier = tags.get('Block Identifier', '')
    ds.PartIdentifier = tags.get('Part Identifier', '')
    ds.StainName = tags.get('Stain Name', '')
    ds.StainTypeName = tags.get('Stain Type Name', '')
    ds.InstitutionAddress = tags.get('Institution Address', '')
    ds.PhotometricInterpretation = tags.get('Photometric Interpretation', '')
    ds.SecondaryCaptureDeviceID = tags.get('Secondary Capture Device ID', '')
    ds.StudyID = tags.get('Study ID', '')

    # 提取所有圖像文件的y和x坐標值
    y_values = []
    x_values = []
    jpg_files = []
    for file in os.listdir(input_folder):
        if file.endswith('.jpg'):
            jpg_files.append(file)
            parts = file[:-4].split('_')
            y = parts[-2]
            x = parts[-1]
            y_values.append(int(y))
            x_values.append(int(x))

    # 計算最大的y和x值
    max_y = max(y_values)
    max_x = max(x_values)

    # 對圖像文件進行排序，確保按照正確的順序排列
    jpg_files.sort(key=lambda f: [int(d) for d in f[:-4].split('_')[-2:]])

    # 讀取第一張圖像獲取其大小
    first_image_path = os.path.join(input_folder, jpg_files[0])
    first_image = Image.open(first_image_path)
    target_size = first_image.size

    # 定義縮放比例
    scale_factor = 1  # 根據需要進行調整
    target_size = tuple([int(scale_factor*x) for x in target_size])

    # 計算調整後的TotalPixelMatrixRows和TotalPixelMatrixColumns
    total_rows = (max_y + 1) * target_size[1]
    total_columns = (max_x + 1) * target_size[0]

    # 創建一個空的Pixel Data列表
    pixel_data_list = []

    # 遍歷排好序的圖像文件
    for i, jpg_file in enumerate(jpg_files):
        # 讀取原始圖像
        image = Image.open(os.path.join(input_folder, jpg_file))

        # 顯示當前處理的圖像文件
        print(f"Processing image {i+1}/{len(jpg_files)}: {jpg_file}")

        # 縮放和填充圖像
        processed_image = resize_and_fill(image, target_size)

        # 將圖像轉換為字節數據
        pixel_data = processed_image.tobytes()

        # 添加到Pixel Data列表中
        pixel_data_list.append(pixel_data)    

    # 設置DICOM數據集的相關屬性

    ds.NumberOfFrames = len(jpg_files)

    maxSide = max(target_size[1], target_size[0])
    ds.Rows = maxSide
    ds.Columns = maxSide

    # 設置調整後的TotalPixelMatrixRows和TotalPixelMatrixColumns
    ds.TotalPixelMatrixRows = total_rows
    ds.TotalPixelMatrixColumns = total_columns
    
    # 創建一個空的PixelData列表
    pixel_data = b''

    # 將每幀像素數據添加到PixelData列表中
    for frame_data in pixel_data_list:
        pixel_data += frame_data

    # 將PixelData賦值給DICOM數據集
    ds.PixelData = pixel_data

    # 將DICOM數據集保存為文件
    ds.save_as(output_file)

    # 調整後的PixelData列表
    ds.PixelData = encapsulate([pixel_data])

    # 保存DICOM數據集為文件
    ds.save_as(output_file)
