#!/usr/bin/python3
#
# Extracts and processes the metadata of images for a given sol.
# Pulls from remote.
# NOTE: MSL manifest 2.0 links (to image metadata manifests) are broken before sol 1246.
#

# Library imports
import json
import requests
import boto3 # AWS

# marsrover-pipeline imports
import missions.spacecraft as spacecraft
import manifest
import util

class SolMetadata:
	def __init__(self,spacecraft,sol):
		self.sc = spacecraft
		
		# Attempt to find the sol in the local metadata first
		# If not there, check remote.
		# If still not there, oops...
		manif = manifest.Manifest(self.sc)
		self.masterMd = manif.getSolMetadata(sol)
		if self.masterMd == {}:
			manif.getRemoteManifest()
			self.masterMd = manif.getSolMetadata(sol)
		if self.masterMd == {}:
			self.initStatus = False
			return

		# Try to get the individual image manifest.
		# If not successful, exit with failure.
		req = requests.get(self.masterMd['url'])
		if req.status_code != 200:
			self.initStatus = False
			return
		
		# If successful, go ahead and parse the json:
		self.imageMd = req.json()
		
		# If we got here, yay, success!!
		self.initStatus = True

	# Check master manifest timestamp against sol manifest timestamp
	# Return True if sol manifast is same time as master, False if newer. 
	# Older doesn't make sense ever, but will return True...
	def checkManifestTimes(self):
		if util.cmptime(self.imageMd['last_manifest_update'],self.masterMd['last_manifest_update']):
			return False
		else:
			return True

	# Return the number of images for the given sol
	# This is per data product, not per frame!
	def getNumImages(self):
		return self.masterMd['num_images']

	# Grab the observations for a sol per instrument
	# Returns all obs in a list
	# Argument is string representation of instrument (i.e. 'pancam')
	def getInstrumentObs(self,inst):
		return self.imageMd[self.sc['instruments'][inst]]

	# Push the manifest to our s3 bucket
	# Should be able to do this without intermediate file by following method.
	def putSolOnBucket(self):
		s3 = boto3.resource('s3')
		dataBucket = s3.Object('marsroversio.data','latest_sols/' + self.sc['mission'] + '/images_sol' + str(self.masterMd['sol']) + '.json')
		dataBucket.put(Body=json.dumps(self.imageMd))

if __name__ == '__main__':
	print("TESTING MODULE: sol_metadata.py")
	l = SolMetadata(spacecraft.MERB,2000) # In local MF at test time
	print("Local:")
	print(l.sc)
	print(l.masterMd)
	print(l.initStatus)
	print(l.imageMd['last_manifest_update'])
	print(l.checkManifestTimes())
	print(l.getNumImages())
	print(l.getInstrumentObs('pancam'))
	r = SolMetadata(spacecraft.MERB,4991) # Not in local MF at test time
	print("Remote:")
	print(r.sc)
	print(r.masterMd)
	print(r.initStatus)
	print(r.imageMd['last_manifest_update'])
	print(r.checkManifestTimes())
	print(r.getNumImages())
	print(r.getInstrumentObs('navcam'))
	r.putSolOnBucket()
	x = SolMetadata(spacecraft.MERA,4000) # Poor Spirit died @ 2209 so this will fail.
	print("Failure:")
	print(x.sc)
	print(x.masterMd)
	print(x.initStatus)

