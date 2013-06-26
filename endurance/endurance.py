from math import *
from euclid import *
from omega import *
from cyclops import *
from pointCloud import *

scene = getSceneManager()
scene.addLoader(PointsLoader())

# The '..' at the beginning is to move up and out of the omega data dir. default shaders for
# pointCloud are inside the modules directory.
shaderPath = "../modules/pointCloud/shaders";
program = ProgramAsset()
program.name = "pointsDepth"
program.vertexShaderName = shaderPath + "/Sphere.vert"
program.fragmentShaderName = shaderPath + "/Sphere.frag"
program.geometryShaderName = shaderPath + "/Sphere.geom"
program.geometryOutVertices = 4
program.geometryInput = PrimitiveType.Points
program.geometryOutput = PrimitiveType.TriangleStrip
scene.addProgram(program)

shaderPath = "./shaders";
programDepthColor = ProgramAsset()
programDepthColor.name = "points"
programDepthColor.vertexShaderName = shaderPath + "/SphereDepthColor.vert"
programDepthColor.fragmentShaderName = shaderPath + "/SphereDepthColor.frag"
programDepthColor.geometryShaderName = shaderPath + "/Sphere.geom"
programDepthColor.geometryOutVertices = 4
programDepthColor.geometryInput = PrimitiveType.Points
programDepthColor.geometryOutput = PrimitiveType.TriangleStrip
scene.addProgram(programDepthColor)

shaderPath = "./shaders";
programFuzzy = ProgramAsset()
programFuzzy.name = "pointsFuzzy"
programFuzzy.vertexShaderName = shaderPath + "/SphereFuzzy.vert"
programFuzzy.fragmentShaderName = shaderPath + "/SphereFuzzy.frag"
programFuzzy.geometryShaderName = shaderPath + "/Sphere.geom"
programFuzzy.geometryOutVertices = 4
programFuzzy.geometryInput = PrimitiveType.Points
programFuzzy.geometryOutput = PrimitiveType.TriangleStrip
scene.addProgram(programFuzzy)

#------------------------------------------------------------------------------
lakePoints = ModelInfo()
lakePoints.name = "lake-points"
lakePoints.path = "data/bonney-points-09.xyz"
lakePoints.optimize = True
scene.loadModel(lakePoints)

lakeSonarMeshModel = ModelInfo()
lakeSonarMeshModel.name = "lake-sonar-mesh"
lakeSonarMeshModel.path = "data/bonney-sonde-bathy.obj"
lakeSonarMeshModel.optimize = True
lakeSonarMeshModel.generateNormals = True
lakeSonarMeshModel.normalizeNormals = True
scene.loadModel(lakeSonarMeshModel)

lakeSondeDropsModel = ModelInfo()
lakeSondeDropsModel.name = "lake-sonde-drops"
lakeSondeDropsModel.path = "data/bonney-sonde-drops.obj"
lakeSondeDropsModel.optimize = True
lakeSondeDropsModel.generateNormals = True
lakeSondeDropsModel.normalizeNormals = True
scene.loadModel(lakeSondeDropsModel)

# Create a scene object using the loaded model
lake = StaticObject.create("lake-points")
lake.setEffect("points")
pointScale = lake.getMaterial().addUniform('pointScale', UniformType.Float)
globalAlpha = lake.getMaterial().addUniform('globalAlpha', UniformType.Float)
minDepth = lake.getMaterial().addUniform('unif_MinDepth', UniformType.Float)
maxDepth = lake.getMaterial().addUniform('unif_MaxDepth', UniformType.Float)

lakeSonarMesh = StaticObject.create("lake-sonar-mesh")
lakeSonarMesh.setEffect("colored -e white -C -t | colored -d black -w -o -1000 -C -t")
lake.addChild(lakeSonarMesh)

lakeSondeDrops = StaticObject.create("lake-sonde-drops")
lakeSondeDrops.setEffect("colored -e #008000")
lakeSondeDrops.setScale(Vector3(1, 1, 1/6.0))
lake.addChild(lakeSondeDrops)

minDepth.setFloat(10)
maxDepth.setFloat(50.0)

pointScale.setFloat(0.02)
globalAlpha.setFloat(1.0)

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

lbl = mm.getMainMenu().addLabel("Camera Position:")

mm.getMainMenu().addLabel("Point Size")
ss = mm.getMainMenu().addSlider(10, "onPointSizeSliderValueChanged(%value%)")
ss.getSlider().setValue(4)
ss.getWidget().setWidth(200)

ptx = mm.getMainMenu().addButton("Point Transparency", "lake.getMaterial().setTransparent(%value%)")
ptx.getButton().setCheckable(True)
ptx.getButton().setChecked(True)

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
mrm.addButton("Color By Normal", "renderModeNormal()")
mrm.addButton("Color By Depth", "renderModeDepthColor()")
mrm.addButton("Fuzzy", "renderModeFuzzy()")

def onPointSizeSliderValueChanged(value):
	size = (value + 1) * 0.01
	pointScale.setFloat(size)

def onAlphaSliderValueChanged(value):
	a = value * 0.1
	globalAlpha.setFloat(a)
	
def onYScaleSliderValueChanged(value):
	scale = (value + 1)
	global scaleLabel
	global lake
	scaleLabel.setText("Y Scale:" + str(scale) + "x")
	lake.setScale(Vector3(1, 1, scale))
	
def renderModeNormal():
	lake.setEffect("points")

def renderModeDepthColor():
	lake.setEffect("pointsDepth")

def renderModeFuzzy():
	lake.setEffect("pointsFuzzy -t -a -D")


#queueCommand(':hint displayWand')

# Event callback
def handleEvent():
	e = getEvent()
	global globalScale
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

#--------------------------------------------------------------------------------------------------
def onUpdate(frame, time, dt):
	global curScale
	global globalScale
	global lastLabelUpdate
	global lbl
	
	if(time - lastLabelUpdate > 0.5):
		lastLabelUpdate = time
		c = getDefaultCamera().getPosition() + getDefaultCamera().getHeadOffset()
		sx = "%.2f" % c.x
		sy = "%.2f" % c.y
		sz = "%.2f" % c.z
		lbl.setText("Center Position: " + sx + " " + sz + " " + sy)
	
	curScale += (globalScale - curScale) * dt
	if(abs(curScale - globalScale) > 0.001):
		pivot.setScale(Vector3(curScale, curScale, curScale))
		
setUpdateFunction(onUpdate)