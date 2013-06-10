from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *

# models to load
modelNames = {
		'rep1': ("rep1.fbx", True),
		'rep2': ("rep2.fbx", True),
		'rep3': ("rep3.fbx", True),
		'rep4': ("rep4.fbx", True),
		'rep5': ("rep5.fbx", True),
 }
		
models = {}

#getSceneManager().displayWand(0, 1)

light = Light.create()
light.setColor(Color("#505050"))
light.setAmbient(Color("#202020"))
light.setPosition(Vector3(50, 50, 0))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#505030"))
light2.setPosition(Vector3(-50, -50, 0))
light2.setEnabled(True)

light3 = Light.create()
light3.setColor(Color("#505030"))
light3.setPosition(Vector3(0, 0, 0))
light3.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

skybox = Skybox()
skybox.loadCubeMap("cubemaps/gradient2", "png")
skybox.loadCubeMap("common/cubemaps/grid3", "png")
scene.setSkyBox(skybox)
scene.setBackgroundColor(Color('#202020'))

# setup menu
mm = MenuManager.createAndInitialize()
menu = mm.getMainMenu()
if(menu == None):
	menu = mm.createMenu("main")
	mm.setMainMenu(menu)

globalScale = 4.0
curScale = 1.0

cam = getDefaultCamera()
cam.setPosition(Vector3(0, -1, 2))
cam.addChild(light3)

# create the default interactor
interactor = ToolkitUtils.setupInteractor("config/interactor")

modelRoot = SceneNode.create("modelRoot")
modelRoot.setPosition(Vector3(0, 1, 0))
getScene().addChild(modelRoot)
interactor.setSceneNode(modelRoot)

# Queue models for loading
for name,model in modelNames.iteritems():
	mi = ModelInfo()
	mi.name = name
	mi.optimize = True
	mi.path = "molecule/data/" + model[0]
	scene.loadModelAsync(mi, "onModelLoaded('" + name + "')")
	
#--------------------------------------------------------------------------------------------------
# Model loaded callback: create objects
def onModelLoaded(name):
	global models
	global modelRoot
	model = StaticObject.create(name)
	modelRoot.addChild(model)
	if(model != None):
		model.setPosition(Vector3(0, 0, 0))
		# disable backface culling
		model.setEffect("colored -g 1.0 -C")
		model.setVisible(modelNames[name][1])
		#model.setAlpha(0.0)
		model.setScale(Vector3(3, 3, 3))
		models[name] = model
		global menu
		mi = menu.addItem(MenuItemType.Button)
		mi.setText(name)
		mi.setCommand("toggleModel('" + name + "')")
		
#--------------------------------------------------------------------------------------------------
def toggleModel(name):
	global models
	print(getEvent().getType())
	models[name].setVisible(not models[name].isVisible())
	
#--------------------------------------------------------------------------------------------------
def handleEvent():
	global curScale
	global globalScale
	global light3
	e = getEvent()
	if(not e.isProcessed()):
		cam = getDefaultCamera()
		if(e.getServiceType() == ServiceType.Mocap and e.getSourceId() == 1):
			light3.setPosition(e.getPosition())
		if(e.isButtonDown(EventFlags.ButtonLeft)): 
			cam.setPosition(Vector3(0, -1, 0))
			cam.setYawPitchRoll(Vector3(0, 0, 0))
		if(e.isButtonDown(EventFlags.ButtonUp)): 
			if(cam.isControllerEnabled()): globalScale = globalScale * 1.5
		if(e.isButtonDown(EventFlags.ButtonDown)): 
			if(cam.isControllerEnabled()): globalScale = globalScale / 1.5

#--------------------------------------------------------------------------------------------------
def onUpdate(frame, time, dt):
	global curScale
	global globalScale
	global modelRoot
	curScale += (globalScale - curScale) * dt
	if(abs(curScale - globalScale) > 0.01):
		modelRoot.setScale(Vector3(curScale, curScale, curScale))
		
setEventFunction(handleEvent)
setUpdateFunction(onUpdate)

# Setup soundtrack
se = getSoundEnvironment()
if(se != None):
	music = se.loadSoundFromFile('music', '/Users/evldemo/sounds/music/slow.wav')
	simusic = SoundInstance(music)
	simusic.setPosition(Vector3(0, 2, -1))
	simusic.setLoop(True)
	#simusic.setReverb(0.0)
	#simusic.setMix(0.0)
	#simusic.setWidth(18)
	simusic.setVolume(0.1)
	simusic.playStereo()

queueCommand(":freefly")

# comment these out if you want to enable the background grid
#scene.setSkyBox(None)
#scene.setBackgroundColor(Color('#000000'))
