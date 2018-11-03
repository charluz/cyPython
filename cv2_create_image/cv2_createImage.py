#!/usr/bin/python

'''
Reference : https://stackoverflow.com/questions/9710520/opencv-createimage-function-isnt-working
'''

import cv2  # Not actually necessary if you just want to create an image.
import numpy as np

def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

# Create new blank 300x300 red image
width, height = 300, 300

red = (255, 0, 0)
image = create_blank(width, height, rgb_color=red)
cv2.imwrite('red.jpg', image)

'''
width = 320
height = 240
blank_image = np.zeros((height,width,3), np.uint8)


blank_image[:,0:0.5*width] = (255,0,0)      # (B, G, R)
blank_image[:,0.5*width:width] = (0,255,0)
'''
