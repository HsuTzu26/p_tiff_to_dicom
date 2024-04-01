import os
import pydicom
import numpy as np

target_folder = "dcm"

input_file = [os.path.join(os.path.join(os.getcwd(), target_folder), _) for _ in os.listdir(f"./{target_folder}")]


for i in range(len(input_file)):

    ds = pydicom.dcmread(input_file[i])

    sopclassuid = "1.2.840.10008.5.1.4.1.1.77.1.6"
    modality = "SM"

    if ds[0x0008,0x0016].value != sopclassuid:
        print("Modifying SOPClassUID")
        ds[0x0008,0x0016].value = sopclassuid

    if ds[0x0008,0x0016].value != modality:
        print("Modifying SOPClassUID")
        ds[0x0008,0x0060].value = modality

    print(f'SOPClassUID: {ds.SOPClassUID}')
    print(f'Modality: {ds.Modality}')
    print(f'Accession Number: {ds.AccessionNumber}')

    print("================================")

print("done.")
