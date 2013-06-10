from math import *
from euclid import *
from omega import *
from cyclops import *

light = Light.create()
light.setColor(Color("#303030"))
light.setAmbient(Color("#020202"))
light.setPosition(Vector3(0, 50, -5))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#404060"))
light2.setAmbient(Color("#000000"))
light2.setPosition(Vector3(100, 200, 0))
light2.setEnabled(True)

light3 = Light.create()
light3.setColor(Color("#404030"))
light3.setAmbient(Color("#000000"))
light3.setPosition(Vector3(0, 0, 300))
light3.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

# setup skybox
skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/stars1", "png")
scene.setSkyBox(skybox)

shipModel = ModelInfo()
shipModel.name = "Enterprise"
shipModel.path = "/home/evl/anishi2/models/Enterprise/Enterprise.obj"
#shipModel.path = "enterprise/TextureMap/DeckA-TextureMapFBX.fbx"
shipModel.optimize = True
shipModel.usePowerOfTwoTextures = False
#shipModel.size = 40.0
scene.loadModelAsync(shipModel, "onModelLoaded()")

cam = getEngine().getDefaultCamera()
# main deck
cam.setPosition(Vector3(-3, 32.25, 10.20))

# lounge
#cam.setPosition(Vector3(0, 26.3, -5.3))

# front
#cam.setPosition(Vector3(0.5, 29, 176))


model = None

# Model loaded callback: create objects
def onModelLoaded():
	global model
	model = StaticObject.create("Enterprise")
	if(model != None):
		model.setPosition(Vector3(0, 0, 0))
		model.setEffect("textured")
		model.setScale(Vector3(1, 1, 1))


#setUpdateFunction(onUpdate)
