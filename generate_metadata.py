tag_file_path="./tiff\example_metadata.txt"

with open(tag_file_path, 'r', encoding='utf-8') as f:
    metadata = f.readlines()

tag_list = [_.split(":")[0] for _ in metadata]
content_list = [_.split(":")[1].replace("\n", "") for _ in metadata]


import uuid
import random
from pydicom.uid import generate_uid
from datetime import datetime, timedelta

def random_date():
    # 生成隨機的年份（2000年至今）
    random_year = random.randint(2000, datetime.now().year)

    # 生成隨機的月份和日期
    random_month = random.randint(1, 12)
    random_day = random.randint(1, 28)  # 為了保險起見，假設每個月都是28天

    # 建立日期對象
    random_date = datetime(random_year, random_month, random_day)

    # 格式化為 YYYYMMDD 
    formatted_date = random_date.strftime("%Y/%m/%d")

    return formatted_date


def generate_metadata():

    metadata_dic={}

    for t in tag_list:
        metadata_dic[t] = ""


    patient_sex = "O"
    randomDate = random_date()
    patientID = patient_sex + randomDate.split("/")[0]
    accessionNumber = "NTUNHS-" + randomDate.split("/")[0]
    randomString = randomDate.split("/")[0]
    # print(patientName)

    metadata_dic["Patient ID"] = patientID
    metadata_dic["Patient Name"] = ""
    metadata_dic["Patient Birth Date"] = randomDate.replace("/", "")
    metadata_dic["Patient Sex"] = "O"
    metadata_dic["Study Instance UID"] = generate_uid() 
    metadata_dic["Accession Number"] = accessionNumber
    metadata_dic["Study Date"] = "20020202"
    metadata_dic["Study Time"] = "123456.789012"
    metadata_dic["Study Last Modified Date"] = "20020203123456.789012"
    metadata_dic["Study Scheduled Pathologist Name"] = "NTUNHS"
    metadata_dic["Second Pathologist Name"] = "NTUNHS"
    metadata_dic["Series Instance UID"] = generate_uid() 
    metadata_dic["Modality"] = "SM"
    metadata_dic["Manufacturer"] = "3DHISTECH"
    metadata_dic["Institution Name"] = "NTUNHS"
    metadata_dic["Institutional Department Name"] = "NTUNHS"
    metadata_dic["Device Serial Number"] = "NTUNHS0123"
    metadata_dic["Software Versions"] = "3.0.3.139795"
    metadata_dic["Last Calibration Date"] = "20020203"
    metadata_dic["Last Calibration Time"] = "012345"
    metadata_dic["Secondary Capture Device Manufacturer"] = "3DHISTECH"
    metadata_dic["Secondary Capture Device Manufacturer's Model Name"] = "NTUNHS"
    metadata_dic["Secondary Capture Device Software Versions"] = "01.03"
    metadata_dic["SOP Instance UID"] = generate_uid() 
    metadata_dic["Pixel data filename"] = "X:\BIOBANK\\20-00010-HE-1000-01.mrxs"
    metadata_dic["Pixel data size (bytes/GB)"] = "9002573824/2.08"
    metadata_dic["Image Type"] = "VOLUME"
    metadata_dic["Acquisition Datetime"] = "20020203123456.000000"
    metadata_dic["Instance Creation Date"] = "20020203"
    metadata_dic["Instance Creation Time"] = "123456.789012"
    metadata_dic["Derivation Description"] = "NTUNHS"
    metadata_dic["Pixel Spacing"] = "0.00025, 0.00025"
    metadata_dic["Lossy Image Compression"] = "01"
    metadata_dic["Lossy Image Compression Ratio"] = "3"
    metadata_dic["Lossy Image Compression Method"] = "3DHISTCH_SKILL"
    metadata_dic["Scanner Calibration Status"] = "OK"
    metadata_dic["Container Identifier"] = "NTUNHS0123_20020203"
    metadata_dic["Block Identifier"] = "C"
    metadata_dic["Part Identifier"] = "012"
    metadata_dic["Stain Name"] = "NTUNHS"
    metadata_dic["Stain Type Name"] = "StainTypeName"
    metadata_dic["Institution Address"] = "NTUNHS Taipei City"
    metadata_dic["Photometric Interpretation"] = "RGB"
    metadata_dic["Secondary Capture Device ID"] = uuid.uuid4()
    metadata_dic["Study ID"] = f"S123-{randomString}"

    f_path = f"./tiff/{accessionNumber}_metadata.txt"
    with open(f_path, "w") as f:
        for k, v in metadata_dic.items():
            f.writelines(f"{k}: {v}\n")
    # return metadata_dic

generate_metadata()







    