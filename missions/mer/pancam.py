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

import missions.spacecraft as spacecraft

class Pancam:
	def __init__(self, image_block, sol):
		self.initStatus = True

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
	
	# Get the sequence ID of a given observation.
	# Since the obsid is a filename, this actually doesn't need any of the data from within the class
	def getSeqId(self,obsId):
		return obsId[18:23]
	
	# Get the Pancam filters used in the observation.
	def getObsFilters(self,obsId):
		filters = []
		frame = None

		# First get the frame by obsId
		for f in self.images:
			if f['id'] == obsId:
				frame = f
				break

		# Exit if frame not found...
		if frame is None:
			return

		# Go through images in frame and get each filter.
		for im in frame['images']:
			eye = im['imageid'][-4]
			filt = im['filter_number']
			filters.append(eye+filt)

		return filters

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
	print("DONE.")

