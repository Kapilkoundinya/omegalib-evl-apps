from math import *
from euclid import *
from omega import *
from cyclops import *

light = Light.create()
light.setColor(Color("#303030"))
light.setAmbient(Color("#000000"))
light.setPosition(Vector3(0, 50, -5))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#404060"))
light2.setAmbient(Color("#000000"))
light2.setPosition(Vector3(0, -50, 100))
light2.setEnabled(True)

light3 = Light.create()
light3.setColor(Color("#403030"))
light3.setAmbient(Color("#000000"))
light3.setPosition(Vector3(30, 10, -100))
light3.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

#skybox = Skybox()
#skybox.loadPano("enterprise/orion-constellation-panorama.jpg")
#scene.setSkyBox(skybox)

# setup skybox
skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/stars1", "png")
scene.setSkyBox(skybox)

shipModel = ModelInfo()
shipModel.name = "Enterprise"
shipModel.path = "qaser/Qaser_Albent.obj"
#shipModel.path = "enterprise/TextureMap/DeckA-TextureMapFBX.fbx"
shipModel.optimize = True
shipModel.usePowerOfTwoTextures = False
#shipModel.size = 40.0
scene.loadModelAsync(shipModel, "onModelLoaded()")

cam = getEngine().getDefaultCamera()
cam.setPosition(Vector3(0, 11.7, 28.13))

model = None

# Model loaded callback: create objects
def onModelLoaded():
	global model
	model = StaticObject.create("Enterprise")
	if(model != None):
		model.setPosition(Vector3(0, 0, 0))
		model.setEffect("textured")
		model.setScale(Vector3(1.0, 1.0, 1.0))


#setUpdateFunction(onUpdate)
