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
import json
import requests
import boto3
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
	print("DONE.")

