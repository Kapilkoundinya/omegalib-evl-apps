import sys
from math import *
from euclid import *
from omega import *
from cyclops import *
from pointCloud import *
from measuringTape import *

import DivePointCloud
import PlaneRubberbandSelector

scene = getSceneManager()
scene.addLoader(TextPointsLoader())
scene.addLoader(BinaryPointsLoader())

setNearFarZ(1, 100000)

pointCloudPath = "D:/Workspace/omegalib/apps/endurance/data"

#------------------------------------------------------------------------------
# models to load
diveNames = {
		'dive09-13': pointCloudPath + "/bonney-09-dive13.xyzb",
		'dive09-17': pointCloudPath + "/bonney-09-dive17.xyzb",
		'dive09-18': pointCloudPath + "/bonney-09-dive18.xyzb",
		'dive09-19': pointCloudPath + "/bonney-09-dive19.xyzb",
		'dive09-20': pointCloudPath + "/bonney-09-dive20.xyzb",
		'dive09-21': pointCloudPath + "/bonney-09-dive21.xyzb",
		'dive09-22': pointCloudPath + "/bonney-09-dive22.xyzb",
		'dive09-23': pointCloudPath + "/bonney-09-dive23.xyzb",
		'dive09-24': pointCloudPath + "/bonney-09-dive24.xyzb",
		'dive09-25': pointCloudPath + "/bonney-09-dive25.xyzb",
		'dive09-26': pointCloudPath + "/bonney-09-dive26.xyzb",
		'dive09-27': pointCloudPath + "/bonney-09-dive27.xyzb"}

diveColors = {
		'dive09-13': Color('#ff0000'),
		'dive09-17': Color('#00ff00'),
		'dive09-18': Color('#0000ff'),
		'dive09-19': Color('#ffff00'),
		'dive09-20': Color('#ff00ff'),
		'dive09-21': Color('#00ffff'),
		'dive09-22': Color('#800000'),
		'dive09-23': Color('#008000'),
		'dive09-24': Color('#000080'),
		'dive09-25': Color('#808000'),
		'dive09-26': Color('#800080'),
		'dive09-27': Color('#008080')}
		
lake = SceneNode.create("lake")

dives = []

pointDecimation = 10

totalPoints = 0
fieldMin = Vector3(sys.float_info.max,sys.float_info.max, sys.float_info.max)
fieldMax = Vector3(-sys.float_info.max,-sys.float_info.max, -sys.float_info.max)

#------------------------------------------------------------------------------
# load dives
for name,model in diveNames.iteritems():
	dive = DivePointCloud.DivePointCloud(lake, name)
	dive.load(model, pointDecimation)
	dive.diveNode.getMaterial().setColor(diveColors[name], Color('black'))
	dives.append(dive)
	totalPoints += dive.diveInfo['numPoints']
	# update field bounds
	minr = dive.diveInfo['minR']
	maxr = dive.diveInfo['maxR']
	ming = dive.diveInfo['minG']
	maxg = dive.diveInfo['maxG']
	minb = dive.diveInfo['minB']
	maxb = dive.diveInfo['maxB']
	if(minr < fieldMin.x): fieldMin.x = minr
	if(ming < fieldMin.y): fieldMin.y = ming
	if(minb < fieldMin.z): fieldMin.z = minb	
	if(maxr > fieldMax.x): fieldMax.x = maxr
	if(maxg > fieldMax.y): fieldMax.y = maxg
	if(maxb > fieldMax.z): fieldMax.z = maxb

print("loaded points: " + str(totalPoints))
print("Field minimums: " + str(fieldMin))
print("Field maximums: " + str(fieldMax))

# Setup attribute bounds uniforms
DivePointCloud.minAttrib.setVector3f(fieldMin)
DivePointCloud.maxAttrib.setVector3f(fieldMax)

