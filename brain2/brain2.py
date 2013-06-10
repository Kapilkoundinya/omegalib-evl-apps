from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *

# models to load
modelNames = ["fullbrain_arteries_low.fbx", "fullbrain_tissue.obj"]
modelEffects = {"fullbrain_arteries_low.fbx": "colored -d red -g 0.6 -s 10 -C", "fullbrain_tissue.obj": "colored -d #606080 -C -g 0.4, -s 4"}
models = []

light = Light.create()
light.setColor(Color("#808080"))
light.setAmbient(Color("#202020"))
light.setPosition(Vector3(0, 5, -5))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#505050"))
light2.setPosition(Vector3(0, 0, 0))
light2.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/grid3", "png")
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

mi1 = menu.addItem(MenuItemType.Button)
mi1.setText("Toggle Brain")
mi1.setCommand("models[1].setVisible(not models[1].isVisible())")

mi2 = menu.addItem(MenuItemType.Button)
mi2.setText("Toggle Blood Vessels")
mi2.setCommand("models[0].setVisible(not models[0].isVisible())")

# create the default interactor
interactor = ToolkitUtils.setupInteractor("config/interactor")

modelRoot = SceneNode.create('root')
modelRoot.setPosition(Vector3(0, 2, -2))
getScene().addChild(modelRoot)
interactor.setSceneNode(modelRoot)

globalScale = 10.0
curScale = 1.0

# Queue models for loading
for model in modelNames:
	mi = ModelInfo()
	mi.name = model
	mi.optimize = True
	mi.generateNormals = True
	mi.normalizeNormals = True
	mi.size = 10.0
	mi.path = "brain2/data/" + model
	scene.loadModelAsync(mi, "onModelLoaded('" + model + "')")
	
# Model loaded callback: create objects
def onModelLoaded(name):
	global models
	global modelRoot
	model = StaticObject.create(name)
	if(model != None):
		model.setPosition(Vector3(0, 0, 0))
		model.setEffect(modelEffects[name])
		if(name == "fullbrain_tissue.obj"):
			model.setScale(Vector3(1.2, 1.2, 1.2))
		else:
			model.setScale(Vector3(1.0, 1.0, 1.0))
		model.pitch(radians(-90))
		models.append(model)
		modelRoot.addChild(model)

#--------------------------------------------------------------------------------------------------
def onUpdate(frame, time, dt):
	global curScale
	global globalScale
	global modelRoot
	curScale += (globalScale - curScale) * dt
	if(abs(curScale - globalScale) > 0.01):
		modelRoot.setScale(Vector3(curScale, curScale, curScale))
		
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
		if(e.isButtonDown(EventFlags.ButtonLeft)): 
			cam.setPosition(Vector3(0, -1, 0))
			cam.setYawPitchRoll(Vector3(0, 0, 0))
		if(e.isButtonDown(EventFlags.ButtonUp)): 
			if(cam.isControllerEnabled()): globalScale = globalScale * 2.0
		if(e.isButtonDown(EventFlags.ButtonDown)): 
			if(cam.isControllerEnabled()): globalScale = globalScale / 2.0
		
setUpdateFunction(onUpdate)
setEventFunction(handleEvent)

# Setup soundtrack
se = getSoundEnvironment()
if se != None:
	music = se.loadSoundFromFile('music', '/Users/evldemo/sounds/music/filmic.wav')
	simusic = SoundInstance(music)
	simusic.setPosition(Vector3(0, 2, -1))
	simusic.setLoop(True)
	simusic.setVolume(0.1)
	simusic.playStereo()

queueCommand(":freefly")

# comment these out if you want to enable the background grid
#scene.setSkyBox(None)
#scene.setBackgroundColor(Color('#000000'))
