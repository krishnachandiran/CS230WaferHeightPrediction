# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 15:41:05 2021

@author: smungi
"""
import imutils
import cv2
import json
import numpy as np
import csv
from PIL import Image, ImageFont, ImageDraw  

def generate_wafer(path, rows, cols):
    
    first = True
    
    for m in range(rows):
        
        list = []
        
        for n in range(cols):
            
            image = cv2.imread(path + '\\wafer_image_' + str((cols * m) +(n+1)) + '.png')
            #image = cv2.imread(path + '\\' + str((rows * m) +(n+1)) + '.png')
            if (m + 1) % 2 == 0:
                list.insert(0, image)
            else:
                list.append(image)
    
        vert = cv2.hconcat(list)
    
        if first == True:
            wfr = vert
            first = False
        else:
            wfr = cv2.vconcat([wfr, vert])
    
    cv2.imwrite(path+"/wafer.png", wfr)
    
def dieToDieRunner(die_h, die_w, st_w, care_areas, ex_zones, rows, cols, path):
    
    leftToRight = True 
    dieNum = 1;
    wafer = cv2.imread(path+"/wafer.png")
    mask = createCareAndExclusionMask(die_h, die_w, care_areas, ex_zones)
    for m in range(rows):  
        if(leftToRight):
            swap = range(cols)
        else:
            swap = reversed(range(cols))
        for n in swap:
            if n == 0:
                tX = (((n + 1) * st_w) + (n * die_w))
                tY = (((m + 1) * st_w) + (m * die_h))
                r1X = tX + die_w + st_w
                r1Y = tY
                r2X = r1X + die_w + st_w
                r2Y = tY
                dieToDie(die_h, die_w, st_w, care_areas, ex_zones, rows, cols, path, (r1X , r1Y) , (r2X, r2Y) , (tX, tY), wafer, mask,dieNum)
            elif n == (cols - 1):
                tX = (((n + 1) * st_w) + (n * die_w))
                tY = (((m + 1) * st_w) + (m * die_h))
                r1X = tX - die_w - st_w
                r1Y = tY
                r2X = r1X - die_w - st_w
                r2Y = tY
                dieToDie(die_h, die_w, st_w, care_areas, ex_zones, rows, cols, path, (r1X , r1Y) , (r2X, r2Y) , (tX, tY), wafer, mask,dieNum)
            else:
                tX = (((n + 1) * st_w) + (n * die_w))
                tY = (((m + 1) * st_w) + (m * die_h))
                r1X = tX - die_w - st_w
                r1Y = tY
                r2X = tX + die_w + st_w
                r2Y = tY
                dieToDie(die_h, die_w, st_w, care_areas, ex_zones, rows, cols, path, (r1X , r1Y) , (r2X, r2Y) , (tX, tY), wafer, mask,dieNum)
            dieNum += 1
        leftToRight = not leftToRight
                
                
           
def createCareAndExclusionMask(die_h, die_w, care_areas, ex_zones):
    
    mask = np.zeros((die_h, die_w, 1), np.uint8)

    for i in range(len(care_areas)) :
        
        (x,y) = (care_areas[i]['top_left']['x'], abs(care_areas[i]['top_left']['y'] - die_h + 1))
    
        (x_, y_) = (care_areas[i]['bottom_right']['x'], abs(care_areas[i]['bottom_right']['y'] - die_h + 1))
        
        mask = cv2.rectangle(mask, (x,y), (x_,y_), (255, 255, 255), -1)

    cv2.imwrite(path + "/mask1.png", mask)
    
    for i in range(len(ex_zones)) :
    
        (x, y) = (ex_zones[i]['top_left']['x'], abs(ex_zones[i]['top_left']['y'] - die_h + 1))
    
        (x_,y_) = (ex_zones[i]['bottom_right']['x'], abs(ex_zones[i]['bottom_right']['y'] - die_h + 1))

        mask = cv2.rectangle(mask, (x,y), (x_,y_), (0, 0, 0), -1)
    
    cv2.imwrite(path + "/mask2.png", mask)
    
    return mask;
    
    
    
def dieToDie(die_h, die_w, st_w, care_areas, ex_zones, rows, cols, path, ref1 , ref2 , target, wafer, mask, dieNum):
    

    
    ref1Img = wafer[ref1[1]: ref1[1] + die_h, ref1[0] : ref1[0] + die_w]
    ref2Img = wafer[ref2[1]: ref2[1] + die_h, ref2[0] : ref2[0] + die_w]
    targetImg = wafer[target[1]: target[1] + die_h, target[0] : target[0] + die_w]
    
    
    ref1G = cv2.cvtColor(ref1Img, cv2.COLOR_BGR2GRAY)
    ref2G = cv2.cvtColor(ref2Img, cv2.COLOR_BGR2GRAY)
    targetG = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY)

#    mean = np.mean(wafer)
    
# =============================================================================
#     grayA = cv2.threshold(grayA, mean, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#     grayB = cv2.threshold(grayB, mean, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#     grayC = cv2.threshold(grayC, mean, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# =============================================================================
    
# =============================================================================
#     threshA = cv2.threshold(grayA, mean, 255,cv2.THRESH_BINARY | cv2.THRESH_BINARY_INV)[1]
#     threshB = cv2.threshold(grayB, mean, 255,cv2.THRESH_BINARY | cv2.THRESH_BINARY_INV)[1]
#     threshC = cv2.threshold(grayC, mean, 255,cv2.THRESH_BINARY | cv2.THRESH_BINARY_INV)[1]
# =============================================================================

# =============================================================================
#     cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
#     cv2.resizeWindow("output", 400, 300)  
#     
#     cv2.imshow("output", grayB)
#     cv2.imshow("im", mask)
#     
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# =============================================================================
    
    sub1 = cv2.subtract(ref1G, targetG)

    cv2.imwrite(path + "/sub1.png", sub1)
    sub2 = cv2.subtract(ref2G, targetG)

    cv2.imwrite(path + "/sub2.png", sub2)
    cv2.absdiff(ref1G, targetG, sub1)
    cv2.absdiff(ref2G, targetG, sub2)
    sub1 = cv2.threshold(sub1, 10, 255, cv2.THRESH_BINARY)[1]
    sub1 = cv2.threshold(sub1, 10, 255, cv2.THRESH_BINARY)[1]
    
    cv2.imwrite(path + "/diffsub1.png", sub1)
    cv2.imwrite(path + "/diffsub2.png", sub2)
    
    
    
    fin = cv2.bitwise_and(sub1, sub2)
    cv2.imwrite(path + "/and.png", fin)
    fin = cv2.bitwise_and(fin, mask)
    cv2.imwrite(path + "/andwithmask.png", fin)
    

# =============================================================================
#     cv2.absdiff(threshA, threshB, sub1)
#     cv2.absdiff(threshC, threshB, sub2)
#     fin2 = cv2.bitwise_and(sub1, sub2)
#     fin2 = cv2.bitwise_and(fin2, mask)
#     
#     fin = cv2.bitwise_or(fin, fin2)
# =============================================================================
    (x,y) = (care_areas[0]['top_left']['x'], abs(care_areas[0]['top_left']['y'] - die_h + 1))

    (x_, y_) = (care_areas[0]['bottom_right']['x'], abs(care_areas[0]['bottom_right']['y'] - die_h + 1))

    (ex, ey) = (ex_zones[0]['top_left']['x'], abs(ex_zones[0]['top_left']['y'] - die_h + 1))

    (ex_,ey_) = (ex_zones[0]['bottom_right']['x'], abs(ex_zones[0]['bottom_right']['y'] - die_h + 1))


    locations = cv2.findNonZero(fin)
    cv2.rectangle(targetG, (x, y), (x_, y_), (255,0,0), 1)
    cv2.rectangle(targetG, (ex, ey), (ex_, ey_), (255,0,0), 1)
 #   cv2.imwrite(path+"/2die.png",targetG)
    cv2.rectangle(ref1G, (x, y), (x_, y_), (255,0,0), 1)
    cv2.rectangle(ref1G, (ex, ey), (ex_, ey_), (255,0,0), 1)
 #   cv2.imwrite(path+"/1die.png",ref1G)
    cv2.rectangle(ref2G, (x, y), (x_, y_), (255,0,0), 1)
    cv2.rectangle(ref2G, (ex, ey), (ex_, ey_), (255,0,0), 1)
#    cv2.imwrite(path+"/3die.png",ref2G)
    fp = open(path + "/../internal/" + "AlgoSolution.csv", "a+")
    for i in locations:
        cv2.circle(targetG, (i[0][0],i[0][1]), radius=0, color=(0, 0, 255), thickness=-1)
        i[0][1] = abs(i[0][1] - die_h + 1)
        fp.write("{},{},{}\n".format(dieNum,i[0][0],i[0][1]))
    
    fp.close()
#    fp.write('DI %d %d\n' % (dieNum, len(dieCareSet))) 

            
    
    print(len(locations))
   # print(locations)
        
# =============================================================================
#         if i[0][1] == 11 or i[0][0] == 11:
#             print(i)
# =============================================================================
        
# =============================================================================
#     print(locations)
# =============================================================================
    output = cv2.resize(targetG, (1000, 800))
    cv2.imwrite(path+"/"+str(dieNum)+"AlgoSolution.png",output)

    backtorgb = cv2.cvtColor(targetG,cv2.COLOR_GRAY2RGB)
    with open(path+"/../internal/output.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(dieNum) :
                    (x,y) = (int(row[1]), abs(int(row[2]) - die_h + 1))
                    cv2.circle(backtorgb, (x,y), radius=0, color=(0, 255, 0), thickness=-1)
    output = cv2.resize(backtorgb, (1000, 800))
    cv2.imwrite(path+"/"+str(dieNum)+"GenSolution.png",output)
                    

                



#    cv2.imshow("1", grayB)
#    cv2.imshow("im", imB)
#    cv2.imshow("2", cv2.bitwise_not(grayB))
#    cv2.imshow("3", fin)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
# =============================================================================
#     cv2.imwrite("A.png", imA)
#     cv2.imwrite("B.png", imB)
#     cv2.imwrite("C.png", imC)
#     cv2.imwrite("dif.png", fin)
# =============================================================================
    
if __name__ == '__main__':

# =============================================================================
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--width', '-width', nargs="?", type=int, default=500)
#     parser.add_argument('--height', '-height' , nargs="?", type=int, default= 600)
#     parser.add_argument('--noOfDieRows', '-dr' , nargs="?", type=int, default= 2)
#     parser.add_argument('--noOfDieColumns', '-dc' , nargs="?", type=int, default= 5 )
#     parser.add_argument('--streetWidth', '-sw' , nargs="?", type=int, default= 10)
#     parser.add_argument('--outWidth', '-ow', nargs="?", type=int, default= 822 )
#     parser.add_argument('--outHeight', '-oh', nargs="?", type=int, default= 265 )
#     parser.add_argument('--swathHeight', '-swh', nargs="?", type=int, default= 123 )
#     parser.add_argument('--swathWidth', '-sww', nargs="?", type=int, default= 256 )
#     parser.add_argument('--path', '-pth', nargs="?", type=str, default=r'D:\UniversityEngagement\simple_hexagons\data')
#     parser.add_argument('--outputFilename', '-o', nargs='?', type=str, default='generated_wafer.png')
#     args = parser.parse_args()
# =============================================================================
    
# =============================================================================
#     path = args.path
# 
#     rs = args.noOfDieRows
#     cs = args.noOfDieColumns
#     
#     die_h = args.height
#     die_w = args.width
#     
#     st_w = args.streetWidth
#     
#     swth_h = args.swathHeight
#     swth_w = args.swathWidth
# =============================================================================
    path = r'C:\Work\CY21 University Engagement\Wafer_Swath_Generator\Sample4'
    path_json = path+ '\data\input.json'
    path = path + '\data'
    
    with open(path_json) as f:
        args = json.load(f)
    
    rs = args['die']['rows']
    cs = args['die']['columns']
    
    die_h = args['die']['height']
    die_w = args['die']['width']
    
    st_w = args['street_width']
    
    care_areas = args['care_areas']
    exclusion_zones = args['exclusion_zones']

    img1 = Image.open(path +"/wafer_image_1.png")
    (swth_w , swth_h) = img1.size
   

    #TODO get swath size on own
    rows = ((die_h * rs) + (st_w * (rs + 1))) / swth_h
    cols = ((die_w * cs) + (st_w * (cs + 1))) / swth_w
    
    rows = int(rows)
    cols = int(cols)


    
    generate_wafer(path, rows, cols)
    
    dieToDieRunner(die_h, die_w, st_w, care_areas, exclusion_zones, rs, cs, path)