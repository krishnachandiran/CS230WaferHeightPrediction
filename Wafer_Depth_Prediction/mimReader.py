import glob
import os
import numpy as np
from PIL import Image


def mimfileread(filepointer, mim2_format):
    num_bytes = 4 if mim2_format else 2
    height = filepointer.read(num_bytes)
    height = int.from_bytes(height, byteorder='little')
    filepointer.seek(num_bytes)
    width = filepointer.read(num_bytes)
    width = int.from_bytes(width, byteorder='little')
    print(height)
    print(width)
    image = np.zeros(shape=(height, width), dtype=np.uint16)

    for i in range(height):
        for j in range(width):
            seeklength = 4 + (i*width + j)*2
            filepointer.seek(seeklength)
            pixel = filepointer.read(2)
            pixel = int.from_bytes(pixel, byteorder='little')
            image[i][j] = pixel


    return image


if __name__ == '__main__':
    input_folder = r"E:\DL\5X_center_dies_MOI_items\MK_Dynamic_Swath_Feature_5x_Dynamic_Swath_Alignment_New_MOI_5x_inps_Test1_20211115045534"
    output_folder = r"E:\DL\5X_center_dies_MOI_items\MK_Dynamic_Swath_Feature_5x_Dynamic_Swath_Alignment_New_MOI_5x_inps_Test1_20211115045534\png"


    read_mim2 = True
    mim_ext = '*.mim2' if read_mim2 else '*.mim'

    mimfile_list = glob.glob(input_folder + "\\" + mim_ext)

    for full_File_Name in mimfile_list:
        basefileName = os.path.basename(full_File_Name)
        filename_without_Extn, ext = os.path.splitext(basefileName)
        output_file = os.path.join(output_folder, filename_without_Extn + ".png")
        print('Converting %s is %s' % (full_File_Name, output_file))

        with open(full_File_Name, "rb") as filep:
            image = mimfileread(filep, read_mim2)

            image_buffer = image.tobytes()
            img = Image.new("I", image.T.shape)
            img.frombytes(image_buffer, 'raw', "I;16")
            img.save(output_file)
