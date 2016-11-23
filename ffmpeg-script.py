# ffmpeg-encoder-script
#
# Recurses through a directory to encode all video files using ffmpeg
# 
# Place this file in the top level of the directory you want to encode
#
# Note: Video files to be encoded should contain the string  "RAW" in 
# their name or be within a subfolder that contains the string "RAW". 
#
# author: mrracine


import os, re, subprocess

def printLogo():
	print("###############################\n" +
	      "##                           ##\n" +
	      "##    ffmpeg-script          ##\n" +
	      "##                           ##\n" +
	      "##    author: Mike Racine    ##\n" +
	      "##                           ##\n" +
	      "###############################\n")
	print("Encoding files in {}".format(os.getcwd()))

def encode(fIn, fOut):
	subprocess.call(["ffmpeg", "-i", fIn,
                         "-map", "0",
                         "-map_metadata", "0",
                         "-c:v", "libx264", "-crf", "20",
                         "-c:a", "libfdk_aac", "-vbr", "5",
                         "-c:a:0", "copy",
                         "-c:s", "copy",
                         fOut])

if __name__ == "__main__":

	printLogo()

	ffmpegDefaultCmd = "ffmpeg -i "
	rawToken = "RAW"
	encodeToken = "ENCODED"

	for dirpath, dirnames, filenames in os.walk(os.curdir):

		# Check for directories containing raw files, encode to parent dir
		if rawToken in dirpath:
			for f in filenames:
				encode(f, os.pardir + os.sep + f)
			break

		# Check for raw files, encode in same dir
		for f in filenames:
			if rawToken in f:
				fName, ext = os.path.splitext(f)
				fName.strip(rawToken)
				fName.strip()
				encode(f, fName + ext)
			else:
				fName, ext = os.path.splitext(f)
				encode(f, fName + encodeToken + ext)

