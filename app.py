from split_tiff_layers_to_jpg_files import split_tiff_layers_to_jpg_files
from preprocess_images import preprocess_images

tiff_file = "input/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).tiff"
jpg_folder = "temp/jpgfiles"
output_path = "output/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).dcm"
tag_file_path = "input/604fd0ec-eae2-472c-a5ae-d57eb6f65bbd-FMT0406_20210615_010912_1_20210615_091754_(3).txt"

split_tiff_layers_to_jpg_files(tiff_file, "temp/jpgfiles/", target_layer=1)
preprocess_images(jpg_folder, output_path, tag_file_path)
