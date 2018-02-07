#!/usr/bin/python3
#
# Extracts and processes the metadata of images for a given sol.
# Pulls from remote.
# NOTE: MSL manifest 2.0 links (to image metadata manifests) are broken before sol 1246.
#

# Library imports
import os
import json
import requests

# marsrover-pipeline imports
import spacecraft

class SolMetadata:
	def __init__(self,spacecraft,sol):
		self.sc = spacecraft


