#!/usr/bin/python3
#
# Just some handy image utilities for all instruments.
# Uses OpenCV and Numpy
#

# Library imports
import cv2
import numpy as np

# Detect partial data products.
# MER images come down top to bottom, left to right, in distinct chunks.
# So checking if the bottom left corner of the image in question is solid black should
# be a decent check of a partial image.
# Return True if partial, False if otherwise
def checkPartial(image):
	# Check to see if image is large enough; our thumbnails are 64x64!
	# If that is the case, check against the whole image - likely it's either all or nothing at this size.
	height, width = image.shape[:2]
	if (height < 150) or (width < 150):
		templateImage = np.zeros((height,width,1), np.uint8)
		checkCorner = image
	else:
		templateImage = np.zeros((150,150,1), np.uint8) # 150 pixel square black area
		checkCorner = image[-151:-1, -151:-1] # Bottom right 150 x 150 area of image

	# Check for full match; if every single original pixel is solid black,
	# there's a preeeeetty good chance it's a partial.
	if (checkCorner == templateImage).all():
		return True
	else:
		return False

