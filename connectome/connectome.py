from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *

# models to load
modelNames = ["fullbrain_tissue.fbx", "fullbrain2.fbx"]
modelEffects = {
	"fullbrain_tissue.fbx": "colored -d #303030b0 -C -t -a -D",
	"fullbrain2.fbx": "colored -g 0.6 -s 10"}
modelScales = {
	"fullbrain_tissue.fbx": Vector3(1.2, 1.2, 1.2),
	"fullbrain2.fbx": Vector3(1, 1, 1)}
modelPositions = {
	"fullbrain_tissue.fbx": Vector3(0, 0, 0),
	"fullbrain2.fbx": Vector3(0, -1, 0)}
models = []

light = Light.create()
light.setColor(Color("#a0a0a0"))
light.setAmbient(Color("#101020"))
light.setPosition(Vector3(0, 5, -5))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#606040"))
light2.setPosition(Vector3(0, 0, 0))
light2.setEnabled(True)
light2.setAttenuation(0, 0.1, 0.1)
#light2.setLightType(LightType.Spot)
#light2.setSpotCutoff(30)
#light2.setSpotExponent(20)

scene = getSceneManager()
scene.setMainLight(light)

skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/grid5", "png")
scene.setSkyBox(skybox)

camera = getDefaultCamera()
camera.setPosition(Vector3(0, 0, 0))
camera.addChild(light2)

# setup menu
mm = MenuManager.createAndInitialize()
menu = mm.getMainMenu()
if(menu == None):
	menu = mm.createMenu("main")
	mm.setMainMenu(menu)

mi1 = menu.addButton("Toggle Brain", "toggleModel(0)")
mi3 = menu.addButton("Toggle DTR", "toggleModel(1)")
mi4 = menu.addButton("Toggle Background", "toggleBackground(%value%)")
mi5 = menu.addButton("Connectome Transparency", "toggleConnectomeTransparency(%value%)")
mi4.getButton().setCheckable(True)
mi4.getButton().setChecked(True)
mi5.getButton().setCheckable(True)

def toggleConnectomeTransparency(t):
	if(t):
		models[1].setEffect("colored -g 0.6 -s 10 -t -a -D")
		models[1].getMaterial().setAlpha(0.3)
	else:
		models[1].setEffect("colored -g 0.6 -s 10")
		models[1].getMaterial().setAlpha(1)

def toggleModel(modelId):
	if(modelId == 0):
		# control brain fade.
		global brainTargetFade
		if(brainTargetFade == 1.0): 
			brainTargetFade = 0.0
		else:
			brainTargetFade = 1.0
	else:
		models[modelId].setVisible(not models[modelId].isVisible())

def toggleBackground(enabled):
	if(enabled):
		scene.setSkyBox(skybox)
	else:
		scene.setSkyBox(None)
		scene.setBackgroundColor(Color('#000000'))

# create the default interactor
interactor = ToolkitUtils.setupInteractor("config/interactor")

modelRoot = SceneNode.create('root')
modelRoot.setPosition(Vector3(0, 2, -2))
getScene().addChild(modelRoot)
interactor.setSceneNode(modelRoot)

globalScale = 10.0
curScale = 1.0

brainTargetFade = 1.0
brainCurFade = 0.0

# Queue models for loading
for model in modelNames:
	mi = ModelInfo()
	mi.name = model
	mi.optimize = True
	mi.generateNormals = True
	mi.normalizeNormals = True
	mi.size = 10.0
	mi.path = "data/" + model
	scene.loadModelAsync(mi, "onModelLoaded('" + model + "')")
	
# Model loaded callback: create objects
def onModelLoaded(name):
	global models
	global modelRoot
	model = StaticObject.create(name)
	if(model != None):
		model.setPosition(Vector3(0, 0, 0))
		model.setEffect(modelEffects[name])
		model.setPosition(modelPositions[name])
		model.setScale(modelScales[name])
		model.pitch(radians(-90))
		models.append(model)
		modelRoot.addChild(model)

#--------------------------------------------------------------------------------------------------
def onUpdate(frame, time, dt):
	global curScale
	global globalScale
	global modelRoot
	global brainTargetFade
	global brainCurFade
	curScale += (globalScale - curScale) * dt
	if(abs(curScale - globalScale) > 0.01):
		modelRoot.setScale(Vector3(curScale, curScale, curScale))
	# fade brain in/out
	if(len(models) > 0):
		brainCurFade += (brainTargetFade - brainCurFade) * dt * 4
		if(abs(brainCurFade - brainTargetFade) > 0.01):
			models[0].getMaterial().setAlpha(brainCurFade)
			scale = 4 - brainCurFade * 3
			models[0].setScale(Vector3(scale, scale, scale))
		
# Event callback
def handleEvent():
	global curScale
	global globalScale
	global light2
	e = getEvent()
	if(not e.isProcessed()):
		cam = getDefaultCamera()
		if(e.getServiceType() == ServiceType.Mocap and e.getSourceId() == 1):
			light2.setPosition(e.getPosition())
			light2.setLightDirection(e.getOrientation() * Vector3(0, 0, -1))
		if(e.isButtonDown(EventFlags.ButtonLeft)): 
			cam.setPosition(Vector3(0, -1, 0))
			cam.setPitchYawRoll(Vector3(0, 0, 0))
		if(e.isButtonDown(EventFlags.ButtonUp)): 
			if(cam.isControllerEnabled()): globalScale = globalScale * 2.0
		if(e.isButtonDown(EventFlags.ButtonDown)): 
			if(cam.isControllerEnabled()): globalScale = globalScale / 2.0
		
setUpdateFunction(onUpdate)
setEventFunction(handleEvent)

# Setup soundtrack
se = getSoundEnvironment()
if se != None:
	music = se.loadSoundFromFile('music', '/Users/evldemo/sounds/music/hq2.wav')
	simusic = SoundInstance(music)
	simusic.setPosition(Vector3(0, 2, -1))
	simusic.setLoop(True)
	#simusic.setReverb(0.1)
	#simusic.setMix(0.1)
	simusic.setWidth(18)
	simusic.setVolume(0.4)
	simusic.playStereo()

queueCommand(":freefly")
