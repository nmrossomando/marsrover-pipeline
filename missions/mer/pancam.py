#!/usr/bin/python3
#
# Instrument data handler for MER's Pancam instrument
# Given an observation block (pcam_images array from json manifest):
#	- Characterizes each observation (i.e. what filters used?)
#	- Can create false colors of L257 observations
#	- Can dump said false colors onto s3, and update s3 false color manifest
#
# Possible future expansion:
#	- Mosaic-ing observations in a given sequence
#	- True color approximations from 13F observations
#	- Anaglyph stereo from L2R2 observations
#

# Library imports
import os
import json
import requests
import cv2
import numpy as np

import missions.spacecraft as spacecraft
import missions.mer.image_utils as image_utils

class Pancam:
	def __init__(self, image_block, sol):
		self.initStatus = True
		self.obsImages = {} # Checked when it may not have been inited yet, so do that here

		# In MER images, the first character of the id (filename) of an image is serial number (MER1 = Oppy)
		missionid = image_block[0]['id'][0]
		if missionid == '1':
			self.sc = spacecraft.MERB
		elif missionid == '2':
			self.sc = spacecraft.MERA
		else:
			self.sc = None
			self.initStatus = False

		# Also make sure this is a Pancam:
		instid = image_block[0]['id'][1]
		if instid == 'P':
			pass
		else:
			self.initStatus = False

		self.images = image_block
		self.sol = sol
	
	# Check if good init:
	def checkInitStatus(self):
		return self.initStatus

	# Get the number of observations on a sol - not images, observations.
	def getNumObs(self):
		return len(self.images)

	# Get "id" of each observation - the prefix of the filename of the first image
	def getObsIds(self):
		ids = []
		for frame in self.images:
			ids.append(frame['id'])

		self.ids = ids # set this internally too.
		return ids

	# Get single observation frame by observation id
	def getObs(self,obsId):
		frame = {}

		# Search observation frames for the obsId
		# End search when found and assigned
		for f in self.images:
			if f['id'] == obsId:
				frame = f
				break

		# If obs is not found, will return an empty dict
		# Otherwise, return will be dict for observation frame
		return frame
	
	# Get the sequence ID of a given observation.
	# Since the obsid is a filename, this actually doesn't need any of the data from within the class
	def getSeqId(self,obsId):
		return obsId[18:23]
	
	# Get the Pancam filters used in the observation.
	def getObsFilters(self,obsId):
		filters = []
		frame = {}

		# First get the frame by obsId
		frame = self.getObs(obsId)

		# Exit if frame not found...
		if frame == {}:
			return []

		# Go through images in frame and get each filter.
		for im in frame['images']:
			eye = im['imageid'][-4]
			filt = im['filter_number']
			filters.append(eye+filt)

		return filters
	
	# Load each image in a given observation from s3
	# Returns False for failure, True for success
	def loadObsImages(self,obsId):
		frame = {}
		self.obsImages = {}
		self.activeObs = obsId # Set which observation the current images are from

		# Get frame by obsId
		frame = self.getObs(obsId)

		# Exit if frame not found
		if frame == {}:
			return False

		# For each image in the frame...
		for im in frame['images']:
			filterPos = im['imageid'][-4:-2] # Get filter eye & pos
			
			req = requests.get(im['url']) # Pull down the image from merpublic bucket
			if req.status_code != 200: # If it fails, a "valid" url died, so fail method
				return False

			# Read image into numpy array (i.e. OpenCV image!)
			self.obsImages[filterPos] = np.asarray(bytearray(req.content), dtype='uint8')
			self.obsImages[filterPos] = cv2.imdecode(self.obsImages[filterPos], cv2.IMREAD_GRAYSCALE)
		
		# At this point return success!
		return True

	# Check if any current images are partials - return filter position of all partials
	def checkPartialImages(self):
		partials = []

		# First check if there is an observation to check; return empty otherwise.
		if self.obsImages == {}:
			return []
		
		# Now go through images and use util funtion to test for partials:
		for key,val in self.obsImages.items():
			if image_utils.checkPartial(val):
				partials.append(key)

		return partials
	
	# Create a false color image using one filter for each channel.
	# Usually this involves the L2, L5, and L7 filters, can occasionally be L456.
	# Args are string filter identifier (i.e. "L2"); filters must be from same eye, left or right
	# Will reject if different eyes or requested filters are unavailable (or partial).
	# Returns True if image created and False otherwise; image added to obsImages dict.
	def makeFalseColor(self,redFilter,greenFilter,blueFilter):
		colorId = ""
		# Check for same eye in all images, and set eye in ID if good.
		if (redFilter[0] == greenFilter[0]) and (redFilter[0] == blueFilter[0]):
			colorId = redFilter[0]
		else:
			return False

		# Now check for existence and completeness of requested frames
		if (redFilter not in self.obsImages) or (redFilter in self.checkPartialImages()):
			return False
		elif (greenFilter not in self.obsImages) or (greenFilter in self.checkPartialImages()):
			return False
		elif (blueFilter not in self.obsImages) or (blueFilter in self.checkPartialImages()):
			return False
		else:
			# If all good, finish the identifier:
			colorId = colorId + redFilter[1] + greenFilter[1] + blueFilter[1]

		# Now for the easy part (yay OpenCV): Merge the images.
		imArray = [self.obsImages[blueFilter], self.obsImages[greenFilter], self.obsImages[redFilter]] # Note: OpenCV uses BGR instead of RGB for some reason. "Legacy."
		self.obsImages[colorId] = cv2.merge(imArray)

		return True

	# Cache generated images locally.
	# Uses path in .marsroverio config file.
	# Return True if success and False if failure
	def saveGenObsImages(self):
		conf = json.load(open(os.path.expanduser('~/.marsroverio'),'r'))
		localImageDir = conf['images_path'] + self.sc['mission'] + '/' + str(self.sol) + '/'
		# Check for directory's existence. If it doesn't exist, create.
		if not os.path.isdir(localImageDir):
			if os.path.isfile(localImageDir[:-1]): # Cut the '/' for this check
				return False
			else:
				os.makedirs(localImageDir)

		# Save images. Not the best algorithm to detect which are generated, but eh.
		# This doesn't just look for a L257 so we can accomodate other color sets and future other products.
		nonGen = self.getObsFilters(self.activeObs)
		for key,val in self.obsImages.items():
			if key not in nonGen:
				cv2.imwrite(localImageDir + self.activeObs + key + '.jpg',val)

		return True

if __name__ == "__main__":
	print("TESTING MODULE: pancam.py")
	import metadata.sol_metadata as solmd
	SD = solmd.SolMetadata(spacecraft.MERB,4995)
	PC = Pancam(SD.getInstrumentObs('pancam'),4995)
	print(PC.checkInitStatus())
	print(PC.getNumObs())
	oids = PC.getObsIds()
	print(oids)
	print(PC.getSeqId(oids[0]))
	for oid in oids:
		print(PC.getObsFilters(oid))
	print(PC.getObsFilters('fake_id'))
	print(PC.loadObsImages(oids[1]))
	print(PC.checkPartialImages())
	print(PC.makeFalseColor("L2","R2","L7"))
	print(PC.makeFalseColor("R3","R2","R1"))
	print(PC.makeFalseColor("L2","L5","L7"))
	print(PC.saveGenObsImages())
	print("DONE.")

