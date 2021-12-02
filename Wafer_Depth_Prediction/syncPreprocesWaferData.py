######################Right to Left working for 33rd,35th swath
import cv2
imagePath = "E:\\DL\\5X_center_dies_MOI_items\\MK_Dynamic_Swath_Feature_5x_Dynamic_Swath_Alignment_New_MOI_5x_inps_Test1_20211115045534\png\SwathTypeEnum[4,Random Swath]35_BF_234342.raw.png"
#imagePath = "E:\\DL\\5X_center_dies_MOI_items\\im.png"
swathDetails = "E:\DL\5X_center_dies_MOI_items\MK_Dynamic_Swath_Feature_5x_Dynamic_Swath_Alignment_New_MOI_5x_inps_Test1_20211115045534\SwathDetails"
snapShot = "E:\\DL\\5X_center_dies_MOI_items\\5X_center_dies_MOI\\StageSnapshot_20211115052711\\AMACDiagRecorder_20211115052711.csv"
name = "35"

import math
from PIL import Image
import numpy as np
import csv
# import cv2
Image.MAX_IMAGE_PIXELS = None

# img = cv2.imread(imagePath)
# crop_img = img[y:y+h, x:x+w]
# cv2.imshow("cropped", crop_img)
# cv2.waitKey(0)
im = Image.open(imagePath)
width, height = im.size
print("Image Width:" + str(width))
print("Image Height:" + str(height))


a=[]
b=[]
c=[]


with open(snapShot, 'r') as read_obj: # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj) # Get all rows of csv from csv_reader object as list of tuples
    list_of_tuples = list(map(tuple, csv_reader)) # display all rows of csv
    
count = 0
startFlag = 0;
for i in range(7,len(list_of_tuples)-1):
    if(int(list_of_tuples[i][24]) == 1):
        count = count + 1
        a.append(int(list_of_tuples[i][1]))
        b.append(int(list_of_tuples[i][9]))
        c.append(int(list_of_tuples[i][4]))

# Program to draw scatter plot using Dataframe.plot
# Import libraries

print("Start X: " + str(a[0]))
print("Start X+1: " +str(a[1]))
print("End X: " + str(a[len(a)-1]))
print("Start X - End X: "+ str(a[0] - a[len(a) - 1]))
print("Start X - End X / 32: "+ str((a[0] - a[len(a) - 1])/32))
print("Count: ")
# print((a[0] - a[len(a) - 1])/ 728)
print(count)
# Prepare data
#data={'X': a, 'Y':b}

#1.291um = 1 pix
#1 um = 1/1.291 pix
#5 um = 5 * 1/1.291 pix


zeroXEncoderCount = 6791390
zeroYEncoderCount = 9740754

swathXStartEncoderCount =  a[0]
swathXEndEncoderCount = a[len(a) - 1]
swathXStartWC = (zeroXEncoderCount - swathXStartEncoderCount)/32
swathXEndWC = (zeroXEncoderCount - swathXEndEncoderCount)/32

# swathL = -150895.697
# swathT = -30866.036386489868
# swathR = 151819.491
# swathB = -36067.513065338135
# print("Swath Left:")
# print(swathL)
# print("Swath Right:")
# print(swathR)
# print("Swath Top:")
# print(swathT)
# print("Swath Bottom:")
# print(swathB)


# 0 - 6791390
# 1 - 6791358

# 0 - 9740754
# 1 - 9740722


# 150500 - 1975390
# -150500 - 11607390


# 151819.491 - 1933166
# -150895.697 11620052





totalSwathWidth = abs(swathXStartWC) + abs(swathXEndWC)
print("Image Total Swath Width:" +str(totalSwathWidth))

perPixelSize  =  totalSwathWidth / height
print("Per Pixel Size:"+ str(perPixelSize))




prevEncoderCount = a[0]
startPixelX = 0;
endPixelX = 0;
startPixelZ = 0;



for pix in range(1, len(a) - 1):
    distance =  a[pix] - prevEncoderCount 
    prevEncoderCount = a[pix]
    distanceInMicrons = distance/32
   # print(distanceInMicrons)
    distanceInPixels = distanceInMicrons/perPixelSize
  #  print(distanceInPixels)
    endPixelX = endPixelX + distanceInPixels
    endPixelX = round(endPixelX)
    
    #print(round(endPixelX))
    startPixelX = endPixelX

print(endPixelX)    
 
    
w, h = width, endPixelX
data = np.zeros((h, w, 3), dtype=np.uint8)

#data[200:256, 0:width] = [255, 0, 0] # red patch in upper left
prevEncoderCount = a[0]
startPixelX = 0;
endPixelX = 0;
startPixelZ = 0;  


for pix in range(1, len(a) - 1):
    distance =  a[pix] -  prevEncoderCount 
    prevEncoderCount = a[pix]
    distanceInMicrons = distance/32
   # print(distanceInMicrons)
    distanceInPixels = distanceInMicrons/perPixelSize
  #  print(distanceInPixels)
    endPixelX = endPixelX + distanceInPixels
    endPixelX = round(endPixelX)
    
    #print(round(endPixelX))
    z = max(0,b[pix])
    z = min(25000, z)
    z = 25000 - z
    z = z/25000 
    z = z * 255
    data[startPixelX: endPixelX, 0: width] = [z , 0 ,  0 ]
    startPixelX = endPixelX



img = Image.fromarray(data, 'RGB')
#img.save('E:\\DL\\5X_center_dies_MOI_items\\out.png')
#img.show()
print(img.size)
img = img.resize((width,height), Image.ANTIALIAS)
print(endPixelX)
print(img)
print(im)



import math
import os


outdir = "E:\\DL\\5X_center_dies_MOI_items\\out"
upper = 0
left = 0
slice_size = 4352
slices = int(math.ceil(height/slice_size))

count = 1
for slice in range(slices):
    print(count)
    #if we are at the end, set the lower bound to be the bottom of the image
    if count == slices:
        lower = height
    else:
        lower = int(count * slice_size)  
    #set the bounding box! The important bit     
    bbox = (left, upper, width, lower)
    working_slice = im.crop(bbox)
    image_8bit = cv2.convertScaleAbs(np.asarray(working_slice))
    image_8 = Image.fromarray(image_8bit)
    working_slice2 = img.crop(bbox)
    upper += slice_size
    #save the slice
    working_slice.save(os.path.join(outdir, name + "_"+str(count)+".png"))
    image_8.save(os.path.join(outdir, name + "_"+str(count)+"_ver.png"))
    working_slice2.save(os.path.join(outdir, name + "_"+str(count)+"_foc.png"))
    count +=1
    
    
    
    
    
# im_crop = im.crop((0, 0, 4352, 50000))
# im_crop.save('E:\\DL\\5X_center_dies_MOI_items\\im.png');
# np_frame = np.array(im.getdata())