#------------------------------------------------------------------------------
# load additional models
lakeSonarMeshModel = ModelInfo()
lakeSonarMeshModel.name = "lake-sonar-mesh"
lakeSonarMeshModel.path = "/data/evl/febret/omegalib/appData/endurance/bonney-sonde-bathy.obj"
lakeSonarMeshModel.optimize = True
lakeSonarMeshModel.generateNormals = True
lakeSonarMeshModel.normalizeNormals = True
scene.loadModel(lakeSonarMeshModel)

lakeSondeDropsModel = ModelInfo()
lakeSondeDropsModel.name = "lake-sonde-drops"
lakeSondeDropsModel.path = "/data/evl/febret/omegalib/appData/endurance/bonney-sonde-drops.obj"
lakeSondeDropsModel.optimize = True
lakeSondeDropsModel.generateNormals = True
lakeSondeDropsModel.normalizeNormals = True
scene.loadModel(lakeSondeDropsModel)

# Create a scene object using the loaded model
#lake.setEffect("points")
#pointScale = lake.getMaterial().addUniform('pointScale', UniformType.Float)
#globalAlpha = lake.getMaterial().addUniform('globalAlpha', UniformType.Float)
#minDepth = lake.getMaterial().addUniform('unif_MinDepth', UniformType.Float)
#maxDepth = lake.getMaterial().addUniform('unif_MaxDepth', UniformType.Float)

lakeSonarMesh = StaticObject.create("lake-sonar-mesh")
lakeSonarMesh.setEffect("colored -e white -C -t | colored -d black -w -o -1000 -C -t")
lake.addChild(lakeSonarMesh)

lakeSondeDrops = StaticObject.create("lake-sonde-drops")
lakeSondeDrops.setEffect("colored -e #008000")
lakeSondeDrops.setScale(Vector3(1, 1, 1/6.0))
lake.addChild(lakeSondeDrops)

#minDepth.setFloat(10)
#maxDepth.setFloat(50.0)

#pointScale.setFloat(0.02)
#globalAlpha.setFloat(1.0)

pivot = SceneNode.create('pivot')
pivot.addChild(lake)
#lake.setPosition(-lake.getBoundCenter())
pivot.setPosition(Vector3(0, 2, -4))
pivot.setScale(Vector3(0.002, 0.002, 0.002))
pivot.pitch(radians(90))

# second light
light = Light.create()
light.setColor(Color(0.8, 0.8, 0.1, 1))
light.setAmbient(Color(0.2, 0.2, 0.2, 1))
light.setPosition(Vector3(0, 2, 0))
#light.setAmbient(Color(0.1, 0.1, 0.1, 1))
#light.setLightDirection(Vector3(0, -1, 0))
light.setEnabled(True)

getDefaultCamera().addChild(light)

scene.setBackgroundColor(Color('black'))

globalScale = 0.01
curScale = 0.001


mm = MenuManager.createAndInitialize()

#------------------------------------------------------------------------------
# dive list
divemnu = mm.getMainMenu().addSubMenu('dives')
for dive in dives:
	dbtn = divemnu.addButton(dive.name, 'setDiveVisible("' + dive.name + '", %value%)') 
	btn = dbtn.getButton()
	btn.setCheckable(True)
	btn.setChecked(True)
	btn.setImageEnabled(True)
	btn.setWidth(200)
	btn.getImage().setFillColor(diveColors[dive.name])
	btn.getImage().setFillEnabled(True)
	btn.getImage().setSize(Vector2(20,20))
	
def setDiveVisible(name, visible):
	for dive in dives: 
		if(dive.name == name): 
			dive.diveNode.setVisible(visible)

#------------------------------------------------------------------------------
# Sliders set the angle bounds
boundmnu = mm.getMainMenu().addSubMenu("Bounds")
anglelabel = boundmnu.addLabel("Angle")
angleminslider = boundmnu.addSlider(100, "setAngleBounds(%value%, anglemaxslider.getSlider().getValue())")
angleminslider.getSlider().setValue(0)
angleminslider.getWidget().setWidth(200)
anglemaxslider = boundmnu.addSlider(100, "setAngleBounds(angleminslider.getSlider().getValue(), %value%)")
anglemaxslider.getSlider().setValue(100)
anglemaxslider.getWidget().setWidth(200)

