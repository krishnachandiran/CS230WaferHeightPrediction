# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:49:32 2021

@author: krishnr
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:31:13 2021

@author: smungi
"""
import numpy as np
import cv2

import numpy as np
import cv2
from PIL import Image, ImageChops




img1 = np.zeros((512,512,3), np.uint8)
img2 = np.zeros((512,512,3), np.uint8)
img3 = np.zeros((512,512,3), np.uint8)

cv2.circle(img1,(130,353), 600, (128,128,128), -1)
cv2.circle(img2,(30,353), 600, (128,128,128), -1)
cv2.circle(img3,(430,353), 600, (128,128,128), -1)

cv2.circle(img1,(130,353), 100, (255,255,255), -1)
cv2.circle(img2,(130,353), 100, (255,255,255), -1)
cv2.circle(img3,(130,353), 100, (255,255,255), -1)


cv2.circle(img1,(130+20,353+23), 3, (130,130,130), -1)
#cv2.circle(img2,(130-10,353-53), 3, (130,130,130), -1)
cv2.circle(img2,(130,353+70), 3, (135,135,135), -1)
cv2.circle(img3,(130,353+70), 3, (130,130,130), -1)


cv2.circle(img1,(13,353), 3, (50,50,50), -1)
cv2.circle(img2,(134,33), 3, (50,50,50), -1)
cv2.circle(img3,(300,370), 3, (50,50,50), -1)

path = r'C:\Work\CY21 University Engagement\Wafer_Swath_Generator\CheckingKrishna'
grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
grayC = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)


cv2.imwrite(path + "/1.png", grayA);
cv2.imwrite(path + "/2.png", grayB);
cv2.imwrite(path + "/3.png", grayC);


img1 = Image.open(path +"/1.png")
img2 = Image.open(path +"/2.png")
img3 = Image.open(path +"/3.png")

sub1 = ImageChops.difference(img2, img1)
sub2 = ImageChops.difference(img2, img3)


sub1.save(path + "/diffsub1.png")
sub2.save(path + "/diffsub2.png")


#sub1 = cv2.subtract(grayA, grayB)
#cv2.imwrite(path + "/aasub1.png", sub1)
#sub2 = cv2.subtract(grayC, grayB)
#cv2.imwrite(path + "/asub2.png", sub2)
#cv2.absdiff(grayA, grayB, sub1)
#cv2.absdiff(grayC, grayB, sub2)

#cv2.imwrite(path + "/diffsub1.png", sub1)
#cv2.imwrite(path + "/diffsub2.png", sub2)

sub1 = cv2.imread(path + "/diffsub1.png")
sub2 = cv2.imread(path + "/diffsub2.png")


fin = cv2.bitwise_and(sub1, sub2)

sub2 = ImageChops.difference(img2, img3)

fin = cv2.cvtColor(fin, cv2.COLOR_BGR2GRAY)
cv2.imwrite(path + "/fin.png", fin)
#fin = cv2.bitwise_and(fin, mask)
#cv2.imwrite(path + "/andwithmask.png", fin)

locations = cv2.findNonZero(fin)

print(len(locations))

