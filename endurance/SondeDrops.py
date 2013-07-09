# A measuring tape tool with movable ends.
from math import *
from euclid import *
from omega import *
from omegaToolkit import *
from cyclops import *

import csv

sondeDropsFile = "SondeBasedBathymetry28-Mar-2013.csv"
sondeDropsDir = "D:/Workspace/omegalib/apps/endurance/data"

sondeDropsPath = sondeDropsDir + "/" + sondeDropsFile

sondeDrops = LineSet.create()
sondeDrops.setEffect('colored -e white')

def createSondeDrop(data):
	stname = data[0]
	stx = float(data[2])
	sty = float(data[3])
	# UTM >> melthole coords
	stx -= 1371377
	sty -= 435670
	depth = float(data[4])
	print("Station " + stname + " X + " + str(stx) + " Y = " + str(sty))
	stline = sondeDrops.addLine()
	stline.setStart(Vector3(stx, sty, 0))
	stline.setEnd(Vector3(stx, sty, depth))
	stline.setThickness(2)
	stname = Text3D.create('fonts/arial.ttf', 2, stname)
	stname.setFacingCamera(getDefaultCamera())
	stname.setPosition(Vector3(stx, sty, 1))
	stname.setFixedSize(True)
	stname.setFontSize(20)
	sondeDrops.addChild(stname)
	
def load():
	with open(sondeDropsPath, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		headerLine = True
		for row in reader:
			if(not headerLine):
				createSondeDrop(row)
			else:
				headerLine = False
