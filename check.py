import os
import pydicom
import numpy as np

def dcmtk_dcmodify(input_file):

    ### 切換至 dcmtk\\bin 路徑 ###
    os.chdir("D:\AUUFFC_tools\dcmtk-3.6.7-win64-dynamic\\bin")
    print('now in: ', os.getcwd())

    ### write with explicit VR little endian TS in quite mode and no backup ###
    command = 'dcmodify -q +te -nb '

    command += input_file

    os.system(command)
    d = os.popen(command)
    print(d.read())
    print(f'The DICOM file {input_file} has been modified.')

def check_single_file(input_file, output_file):

    ds = pydicom.dcmread(input_file)

    print(ds)

    sopclassuid = "1.2.840.10008.5.1.4.1.1.77.1.6"
    modality = "SM"

    if ds[0x0008,0x0016].value != sopclassuid:
        print("Modifying SOPClassUID")
        ds[0x0008,0x0016].value = sopclassuid

    if ds[0x0008,0x0016].value != modality:
        print("Modifying SOPClassUID")
        ds[0x0008,0x0060].value = modality

    
    print(ds)
    # print(f'SOPClassUID: {ds.SOPClassUID}')
    # print(f'Modality: {ds.Modality}')
    # print(f'Accession Number: {ds[0x0008, 0x0050].value}')  
    # print(f'Image Type: {ds[0x0008,0x0008]}')

    ds.save_as(output_file)
    print('=== done. ===')

def check_muti_files(input_file, output_file):

    for i in range(len(input_file)):

        ds = pydicom.dcmread(input_file[i])

        sopclassuid = "1.2.840.10008.5.1.4.1.1.77.1.6"
        modality = "SM"

        # if ds[0x0008,0x0016].value != sopclassuid:
        print("Modifying SOPClassUID")
        ds[0x0008,0x0016].value = sopclassuid

        # if ds[0x0008,0x0016].value != modality:
        print("Modifying SOPClassUID")
        ds[0x0008,0x0060].value = modality

        print(ds)
        # print(f'SOPClassUID: {ds.SOPClassUID}')
        # print(f'Modality: {ds.Modality}')
        # print(f'Accession Number: {ds.AccessionNumber}')

        ds.save_as(output_file[i])
        print("================================")

    print('=== done. ===')


### muti-files processing testing example###
# target_folder = "dcm"
# input_file = [os.path.join(os.path.join(os.getcwd(), target_folder), _) for _ in os.listdir(f"./{target_folder}")]

# for i in range(len(input_file)):

#     ds = pydicom.dcmread(input_file[i])

#     sopclassuid = "1.2.840.10008.5.1.4.1.1.77.1.6"
#     modality = "SM"

#     if ds[0x0008,0x0016].value != sopclassuid:
#         print("Modifying SOPClassUID")
#         ds[0x0008,0x0016].value = sopclassuid

#     if ds[0x0008,0x0016].value != modality:
#         print("Modifying SOPClassUID")
#         ds[0x0008,0x0060].value = modality

#     print(f'SOPClassUID: {ds.SOPClassUID}')
#     print(f'Modality: {ds.Modality}')
#     print(f'Accession Number: {ds.AccessionNumber}')

#     print("================================")

# print("done.")
