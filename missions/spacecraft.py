#!/usr/bin/python3
#
# Contains general spacecraft info that'll be useful in several places. Probably.
#

# Oppy
MERB = {'raws_prefix' : 'http://merpublic.s3.amazonaws.com/oss/merb/',
		'image_manifest' : 'images/image_manifest.json',
		'name' : 'Opportunity',
		'mission' : 'merb',
		'scid' : 253,
		'spacecraft' : 'MER1',
		'instruments' : {'pancam' : 'pcam_images','navcam' : 'ncam_images','fhaz' : 'fcam_images','rhaz' : 'rcam_images','mi' : 'mi_images','mobidd' : 'course_plot_images'}}

# Spirit
# :sadparrot:
MERA = {'raws_prefix' : 'http://merpublic.s3.amazonaws.com/oss/mera/',
		'image_manifest' : 'images/image_manifest.json',
		'name' : 'Spirit',
		'mission' : 'mera',
		'scid' : 254,
		'spacecraft' : 'MER2',
		'instruments' : {'pancam' : 'pcam_images','navcam' : 'ncam_images','fhaz' : 'fcam_images','rhaz' : 'rcam_images','mi' : 'mi_images','mobidd' : 'course_plot_images'}}

# That other rover
# Okay, okay, calm down MSL folks...
# Curiosity
MSL =  {'raws_prefix' : 'http://msl-raws.s3.amazonaws.com/',
		'image_manifest' : 'images/image_manifest.json',
		'name' : 'Curiosity',
		'mission' : 'msl',
		'scid' : 76,
		'spacecraft' : 'MSL',
		'instruments' : {'chemcam' : 'ccam_images','fhaz' : 'fcam_images','rhaz' : 'rcam_images','navcam' : 'ncam_images','mastcam_left' : 'mastcam_left_images','mastcam_right' : 'mastcam_right_images','mahli' : 'mahli_images','mardi' : 'mardi_images'}}

# I have no idea if we'll be able to incorporate INSIGHT, but reserving.
NSYT = {'raws_prefix' : 'Coming Sooner',
		'image_manifest' : 'Coming Sooner',
		'name' : 'InSight',
		'mission' : 'nsyt',
		'scid' : 189,
		'spacecraft' : 'NSYT',
		'instruments' : {'idc' : 'idc','icc' : 'icc'}} # Instruments correct, naming notional!

# Reserving! Update this in a few years...
# And yes, we know the scid already.
M20 =  {'raws_prefix' : 'Coming Soon(TM)',
		'image_manifest' : 'Coming Soon(TM)',
		'name' : 'MARS-2020',
		'mission' : 'm20',
		'scid' : 168,
		'spacecraft' : 'M2020',
		'instruments' : {}} # Many cams, 2 years to fill in.

if __name__ == '__main__':
	print("TESTING MODULE: spacecraft.py")
	print("Opportunity: ")
	print("    Manifest URL:")
	print("    " + MERB['raws_prefix'] + MERB['image_manifest'])
	print("    Spacecraft Info:")
	print("    " + MERB['name'] + " " + str(MERB['scid']) + " " + MERB['spacecraft'] + MERB['mission'])
	print("Spirit: ")
	print("    Manifest URL:")
	print("    " + MERA['raws_prefix'] + MERA['image_manifest'])
	print("    Spacecraft Info:")
	print("    " + MERA['name'] + " " + str(MERA['scid']) + " " + MERA['spacecraft'] + MERA['mission'])
	print("Curiosity: ")
	print("    Manifest URL:")
	print("    " + MSL['raws_prefix'] + MSL['image_manifest'])
	print("    Spacecraft Info:")
	print("    " + MSL['name'] + " " + str(MSL['scid']) + " " + MSL['spacecraft'] + MSL['mission'])
	print("Mars 2020: ")
	print("    Manifest URL:")
	print("    " + M20['raws_prefix'] + M20['image_manifest'])
	print("    Spacecraft Info:")
	print("    " + M20['name'] + " " + str(M20['scid']) + " " + M20['spacecraft'] + M20['mission'])
	print("InSight: ")
	print("    Manifest URL:")
	print("    " + NSYT['raws_prefix'] + NSYT['image_manifest'])
	print("    Spacecraft Info:")
	print("    " + NSYT['name'] + " " + str(NSYT['scid']) + " " + NSYT['spacecraft'] + NSYT['mission'])
	print("DONE.")