rangelabel = boundmnu.addLabel("Range")
rangeminslider = boundmnu.addSlider(100, "setRangeBounds(%value%, rangemaxslider.getSlider().getValue())")
rangeminslider.getSlider().setValue(0)
rangeminslider.getWidget().setWidth(200)
rangemaxslider = boundmnu.addSlider(100, "setRangeBounds(rangeminslider.getSlider().getValue(), %value%)")
rangemaxslider.getSlider().setValue(100)
rangemaxslider.getWidget().setWidth(200)
			

# Sets the angle bounds
def setAngleBounds(percMin, percMax):
	range = fieldMax.x - fieldMin.x
	min = fieldMin.x + range * percMin / 100
	max = fieldMin.x + range * percMax / 100
	curMinAttrib = DivePointCloud.minAttrib.getVector3f()
	curMaxAttrib = DivePointCloud.maxAttrib.getVector3f()
	curMinAttrib.x = min
	curMaxAttrib.x = max
	DivePointCloud.minAttrib.setVector3f(curMinAttrib)
	DivePointCloud.maxAttrib.setVector3f(curMaxAttrib)
	anglelabel.setText("Angle: %.1f" % min + "   %.1f" % max)
	
# Sets the range bounds
def setRangeBounds(percMin, percMax):
	range = fieldMax.y - fieldMin.y
	min = fieldMin.y + range * percMin / 100
	max = fieldMin.y + range * percMax / 100
	curMinAttrib = DivePointCloud.minAttrib.getVector3f()
	curMaxAttrib = DivePointCloud.maxAttrib.getVector3f()
	curMinAttrib.y = min
	curMaxAttrib.y = max
	DivePointCloud.minAttrib.setVector3f(curMinAttrib)
	DivePointCloud.maxAttrib.setVector3f(curMaxAttrib)
	rangelabel.setText("Range: %.1f" % min + "   %.1f" % max)
	
# call both functions to reset bounds and bound labels
setAngleBounds(0, 100)
setRangeBounds(0, 100)

#------------------------------------------------------------------------------
# other menu items
mm.getMainMenu().addLabel("Point Size")
ss = mm.getMainMenu().addSlider(10, "onPointSizeSliderValueChanged(%value%)")
ss.getSlider().setValue(4)
ss.getWidget().setWidth(200)

mm.getMainMenu().addLabel("Point Transparency")

ss = mm.getMainMenu().addSlider(11, "onAlphaSliderValueChanged(%value%)")
ss.getSlider().setValue(10)
ss.getWidget().setWidth(200)

scaleLabel = mm.getMainMenu().addLabel("Y Scale")
ss = mm.getMainMenu().addSlider(10, "onYScaleSliderValueChanged(%value%)")
ss.getSlider().setValue(2)
ss.getWidget().setWidth(200)

sondebtn = mm.getMainMenu().addButton("Show Sonde Bathymetry", "lakeSonarMesh.setVisible(%value%)")
sondebtn.getButton().setCheckable(True)
sondebtn.getButton().setChecked(True)

ptx = mm.getMainMenu().addButton("Sonde Bathymetry Transparency", "lakeSonarMesh.getMaterial().setTransparent(%value%)")
ptx.getButton().setCheckable(True)
ptx.getButton().setChecked(False)

ss = mm.getMainMenu().addSlider(11, "lakeSonarMesh.getMaterial().setAlpha(%value% * 0.1)")
ss.getSlider().setValue(10)
ss.getWidget().setWidth(200)

dropbtn = mm.getMainMenu().addButton("Show Sonde Drops", "lakeSondeDrops.setVisible(%value%)")
dropbtn.getButton().setCheckable(True)
dropbtn.getButton().setChecked(True)

