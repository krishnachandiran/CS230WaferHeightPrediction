#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Generate regular tilings of the plane with Pillow.

Diagrams and background to this code are on my blog:
http://alexwlchan.net/2016/10/tiling-the-plane-with-pillow/
"""

from __future__ import division

import math

from PIL import Image, ImageDraw
import numpy as np
from numpy import random

CANVAS_WIDTH  = 400
CANVAS_HEIGHT = 400
SCALING = 50


def _scale_coordinates(generator, image_width, image_height, SCALING):
    side_length = SCALING
    scaled_width = int(image_width / side_length) + 2
    scaled_height = int(image_height / side_length) + 2

    for coords in generator(scaled_width, scaled_height):
        yield [(x * side_length, y * side_length) for (x, y) in coords]


def generate_unit_squares(image_width, image_height):
    """Generate coordinates for a tiling of unit squares."""
    # Iterate over the required rows and cells.  The for loops (x, y)
    # give the coordinates of the top left-hand corner of each square:
    #
    #      (x, y) +-----+ (x + 1, y)
    #             |     |
    #             |     |
    #             |     |
    #  (x, y + 1) +-----+ (x + 1, y + 1)
    #
    for x in range(image_width):
        for y in range(image_height):
            yield [(x, y), (x + 1, y), (x + 1, y+1), (x, y+1)]


def generate_squares(*args, **kwargs):
    """Generate coordinates for a tiling of squares."""
    return _scale_coordinates(generate_unit_squares, *args, **kwargs)



"""
    Created for CY21UE
"""
def generate_unit_lines(image_width, image_height):
    """Generate coordinates for a tiling of unit lines."""
    #
    #      (x, y) +-----+ (x + 1, y)
    #
    for x in range(image_width):
        for y in range(image_height):
            yield [(x, y), (x + 1, y), (x, y), (x + 1, y)]



"""
    Created for CY21UE
"""
def generate_lines(*args, **kwargs):
    """Generate coordinates for a tiling of lines."""
    return _scale_coordinates(generate_unit_lines, *args, **kwargs)


def generate_unit_triangles(image_width, image_height):
    """Generate coordinates for a tiling of unit triangles."""
    # Our triangles lie with one side parallel to the x-axis.  Let s be
    # the length of one side, and h the height of the triangle.
    #
    # The for loops (x, y) gives the coordinates of the top left-hand corner
    # of a pair of triangles:
    #
    #           (x, y) +-----+ (x + 1, y)
    #                   \   / \
    #                    \ /   \
    #    (x + 1/2, y + h) +-----+ (x + 3/2, y + h)
    #
    # where h = sin(60°) is the height of an equilateral triangle with
    # side length 1.
    #
    # On odd-numbered rows, we translate by (s/2, 0) to make the triangles
    # line up with the even-numbered rows.
    #
    # To avoid blank spaces on the edge of the canvas, the first pair of
    # triangles on each row starts at (-1, 0) -- one width before the edge
    # of the canvas.
    h = math.sin(math.pi / 3)

    for x in range(-1, image_width):
        for y in range(int(image_height / h)):

            # Add a horizontal offset on odd numbered rows
            x_ = x if (y % 2 == 0) else x + 0.5

            yield [(x_, y * h), (x_+1, y * h), (x_+0.5, (y+1) * h)]
            yield [(x_+1, y * h), (x_+1.5, (y+1) * h), (x_+0.5, (y+1) * h)]

def generate_triangles(*args, **kwargs):
    """Generate coordinates for a tiling of triangles."""
    return _scale_coordinates(generate_unit_triangles, *args, **kwargs)


def generate_unit_hexagons(image_width, image_height):
    """Generate coordinates for a regular tiling of unit hexagons."""
    # Let s be the length of one side of the hexagon, and h the height
    # of the entire hexagon if one side lies parallel to the x-axis.
    #
    # The for loops (x, y) give the coordinate of one coordinate of the
    # hexagon, and the remaining coordinates fall out as follows:
    #
    #                     (x, y) +-----+ (x + 1, y)
    #                           /       \
    #                          /         \
    #         (x - 1/2 y + h) +           + (x + 3/2, y + h)
    #                          \         /
    #                           \       /
    #                 (x, y + 2h) +-----+ (x + 1, y + 2h)
    #
    # In each row we generate hexagons in the following pattern
    #
    #         /‾‾‾\   /‾‾‾\   /‾‾‾\
    #         \___/   \___/   \___/
    #
    # and the next row is offset to fill in the gaps. So after two rows,
    # we'd have the following pattern:
    #
    #         /‾‾‾\   /‾‾‾\   /‾‾‾\
    #         \___/‾‾‾\___/‾‾‾\___/‾‾‾\
    #             \___/   \___/   \___/
    #
    # There are offsets to ensure we fill the entire canvas.

    # Half the height of the hexagon
    h = math.sin(math.pi / 3)

    for x in range(-1, image_width, 3):
        for y in range(-1, int(image_height / h) + 1):

            # Add the horizontal offset on every other row
            x_ = x if (y % 2 == 0) else x + 1.5

            yield [
                (x_,        y * h),
                (x_ + 1,    y * h),
                (x_ + 1.5, (y + 1) * h),
                (x_ + 1,   (y + 2) * h),
                (x_,       (y + 2) * h),
                (x_ - 0.5, (y + 1) * h),
            ]


def generate_hexagons(*args, **kwargs):
    """Generate coordinates for a tiling of hexagons."""
    return _scale_coordinates(generate_unit_hexagons, *args, **kwargs)


"""
    Modified for CY21UE
"""
def draw_tiling(coord_generator, width , height, scaling=50, patternBgr='plain', base_color= 0):


    CANVAS_WIDTH = width
    CANVAS_HEIGHT = height
    SCALING = scaling
    col = 128 + base_color
    im = Image.new('L', size=(CANVAS_WIDTH, CANVAS_HEIGHT),color = col)
    if patternBgr == 'gradient' : 
       
        img_arr = np.array(im) 
        
        size = CANVAS_WIDTH * CANVAS_HEIGHT
        print(size)
        
        gau_arr_1d = random.normal(loc=0, scale=3, size=CANVAS_WIDTH * CANVAS_HEIGHT)
        gau_arr_2d = np.reshape(gau_arr_1d, (CANVAS_HEIGHT, CANVAS_WIDTH )) 
        
        
        final = np.add(gau_arr_2d , img_arr)
        
        im = Image.fromarray(final)
        im = im.convert("L")

    for shape in coord_generator(CANVAS_WIDTH, CANVAS_HEIGHT, SCALING):
        ImageDraw.Draw(im).polygon(shape, outline='white')
        
 #   im.save("die.png")
    return im
 


if __name__ == '__main__':
   # draw_tiling(generate_squares,  500 , 600 )
   # draw_tiling(generate_triangles,500 , 600)
    draw_tiling(generate_hexagons,  500 , 600)
