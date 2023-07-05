import os
from PIL import Image
import pydicom
from pydicom import FileDataset
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from pydicom.uid import generate_uid
from pydicom.encaps import encapsulate

def parse_tag_file(tag_file):
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
    # 创建一个空白的图像
    new_image = Image.new("RGB", target_size, color="black")

    # 计算缩放比例
    width, height = target_size

    # 缩放图像
    resized_image = image.resize((width , height))
    print(target_size)
    # 将缩放后的图像粘贴
    new_image.paste(resized_image, (0, 0))
    #new_image.save(generate_uid() + ".jpg")
    return new_image

def preprocess_images(input_folder, output_file, tag_file):

    # 创建一个空的DICOM数据集
    file_meta = Dataset()

    # 先把基本要顯示圖所必需的tag的先填入 之後再讀取文字檔案做替換修改
    ds = FileDataset(output_file, {},file_meta = file_meta,preamble=b'\0'*128)
    ds.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
    ds.StudyInstanceUID = generate_uid() 
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.77.1.6.1'
    ds.SOPInstanceUID = generate_uid()
    ds.PatientID = "aaaaaawer"
    ds.Modality = 'SM'  # 这里使用'SM'表示静态图像
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

    # 提取所有图像文件的y和x坐标值
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

    # 计算最大的y和x值
    max_y = max(y_values)
    max_x = max(x_values)

    # 对图像文件进行排序，确保按照正确的顺序排列
    jpg_files.sort(key=lambda f: [int(d) for d in f[:-4].split('_')[-2:]])

    # 读取第一张图像获取其大小
    first_image_path = os.path.join(input_folder, jpg_files[0])
    first_image = Image.open(first_image_path)
    target_size = first_image.size

    # 定义缩放比例
    scale_factor = 1  # 根据需要进行调整
    target_size = tuple([int(scale_factor*x) for x in target_size])

    # 计算调整后的TotalPixelMatrixRows和TotalPixelMatrixColumns
    total_rows = (max_y + 1) * target_size[1]
    total_columns = (max_x + 1) * target_size[0]

    # 创建一个空的Pixel Data列表
    pixel_data_list = []

    # 遍历排好序的图像文件
    for i, jpg_file in enumerate(jpg_files):
        # 读取原始图像
        image = Image.open(os.path.join(input_folder, jpg_file))

        # 显示当前处理的图像文件
        print(f"Processing image {i+1}/{len(jpg_files)}: {jpg_file}")

        # 缩放和填充图像
        processed_image = resize_and_fill(image, target_size)

        # 将图像转换为字节数据
        pixel_data = processed_image.tobytes()

        # 添加到Pixel Data列表中
        pixel_data_list.append(pixel_data)    

    # 设置DICOM数据集的相关属性

    ds.NumberOfFrames = len(jpg_files)

    maxSide = max(target_size[1], target_size[0])
    ds.Rows = maxSide
    ds.Columns = maxSide

    # 设置调整后的TotalPixelMatrixRows和TotalPixelMatrixColumns
    ds.TotalPixelMatrixRows = total_rows
    ds.TotalPixelMatrixColumns = total_columns
    
    # 创建一个空的PixelData列表
    pixel_data = b''

    # 将每帧像素数据添加到PixelData列表中
    for frame_data in pixel_data_list:
        pixel_data += frame_data

    # 将像素数据赋值给PixelData属性
    ds.PixelData = pixel_data
    ds.is_little_endian = True  
    ds.is_implicit_VR = True

    # 保存DICOM文件
    pydicom.filewriter.write_file(output_file, ds, write_like_original=False)