mrm = mm.getMainMenu().addSubMenu("Render Mode")
mrm.addButton("Normal", "renderModeNormal()")
mrm.addButton("Simple", "renderModeSimple()")
abtn = mrm.addButton("Additive", "setAdditive(%value%)")
abtn.getButton().setCheckable(True)
mrm.addLabel("------------------")
mrm.addButton("Color By Dive", "colorByDive()")
mrm.addButton("Color By Angle", "colorByAngle()")
mrm.addButton("Color By Range", "colorByRange()")
mrm.addButton("Color By Timestamp", "colorByTimestamp()")

def onPointSizeSliderValueChanged(value):
	size = ((value + 1) ** 2) * 0.01
	DivePointCloud.pointScale.setFloat(size)

def onAlphaSliderValueChanged(value):
	a = value * 0.1
	setDiveAlpha(a)
		
def setDiveAlpha(v):
	for dive in dives:
		dive.diveNode.getMaterial().setAlpha(v)

	
def onYScaleSliderValueChanged(value):
	scale = (value + 1)
	global scaleLabel
	global lake
	scaleLabel.setText("Y Scale:" + str(scale) + "x")
	lake.setScale(Vector3(1, 1, scale))
	
def renderModeNormal():
	for dive in dives:
		dive.diveNode.getMaterial().setProgram("points")
		dive.diveNode.getMaterial().setTransparent(True)

def renderModeSimple():
	for dive in dives:
		dive.diveNode.getMaterial().setProgram("points-simple")
		dive.diveNode.getMaterial().setTransparent(True)
	
def setAdditive(value):
	for dive in dives:
		dive.diveNode.getMaterial().setAdditive(value)
		dive.diveNode.getMaterial().setDepthTestEnabled(not value)
		
def colorByAngle():
	DivePointCloud.w1.setFloat(1)
	DivePointCloud.w2.setFloat(0)
	DivePointCloud.w3.setFloat(0)
	DivePointCloud.w4.setFloat(0)
	DivePointCloud.minDepth.setFloat(fieldMin.x)
	DivePointCloud.maxDepth.setFloat(fieldMax.x)

def colorByRange():
	DivePointCloud.w1.setFloat(0)
	DivePointCloud.w2.setFloat(1)
	DivePointCloud.w3.setFloat(0)
	DivePointCloud.w4.setFloat(0)
	DivePointCloud.minDepth.setFloat(fieldMin.y)
	DivePointCloud.maxDepth.setFloat(fieldMax.y)

def colorByTimestamp():
	DivePointCloud.w1.setFloat(0)
	DivePointCloud.w2.setFloat(0)
	DivePointCloud.w3.setFloat(1)
	DivePointCloud.w4.setFloat(0)
	DivePointCloud.minDepth.setFloat(fieldMin.z)
	DivePointCloud.maxDepth.setFloat(fieldMax.z)
	
def colorByDive():
	DivePointCloud.w1.setFloat(0)
	DivePointCloud.w2.setFloat(0)
	DivePointCloud.w3.setFloat(0)
	DivePointCloud.w4.setFloat(1)

#queueCommand(':hint displayWand')
queueCommand(":autonearfar on")
globalScale = 1
DivePointCloud.maxDepth.setFloat(50)
DivePointCloud.minDepth.setFloat(-50)

#------------------------------------------------------------------------------
# Wand ray information
wandRayPos = None
wandRayDir = None

#------------------------------------------------------------------------------
# Event callback
def handleEvent():
	e = getEvent()
	global globalScale
	global wandRayPos
	global wandRayDir
	
	# save wand ray
	if(e.getServiceType() == ServiceType.Wand):
		r = getRayFromEvent(e)
		wandRayPos = r[1]	
		wandRayDir = r[2]	
		
	if(not e.isProcessed()):
		cam = getDefaultCamera()
		if(e.getServiceType() == ServiceType.Wand and e.getSourceId() == 1):
			light.setPosition(e.getPosition())
		if(e.isButtonDown(EventFlags.ButtonLeft)): 
			cam.setPosition(Vector3(0, -1, 0))
			cam.setYawPitchRoll(Vector3(0, 0, 0))
		if(e.isButtonDown(EventFlags.ButtonUp)): 
			if(cam.isControllerEnabled()): globalScale = globalScale * 2.0
		if(e.isButtonDown(EventFlags.ButtonDown)): 
			if(cam.isControllerEnabled()): globalScale = globalScale / 2.0
		
