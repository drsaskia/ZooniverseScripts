#!/usr/bin/python
import sys, os, subprocess, re
import argparse

usage = """
JOTTER Jadas Output Tif daTa ExporteR
viruszoo.py -s VH-HCF_20kx -f 1 -l 50 
eman2 must be in user's path. 
"""

parser = argparse.ArgumentParser(description=usage)
# example command 
#> viruszoo.py Tomogram OR coordmode Inputfile (type?) Boxsize outputfile [binning]
parser.add_argument("-s", "--session", "--ses", "-S", action="store", default="none", dest="session", 
					help="Required. Input file name. First input file name in the session you're processing.")
parser.add_argument("-f", "--first", "--fi", "-F", action="store", dest="first", type=int,
					help="Optional. If present will start processing from this image, useful to continue interrupted session")
parser.add_argument("-l", "--last", "--la", "-L", action="store", dest="last", type=int,
					help="Optional. If present will start processing from this image, useful to continue interrupted session")
args = parser.parse_args()

def inputChecker(args):
	"""check sensible input has been given"""
	# Check session has been correctly given, files exist and are correct type
	print args
	if args.session == "none":
		response = "No input files given. Please check input."
		print response
		sys.exit()
	else: session = args.session
	min_image = int(args.first)
	max_image = int(args.last)
	return session, min_image, max_image
	
def countImages(session):
	"""Counts number of images and number of frames for a session"""
#	loop over images from 1 to check what the highest existing number is. NEEDS SEQUENTIAL NUMBERS
	max_image = 1
	image_exists = os.path.exists(str(session)+'_'+str(max_image).zfill(4)+'_frameImage1.mrc')
	while image_exists == True:
		max_image += 1
		image_exists = os.path.exists(str(session)+'_'+str(max_image).zfill(4)+'_frameImage1.mrc')
	else:
		max_image -= 1
	max_frame = 0
	frame_exists = os.path.exists(str(session)+'_0001_'+str(max_frame)+'.mrc')
	while frame_exists == True:
		max_frame += 1
		frame_exists = os.path.exists(str(session)+'_0001_'+str(max_frame)+'.mrc')
	else:
		max_frame -= 1
	return max_image, max_frame
	

def environCheck():
	"""Checks required programs are in PATH"""
	run = subprocess.Popen(['newstack', "--help"])
	success = run.wait()
	if success != 0:
		response = "Cannot find Imod!"
		print response
		sys.exit()
	return success
	
def virusChopper(session, image):
	"""Takes OneView image and chops it into smaller bits """
	infile = str(session)+'_'+str(image).zfill(4)+'.dm3'
	if os.path.isfile(infile) == True:
		for xcoord in 700,1600,2500,3396:
			for ycoord in 700,1600,2500,3396:
				outfile = str(session)+'_'+str(image).zfill(4)+'_'+str(xcoord)+'_'+str(ycoord)+'.png'
				clip = '--clip=1400,1400,'+str(xcoord)+','+str(ycoord)
				command = ['e2proc2d.py', infile, 'temp.png', clip]
				print command
				subprocess.call(command)#
				command2 = ['e2proc2d.py', 'temp.png', outfile, '--meanshrink=2']
				subprocess.call(command2)
#			print command
	else:  
		print "file " + infile + " does not exist. Skipping."
	return infile




#check = environCheck()
#args = parser.parse_args()
session, min_image, max_image = inputChecker(args)
print session, min_image, max_image
#pseudocode:
# determine number of images in session
# check options here
# if last_frame given 
# if last_frame > max_frame:
#	print: last_frame + " does not exist, using " +max_frame+ as last frame
#print "Found " +str(max_image)+ " images, with "+str(max_frame)+ " frames each."

#loop over images to chop them
#image = 155
for image in range(min_image,max_image+1):
	outfile = virusChopper(session, image)
		
	
	
	
	
	
	
	