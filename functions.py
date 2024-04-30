import os
from generate_metadata import generate_metadata 

def catch_img_file(IMG_PATH=None, DCM_PATH=None, IMG_endwith=None):
    img_files, tag_files, dcm_files = [], [], []

    img_path = os.path.abspath(IMG_PATH)
    dcm_path = os.path.abspath(DCM_PATH)

    img_files = [os.path.join(img_path, _) for _ in os.listdir(IMG_PATH) if _.endswith(f'.{IMG_endwith}')]
    dcm_files = [os.path.join(dcm_path, _.replace(IMG_endwith, 'dcm')) for _ in os.listdir(IMG_PATH) if _.endswith(f'.{IMG_endwith}')]
    tag_files = [os.path.join(img_path, _) for _ in os.listdir(IMG_PATH) if _.endswith('.txt')]

    return img_files, tag_files, dcm_files

def create_metadata(IMG_PATH=None, IMG_endwith=None):
    img_files = [_ for _ in os.listdir(IMG_PATH) if _.endswith(f'.{IMG_endwith}')]

    for _ in range(len(img_files)):
        generate_metadata()