setEventFunction(handleEvent)

lastLabelUpdate = 0

#------------------------------------------------------------------------------
def onUpdate(frame, time, dt):
	global curScale
	global globalScale
	global lastLabelUpdate
	global lbl
	
	curScale += (globalScale - curScale) * dt
	if(abs(curScale - globalScale) > 0.001):
		pivot.setScale(Vector3(curScale, curScale, curScale))
		
setUpdateFunction(onUpdate)

#scene.setBackgroundColor(Color('#303030'))

#------------------------------------------------------------------------------
# selection mode
def onSelectionUpdated():
	sp = PlaneRubberbandSelector.startPoint
	ep = PlaneRubberbandSelector.endPoint
	print(sp)
	print(ep)
	tape.startHandle.setPosition(sp)
	tape.endHandle.setPosition(ep)
	DivePointCloud.minBox.setVector3f(Vector3(sp.x, -100, sp.z))
	DivePointCloud.maxBox.setVector3f(Vector3(ep.x, 0, ep.z))
	#else:
	#	print("Invalid intersection")
	
def enableSelectionMode():
	PlaneRubberbandSelector.enabled = True
	PlaneRubberbandSelector.plane = Plane(Vector3(0,1,0), 0.0)
	PlaneRubberbandSelector.selectionUpdatedCallback = onSelectionUpdated
	cam = getDefaultCamera()
	cam.setControllerEnabled(False)
	p = lake.getBoundCenter()
	cam.setPosition(p + Vector3(0, lake.getBoundRadius() * 3, 0))
	cam.setPitchYawRoll(Vector3(radians(-90), radians(-55), 0))
	DivePointCloud.pointScale.setFloat(1)

#------------------------------------------------------------------------------
# setup the measuring tape
tape = MeasuringTape()
tapemnu = mm.getMainMenu().addSubMenu('Measuring Tape')
tapemnu.addButton('Set End', 'tapeSetEnd()')
tapemnu.addButton('Set Start', 'tapeSetStart()')
tapemnu.addButton('Set Bounds', 'setBounds()')
tapemnu.addButton('Reset Bounds', 'resetBounds()')

def tapeSetStart():
	# Position 2 meters away along wand.
	tape.startHandle.setPosition(wandRayPos + wandRayDir * 2)
	tape.startText.setFacingCamera(getDefaultCamera())
	#tape.startText.setColor(Color('black'))
	
def tapeSetEnd():
	# Position 2 meters away along wand.
	tape.endHandle.setPosition(wandRayPos + wandRayDir * 2)
	tape.endText.setFacingCamera(getDefaultCamera())
	#tape.endText.setColor(Color('black'))

def setBounds():
	ep = tape.endHandle.getPosition()
	sp = tape.startHandle.getPosition()
	minx = ep.x if ep.x < sp.x else sp.x
	miny = ep.y if ep.y < sp.y else sp.y
	minz = ep.z if ep.z < sp.z else sp.z
	maxx = ep.x if ep.x > sp.x else sp.x
	maxy = ep.y if ep.y > sp.y else sp.y
	maxz = ep.z if ep.z > sp.z else sp.z
	minv = Vector3(minx, miny, minz)
	maxv = Vector3(maxx, maxy, maxz)
	print(minv)
	print(maxv)
	DivePointCloud.minBox.setVector3f(minv)
	DivePointCloud.maxBox.setVector3f(maxv)	
	
def resetBounds():
	DivePointCloud.minBox.setVector3f(Vector3(-1000,-1000,-1000))
	DivePointCloud.maxBox.setVector3f(Vector3(1000,1000,1000))	