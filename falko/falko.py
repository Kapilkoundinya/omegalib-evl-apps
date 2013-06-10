from math import *
from euclid import *
from omega import *
from cyclops import *

light = Light.create()
light.setColor(Color("#505050"))
light.setAmbient(Color("#606040"))
light.setPosition(Vector3(0, 50, -5))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#606080"))
light2.setAmbient(Color("#000000"))
light2.setPosition(Vector3(0, -50, 100))
light2.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

cam = getDefaultCamera()
cam.setPosition(Vector3(64, 0, 60))
cam.setYawPitchRoll(Vector3(0, -0.5, 0))

#skybox = Skybox()
#skybox.loadPano("enterprise/orion-constellation-panorama.jpg")
#scene.setSkyBox(skybox)

# setup skybox
skybox = Skybox()
#skybox.loadCubeMap("cubemaps/gradient1", "png")
skybox.loadCubeMap("common/cubemaps/grid4", "png")
scene.setSkyBox(skybox)

shipModel = ModelInfo()
shipModel.name = "Enterprise"
shipModel.path = "falko/se_building.obj"
#shipModel.path = "enterprise/TextureMap/DeckA-TextureMapFBX.fbx"
shipModel.optimize = True
shipModel.usePowerOfTwoTextures = False
#shipModel.size = 40.0
scene.loadModelAsync(shipModel, "onModelLoaded()")

model = None

# Model loaded callback: create objects
def onModelLoaded():
	global model
	model = StaticObject.create("Enterprise")
	if(model != None):
		model.setPosition(Vector3(0, 0, 0))
		model.setEffect("textured")
		model.setScale(Vector3(0.02, 0.02, 0.02))


#setUpdateFunction(onUpdate)
