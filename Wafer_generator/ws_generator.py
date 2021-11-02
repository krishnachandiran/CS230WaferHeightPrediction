# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:36:17 2021

@author: krishnachandiran.r
"""
from queue import LifoQueue
from PIL import Image, ImageFont, ImageDraw  
import numpy as np
from geopatterns import GeoPattern
from random import choice
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import os
import enum
from PIL import Image
from base64 import decodestring, b64decode
from io import BytesIO, StringIO
import random
import math
from tilings import *
import sys
import logging
import os
import time
import multiprocessing
from functools import partial

class SwathDir(enum.Enum):
   Left = 1
   Right = 2

def generate_wafer_image(width, height, ndr , ndc, streetWidth, userId , swathWidth, swathHeight, pattern, patternAttr, impuritiesPerDie, careAreas, exclusionZones):
    
    if not os.path.exists(userId):
        os.makedirs(userId)
    dirname = os.path.dirname(__file__)
    datafolder = os.path.join(dirname, userId + '/data')
    if not os.path.exists(datafolder):    
        os.mkdir(datafolder) 
    datafolder = os.path.join(dirname, userId + '/internal')
    if not os.path.exists(datafolder):    
        os.mkdir(datafolder) 
        
           
    die = generate_die(width, height, pattern, patternAttr, userId)
    if os.path.exists(userId + "/internal/" + "output.csv"):    
        os.remove(userId + "/internal/" + "output.csv")
    #Move repeated Calculations here
    dieNum = 1
    
    waferWidth = (((ndc + 1) * streetWidth) + (ndc * width))
    waferHeight = (((ndr + 1) * streetWidth) + (ndr * height))
   
    width, height = die.size
    dieAreaSize = width * height
    totalCareAreaSize = calculate_total_care_area_size(careAreas)
    
    totalCareAreaRatio = totalCareAreaSize / dieAreaSize
    
#   numOfImpInTotalCareArea = totalCareAreaRatio * impuritiesPerDie
    numOfImpInTotalCareArea = totalCareAreaRatio * impuritiesPerDie
    numOfImpInDieArea = impuritiesPerDie - numOfImpInTotalCareArea
    print(" Num of imp in Care area "+ str(numOfImpInTotalCareArea))
    print(" Num of imp in Die area "+ str(numOfImpInDieArea))
    print(" Wafer width "+ str(waferWidth))
    print(" Wafer height "+ str(waferHeight))
    
    starttime = time.time()
    
    dieRows = Image.new('RGB', (waferWidth , waferHeight) , (0, 0, 0))
    leftToRight = True    
    
    for j in range(1, ndr+1):
        dieColumns = Image.new('RGB', (waferWidth , (2 * streetWidth + height )) , (0, 0, 0))
        for i in range(1, ndc+1):
            dieTemp = die.copy()
            generate_impure_die_file(dieTemp, dieNum, userId, numOfImpInDieArea, numOfImpInTotalCareArea , totalCareAreaSize, careAreas, exclusionZones)
            dieNum += 1
            if leftToRight:
                dieColumns.paste(dieTemp, ( i * streetWidth   + ((i - 1 ) * width)   , streetWidth))     
            else:
                k = ndc+1-i
                dieColumns.paste(dieTemp, ( k * streetWidth   + ((k - 1 ) * width)   , streetWidth))
#        dieColumns.save("dieRow"+str(dieNum)+".png") 
        dieRows.paste(dieColumns,  (0 ,((j - 1) * streetWidth) +  ((j - 1 ) * height))) 
        leftToRight = not leftToRight
#    dieRows.save(userId + "/data/wafer"  + str('.png'))

    print('This took {} seconds'.format(time.time() - starttime))
    
    starttime = time.time()
    
    generate_swath_images(dieRows,swathWidth, swathHeight, userId)
    
    print('That took {} seconds'.format(time.time() - starttime))
    return (waferWidth , waferHeight)


def generate_impure_die_file(die, dieNum , userId, numOfImpInDieArea, numOfImpInTotalCareArea, totalCareAreaSize , careAreas, exclusionZones):
    print("\nDie-Number " + str(dieNum))
    width, height = die.size
    dieCareSet = set()
    dieExclusionSet = set()
    dieAllSet = set()

    for careArea in careAreas:
        careSet, allSet, exclusionSet = add_impurities_per_care_area(die, totalCareAreaSize , careArea , numOfImpInTotalCareArea, exclusionZones)
        dieCareSet.update(careSet)
        dieAllSet.update(allSet)
        dieExclusionSet.update(exclusionSet)
    dieCareSetNum = len(dieCareSet)
    dieExclusionSetNum = len(dieExclusionSet)
    dieAllSetNum = len(dieAllSet)
    print("  Total-cares-care "+ str( dieCareSetNum ))
    print("  Total-cares-exc "+ str( dieExclusionSetNum ))
    print("  Total-cares-all "+ str( dieAllSetNum ))
    
    for i in range(int(numOfImpInDieArea)): 
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        dieAllSet.add((x, height  - 1 - y))
        if(is_inside_care_areas(x, y, careAreas) and (not is_inside_exclusion_zones(x, y , exclusionZones))):
            dieCareSet.add((x, y))
        else:
            dieExclusionSet.add((x , y))
            

#   Uncomment following 4 lines for debugging die numbering
#    draw = ImageDraw.Draw(die)  
#    font= ImageFont.truetype("C:\Work\CY21 University Engagement\Wafer_Swath_Generator\cute_little_sheep\Cute Little Sheep.ttf", 2000) 
#    text = str(dieNum)
#    draw.text((5, 5), text, fill ="red", font = font, align ="right")  
    
    dieCareSetNum = len(dieCareSet) - dieCareSetNum
    dieExclusionSetNum = len(dieExclusionSet) - dieExclusionSetNum
    dieAllSetNum = len(dieAllSet) - dieAllSetNum
    print("  Total-out-care "+ str( dieCareSetNum))
    print("  Total-out-exc "+ str( dieExclusionSetNum ))
    print("  Total-out-all "+ str(dieAllSetNum))
    print("  Final-care "+str( len(dieCareSet)))
    print("  Final-exc "+str(len(dieExclusionSet)))
    print("  Final-all "+ str(len(dieAllSet)))
    make_impure(die, dieAllSet)
    fp = open(userId + "/internal/" + "output.csv", "a+")
#    fp.write('DI %d %d\n' % (dieNum, len(dieCareSet))) 
    for x in dieCareSet:
        fp.write("{},{},{}\n".format(dieNum,x[0],x[1]))
#    fp.write('\n')
    fp.close()

 
    
    
    
def add_impurities_per_care_area(die, totalCareAreaSize, careArea, numOfImpInTotalCareArea, exclusionZones):
    width, height = die.size
    area = calculate_care_area_size(careArea)
    ratio = area/totalCareAreaSize
    numOfImp = ratio * numOfImpInTotalCareArea
    top_left = careArea['top_left']
    bottom_right = careArea['bottom_right']        
    careSet = set()
    allSet = set()
    exclusionSet = set()
    for i in range(int(numOfImp)): 
        x = random.randint(top_left['x'], bottom_right['x'])
        y = random.randint(bottom_right['y'], top_left['y'])
        allSet.add((x, height  - 1 - y))
        if(not is_inside_exclusion_zones(x , y , exclusionZones)):
            careSet.add((x, y))  
        else:
            exclusionSet.add((x,y))
    print("     care-sub "+ str(len(careSet)))
    print("     exc-sub "+ str(len(exclusionSet)))
    print("     all-sub "+ str(len(allSet)))

    return careSet, allSet , exclusionSet

    
def make_impure(die , imageSet ):
    pixels = die.load()
    for i in imageSet:
        pixels[i] = (100, 200, 400)  
 #   pixels = die.convert('RGB').load()
 #   for i in allSet:
 #       print(i)
 #       pixels[i] = (255, 255, 255) 
 #   die.show()
   
    
def is_inside_care_areas(x, y , careAreas):
    for careArea in careAreas:
        if(is_inside_care_area(x, y, careArea)):
            return True
    return False

def is_inside_care_area(x, y , careArea):
    top_left = careArea['top_left']
    bottom_right = careArea['bottom_right']
    return x >= top_left['x'] and x <= bottom_right['x'] and y <= top_left['y'] and y >= bottom_right['y']
    
def is_inside_exclusion_zones(x , y , exclusionZones):
    for zone in exclusionZones:
        if(is_inside_exclusion_zone(x, y , zone)):
            return True
    return False
    
def is_inside_exclusion_zone(x, y, exclusionZone):
    top_left = exclusionZone['top_left']
    bottom_right = exclusionZone['bottom_right']
    return x >= top_left['x'] and x <= bottom_right['x'] and y <= top_left['y'] and y >= bottom_right['y']

def calculate_total_care_area_size(careAreas):
    area = 0
    for i in careAreas:
        area += calculate_care_area_size(i)
    return area
        
    
    
def calculate_care_area_size(careArea):
    top_left = careArea['top_left']
    bottom_right = careArea['bottom_right']
    width = bottom_right['x'] - top_left['x']
    height = top_left['y'] - bottom_right['y']
    return width * height
    
# def generate_swath_images(wafer, swathWidth, swathHeight, userId):

#     direction = SwathDir.Right;
#     x = 0;
#     y = swathHeight;
#     wW, wH = wafer.size
#     numOfImages =( wW / swathWidth) * (wH / swathHeight)
#     print(numOfImages)
#     i = 1;
#     while(True):
#         if(direction == SwathDir.Right):
#             if(isValid(wW,wH, x + swathWidth , y)):
#                 temp = wafer.crop((x , y - swathHeight , x + swathWidth , y));
#                 temp.save(userId + "/data/" + str(i)+".png");
#                 x = x + swathWidth
#                 i += 1;
#             elif(isValid(wW,wH,x , y + swathHeight)):
#                 y = y + swathHeight
#                 direction = SwathDir.Left
#             else:
#                 break;
#         elif (direction == SwathDir.Left):
#             if(isValid(wW,wH,x - swathWidth , y)):
#                 temp = wafer.crop((x - swathWidth , y - swathHeight  , x , y ));
#                 temp.save(userId + "/data/" + str(i)+".png");
#                 x = x - swathWidth
#                 i += 1;
#             elif(isValid(wW,wH,x , y + swathHeight)):
#                 y = y + swathHeight
#                 direction = SwathDir.Right
#             else:
#                 break;
                
                
def generate_swath_image(swathNum, swathWidth, swathHeight, userId):
        temp =  Image.new('RGB', (swathWidth , swathHeight) , (0, 0, 0));
        temp.save(userId + "/data/" + str(swathNum)+".png");
        # x = x + swathWidth
        # i += 1;
    
    
def generate_swath_images(wafer, swathWidth, swathHeight, userId):

    direction = SwathDir.Right;
    x = 0;
    y = swathHeight;
    wW, wH = wafer.size
    numOfImages =( wW / swathWidth) * (wH / swathHeight)
    print(int(numOfImages))
    
   # processes = []
    
    # for i in range(1,int(numOfImages)):
    #     p = multiprocessing.Process(target=generate_swath_image, args=(i, swathWidth, swathHeight,userId))
    #     processes.append(p)
    #     p.start()
        
    # for process in processes:
    #     process.join()
    
    # pool = multiprocessing.Pool()
    # prod_x=partial(generate_swath_image, swathWidth=swathWidth, swathHeight=swathHeight, userId=userId)
    # pool.map(prod_x, range(1,int(numOfImages)))
    # pool.close()
    
    
    i = 1;
    while(True):
        if(direction == SwathDir.Right):
            if(isValid(wW,wH, x + swathWidth , y)):
                temp =  Image.new('RGB', (swathWidth , swathHeight) , (0, 0, 0));
                temp.save(userId + "/data/" + str(i)+".png");
                x = x + swathWidth
                i += 1;
            elif(isValid(wW,wH,x , y + swathHeight)):
                y = y + swathHeight
                direction = SwathDir.Left
            else:
                break;
        elif (direction == SwathDir.Left):
            if(isValid(wW,wH,x - swathWidth , y)):
                temp =  Image.new('RGB', (swathWidth , swathHeight) , (0, 0, 0));
                temp.save(userId + "/data/" + str(i)+".png");
                x = x - swathWidth
                i += 1;
            elif(isValid(wW,wH,x , y + swathHeight)):
                y = y + swathHeight
                direction = SwathDir.Right
            else:
                break;


        
        
        
def isValid(waferWidth , waferHeight, x , y):
    return x >= 0 and y >= 0 and x <= waferWidth and y <= waferHeight
    
def generate_die(width, height, pattern, patternAttr, userId):
    simple = ['simple_lines', 'simple_squares', 'simple_triangles', 'simple_hexagons']
    geoPatterns = [ 'bricks',
            'hexagons',
            'overlapping_circles',
            'overlapping_rings',
            'plaid',
            'plus_signs',
            'rings',
            'sinewaves',
            'squares',
            'triangles',
            'xes']
    if pattern == 'complex_maze':
        die = generate_cropped_maze(width, height)
    elif pattern == 'quasi_crystal':
        die = generate_quasi_patterns(width, height)
    elif pattern in simple:
        die = generate_simple_pattents(width, height, pattern, patternAttr)
    elif pattern in geoPatterns:
        die = generate_geo_pattern(width, height, pattern, userId)

    die.save("die.png") 
    return die

def generate_simple_pattents(width, height, pattern, patternAttr):
    scaling = patternAttr['scaling']
    if pattern == 'simple_lines':
        die = draw_tiling(generate_lines, width, height, scaling)
    elif pattern == 'simple_squares':
        die = draw_tiling(generate_squares, width, height, scaling)
    elif pattern == 'simple_triangles':
        die = draw_tiling(generate_triangles, width, height, scaling)
    elif pattern == 'simple_hexagons':
        die = draw_tiling(generate_hexagons, width, height, scaling)
    return die
    
def generate_geo_pattern(width , height, pattern, userId):

    pattern =  GeoPattern(userId, pattern)
    drawing = svg2rlg(StringIO(pattern.svg_string))
    im = renderPM.drawToPIL(drawing)
        # The width and height of the background tile
    bg_w, bg_h = im.size

    # Creates a new empty image, RGB mode, and size 1000 by 1000
    new_im = Image.new('RGB', (width,height))

    # The width and height of the new image
    w, h = new_im.size

    # Iterate through a grid, to place the background tile
    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            # Change brightness of the images, just to emphasise they are unique copies
            #im = Image.eval(im, lambda x: x+(i+j)/1000)
    
            #paste the image at location i, j:
            new_im.paste(im, (i, j))

    #new_im.show()
     #   renderPM.drawToFile(drawing, "Pic.png")
     #   image = Image.open(BytesIO(png))
    return new_im


def generate_quasi_patterns(width, height):
    imgx = width; imgy = height
    image = Image.new("RGB", (imgx, imgy))
    pixels = image.load()
    
    f = random.random() * 40 + 10 # frequency
    p = random.random() * math.pi # phase
    n = random.randint(10, 20) # of rotations
    
    for ky in range(imgy):
        y = float(ky) / (imgy - 1) * 4 * math.pi - 2 * math.pi
        for kx in range(imgx):
            x = float(kx) / (imgx - 1) * 4 * math.pi - 2 * math.pi
            z = 0.0
            for i in range(n):
                r = math.hypot(x, y)
                a = math.atan2(y, x) + i * math.pi * 2.0 / n
                z += math.cos(r * math.sin(a) * f + p)
            c = int(round(255 * z / n))
            pixels[kx, ky] = (c, c, c) # grayscale
    return image


def generate_cropped_maze(width, height):
    die = generate_maze(int(width/2) + 1, int(height/2) + 1)
    fW, fH = die.size
    die = die.crop((1, 1 ,fW - 2  , fH - 2))
    return die
    
    
def generate_maze(width, height):
    maze = Image.new('RGB', (2*width + 1, 2*height + 1), 'black')
    pixels = maze.load()
    
    # Create a path on the very top and bottom so that it has an entrance/exit
    pixels[1, 0] = (255, 255, 255)
    pixels[-2, -1] = (255, 255, 255)
    
    stack = LifoQueue()
    cells = np.zeros((width, height))
    cells[0, 0] = 1
    stack.put((0, 0))

    while not stack.empty():
        x, y = stack.get()

        adjacents = []
        if x > 0 and cells[x - 1, y] == 0:
            adjacents.append((x - 1, y))
        if x < width - 1 and cells[x + 1, y] == 0:
            adjacents.append((x + 1, y))
        if y > 0 and cells[x, y - 1] == 0:
            adjacents.append((x, y - 1))
        if y < height - 1 and cells[x, y + 1] == 0:
            adjacents.append((x, y + 1))

        if adjacents:
            stack.put((x, y))

            neighbour = choice(adjacents)
            neighbour_on_img = (neighbour[0]*2 + 1, neighbour[1]*2 + 1)
            current_on_img = (x*2 + 1, y*2 + 1)
            wall_to_remove = (neighbour[0] + x + 1, neighbour[1] + y + 1)

            pixels[neighbour_on_img] = (255, 255, 255)
            pixels[current_on_img] = (255, 255, 255)
            pixels[wall_to_remove] = (255, 255, 255)

            cells[neighbour] = 1
            stack.put(neighbour)

    return maze


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', '-width', nargs="?", type=int, default=400)
    parser.add_argument('--height', '-height' , nargs="?", type=int, default= 200)
    parser.add_argument('--noOfDieRows', '-dr' , nargs="?", type=int, default= 5)
    parser.add_argument('--noOfDieColumns', '-dc' , nargs="?", type=int, default= 10 )
    parser.add_argument('--streetWidth', '-sw' , nargs="?", type=int, default= 10)
    parser.add_argument('--outWidth', '-ow', nargs="?", type=int, default= 822 )
    parser.add_argument('--outHeight', '-oh', nargs="?", type=int, default= 265 )
    parser.add_argument('--userId', '-o', nargs='?', type=str, default='user1')
    parser.add_argument('--userId', '-o', nargs='?', type=str, default='user1')
    parser.add_argument('--userId', '-o', nargs='?', type=str, default='user1')
    args = parser.parse_args()

    size = (args.width, args.height) if args.height else (args.width, args.width)
    noOfDieRows = args.noOfDieRows
    noOfDieColumns = args.noOfDieColumns
    userId = args.userId
    swathWidth = args.outWidth 
    swathHeight = args.outHeight
    streetWidth = args.streetWidth
    
    generate_wafer_image(*size, noOfDieRows, noOfDieColumns, streetWidth, userId, swathWidth, swathHeight, pattern, patternAttr,  impuritiesPerDie, careAreas, exclusionZones )
    
  