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

import missions.spacecraft as sc

print(sc.MERB['name'])

