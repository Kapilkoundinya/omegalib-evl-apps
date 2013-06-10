# Super simple panorama viewer app
from collections import *
from euclid import *
from omega import *
from omegaToolkit import *
from cyclops import *
from pano import *

#--------------------------------------------------------------------------------------------------
# Panorama Data Container
class PanoInfo:
    def __init__(self, type, name, file, lstr="L", rstr="R", horizStartDegrees=0, vertStartDegrees=0, horizSpanDegrees=360, vertSpanDegrees=180, height=4, offset=Vector3(0, 0, 0) ):
        self.type = type
        self.name = name
        self.file = file
        self.lstr = lstr
        self.rstr = rstr
        self.horizStartDegrees = horizStartDegrees
        self.vertStartDegrees = vertStartDegrees
        self.horizSpanDegrees = horizSpanDegrees
        self.vertSpanDegrees = vertSpanDegrees
        self.height = height
        self.offset = offset

#--------------------------------------------------------------------------------------------------
# List of panos
panos = [
	PanoInfo(PanoType.Cylinder, "galaxy", "panorama/ants/ssc2008-11a15.jpg"),
	PanoInfo(PanoType.Sphere, "Blue Mounds", "panorama/pano/Blue-Mounds-8-%1%-360x180-16-8.jpg"),
	PanoInfo(PanoType.Sphere, "Luxor Temple", "panorama/pano/LuxorTempleFirstCourtNight-%1%-360x180-16-8.jpg"),
	PanoInfo(PanoType.Sphere, "Madaen Saleh", "panorama/pano/Madaen-Saleh-Rock-Formation-%1%-360x180-16-8.jpg"),
	PanoInfo(PanoType.Cylinder, "Ants 1", "panorama/ants/AntsView1_%1%.jpg", lstr="left", rstr="right", height=6, offset=Vector3(0, -10, 0)),
	PanoInfo(PanoType.Cylinder, "Ants 2", "panorama/ants/AntsView2_%1%.jpg", lstr="left", rstr="right", height=6, offset=Vector3(0, -10, 0)),
	PanoInfo(PanoType.Cylinder, "Ants 3", "panorama/ants/AntsView3_%1%.jpg", lstr="left", rstr="right", height=6, offset=Vector3(0, -10, 0)),
	PanoInfo(PanoType.Cylinder, "Ants 4", "panorama/ants/AntsView4_%1%.jpg", lstr="left", rstr="right", height=6, offset=Vector3(0, -10, 0)),
	PanoInfo(PanoType.Cylinder, "Ants 5", "panorama/ants/AntsView5_%1%.jpg", lstr="left", rstr="right", height=6, offset=Vector3(0, -10, 0)),
	PanoInfo(PanoType.Cylinder, "Ants 6", "panorama/ants/AntsView6_%1%.jpg", lstr="left", rstr="right", height=4, offset=Vector3(0, -10, 0)),
	PanoInfo(PanoType.Sphere, "WI Capitol", "panorama/pano/WI-Capitol-L-360x180-16-8.jpg"),
	PanoInfo(PanoType.Sphere, "Mars", "panorama/pano/PIA16101.jpg")
	]

#--------------------------------------------------------------------------------------------------
frontPano = Pano()
backPano = Pano()

cam = getEngine().getDefaultCamera()

mm = MenuManager.createAndInitialize()
menu = mm.createMenu("main")
mm.setMainMenu(menu)

i = 0
for panoInfo in panos:
	mit = menu.addItem(MenuItemType.Button)
	mit.setText(panoInfo.name)
	mit.setCommand("setActivePano(" + str(i) + ")")
	i+=1

#--------------------------------------------------------------------------------------------------
def setActivePano(panoId):
    global frontPano
    global backPano
    tmp = frontPano
    frontPano = backPano
    backPano = tmp
    frontPano.loadPano(panos[panoId].type, panos[panoId].file, panos[panoId].lstr, panos[panoId].rstr)
    if(panos[panoId].type == PanoType.Cylinder):
		frontPano.setCylinderOffsetAndHeight(panos[panoId].offset, panos[panoId].height)
    frontPano.setAlpha(0.0)

#--------------------------------------------------------------------------------------------------
def onUpdate(frame, t, dt):
	global frontPano
	global backPano
	if(dt < 0.2):
		alpha = frontPano.getAlpha()
		alpha += (1.0 - alpha) * dt * 5
		if(alpha > 0.99): alpha = 1.0
		frontPano.setAlpha(alpha)
		backPano.setAlpha(1.0 - alpha)

setUpdateFunction(onUpdate)
setActivePano(0)
		