from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *

scene = getSceneManager()

#--------------------------------------------------------------------------------------------------
# Model table
class ModelData:
    def __init__(self, name, label, path, effect, defaultPosition=Vector3(0, 2, -4), size=-1.0, animated = False):
        self.type = type
        self.name = name
        self.label = label
        self.path = path
        self.effect = effect
        self.animated = animated
        self.defaultPosition = defaultPosition
        self.size = size

orun("modelView/Config.py")

# dictionary of loaded models. will be filled up by the onModelLoaded function
loadedModels = {}

#--------------------------------------------------------------------------------------------------
# Start model loading queue
for name, model in models.iteritems():
	mi = ModelInfo()
	mi.name = name
	mi.path = model.path
	mi.size = model.size
	mi.optimize = True
	scene.loadModelAsync(mi, "onModelLoaded('" + mi.name + "')")
	
#--------------------------------------------------------------------------------------------------
light = Light.create()
light.setColor(Color("#807070"))
light.setAmbient(Color("#202020"))
light.setPosition(Vector3(0, 20, -5))
light.setEnabled(True)
scene.setMainLight(light)

light2 = Light.create()
light2.setColor(Color("#707090"))
light2.setPosition(Vector3(0, -20, -5))
light2.setEnabled(True)

# setup menu
mm = MenuManager.createAndInitialize()
menu = mm.createMenu("main")
mm.setMainMenu(menu)

# setup the skybox menu
miSkyboxes = menu.addItem(MenuItemType.SubMenu)
miSkyboxes.setText("Background");
menuSkyboxes = miSkyboxes.getSubMenu()
misb1 = menuSkyboxes.addItem(MenuItemType.Button)
misb1.setText("Gradient 1")
misb1.setCommand('skybox.loadCubeMap("cubemaps/gradient1", "png")')
misb1 = menuSkyboxes.addItem(MenuItemType.Button)
misb1.setText("Gradient 2")
misb1.setCommand('skybox.loadCubeMap("cubemaps/gradient2", "png")')
misb1 = menuSkyboxes.addItem(MenuItemType.Button)
misb1.setText("Grid 1")
misb1.setCommand('skybox.loadCubeMap("common/cubemaps/grid3", "png")')
misb1 = menuSkyboxes.addItem(MenuItemType.Button)
misb1.setText("Grid 2")
misb1.setCommand('skybox.loadCubeMap("common/cubemaps/grid4", "png")')
misb1 = menuSkyboxes.addItem(MenuItemType.Button)
misb1.setText("Stars")
misb1.setCommand('skybox.loadCubeMap("common/cubemaps/stars", "png")')

# setup skybox
skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/grid4", "png")
scene.setSkyBox(skybox)

# create the default interactor
interactor = ToolkitUtils.setupInteractor("config/interactor")

# The currently visible model
curModel = None

# enable wand
scene.displayWand(0, 1)

#--------------------------------------------------------------------------------------------------
def onModelLoaded(name):
	m = models[name]
	if(m.animated == False): model = StaticObject.create(m.name)
	else: model = AnimatedObject.create(m.name)
	#model.setBoundingBoxVisible(True)
	model.setPosition(m.defaultPosition)
	model.setEffect(m.effect)
	model.setSelectable(True)
	model.setVisible(False)
	loadedModels[name] = model
	global menu
	mi = menu.addItem(MenuItemType.Button)
	mi.setText(m.label)
	mi.setCommand("toggleModel('" + name + "')")

#--------------------------------------------------------------------------------------------------
def toggleModel(name):
	global curModel
	if(curModel != None): 
		curModel.setVisible(False)
	curModel = loadedModels[name]
	curModel.setVisible(True)
	#interactor.setSceneNode(curModel)
	curModel.setSelected(True)
	if(models[name].animated == True and curModel.hasAnimations()): curModel.loopAnimation(0)

#--------------------------------------------------------------------------------------------------
#def onEvent():
	
#setEventFunction(onEvent)
#setUpdateFunction(onUpdate)
#toggleModel("astronaut")
