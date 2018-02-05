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

class Manifest:
	def __init__(self, spacecraft):
		self.sc = spacecraft
		
		conf = json.load(open(os.path.expanduser('~/.marsroverio'),'r'))
		self.localMf = conf['manifest_path'][self.sc['mission']] + 'image_manifest.json'

if __name__ == "__main__":
	print("TESTING MODULE: manifest.py")
	m = Manifest(spacecraft.MERB)
	print(m.sc['scid'])
	print(m.localMf)
	print("DONE.")

