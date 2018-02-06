#!/usr/bin/python3
#
# Handles checking the NASA public image manifest against the locally stored one.
# NOTE: MSL manifest 2.0 is currently broken before sol 1246.
#

# Library imports
import os
import json
import requests

# marsrover-pipline imports
import spacecraft
import util

class Manifest:
	def __init__(self, spacecraft):
		self.sc = spacecraft
		self.remoteMf = None
		self.recentSols = []
		self.toUpdate = []

		# Pull in locally cached image manifest here
		conf = json.load(open(os.path.expanduser('~/.marsroverio'),'r'))
		self.localMfPath = conf['manifest_path'][self.sc['mission']] + 'image_manifest.json'
		self.localMf = json.load(open(self.localMfPath,'r'))

	# Pull in the remote manifest
	def getRemoteManifest(self):
		remoteMfUrl = self.sc['raws_prefix'] + self.sc['image_manifest']
		req = requests.get(remoteMfUrl)

		# Check for success first:
		if req.status_code != 200:
			return False
		
		# If success, snag the json, decode, and return success.
		self.remoteMf = req.json()
		return True

	# Check for newness of manifest
	# Returns -1 for error, 0 for local is same or newer, 1 for remote is newer.
	def checkManifestTimes(self):
		status = -1

		# First ensure that we got the remote manifest
		if self.remoteMf is None:
			if not self.getRemoteManifest():
				return status

		# We're gonna check both the update time and the latest image time.
		# Just to be sure, honestly.
		if util.cmptime(self.remoteMf['last_manifest_update'],self.localMf['last_manifest_update']):
			status = 1
		elif util.cmptime(self.remoteMf['most_recent_image'],self.localMf['most_recent_image']):
			status = 1
		else:
			status = 0

		return status
	
	# Replace the locally cached manifest with the (presumably new) remote manifest.
	# Returns True if the write happened, False if remoteMf was not populated yet.
	def replaceManifest(self):
		if self.remoteMf is not None:
			with open(self.localMfPath,'w') as outfile:
				outfile.write(json.dumps(self.remoteMf, indent=2))
			return True
		else:
			return False

	# Make list of most recent sols (to push metadata to s3 to avoid unnecessary database hits.)
	# (Specifically, if we go Dynamo, keeping the most recent sols on s3 helps avoid hot keys.)
	def findRecentSols(self):
		latest = self.remoteMf['latest_sol']
		self.recentSols = list(range(latest,latest-10,-1)) # Calling it 10 sols.
	
	# Make list of sols that have updated metadata compared to previous manifest
	# This will let us only update the sols that need updating.
	def findUpdatedSols(self):
		oldManifTime = self.localMf['last_manifest_update']
		for sol in self.remoteMf['sols']:
			if util.cmptime(sol['last_manifest_update'],oldManifTime):
				self.toUpdate.append(sol['sol'])
	
	# Return a dictionary of metadata for a given sol - really just the bit of json for that sol.
	# No good way to do except iterating...
	# Also, since we know some sols are missing (grrr...), handle that.
	def getSolMetadata(solNum):
		for sol in self.remoteMf['sols']:
			if sol['sol'] == solNum:
				return sol

		return {} # If not in data, return empty dict.

if __name__ == "__main__":
	print("TESTING MODULE: manifest.py")
	m = Manifest(spacecraft.MERB)
	print(m.sc['scid'])
	print(m.localMf['latest_sol'])
	m.getRemoteManifest()
	print(m.checkManifestTimes())
	m.findRecentSols()
	print(m.recentSols)
	print("DONE.")

