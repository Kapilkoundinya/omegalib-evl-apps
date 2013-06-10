from math import *
from euclid import *
from omega import *
from cyclops import *

light = Light.create()
light.setColor(Color("#505050"))
light.setAmbient(Color("#606050"))
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
cam.setPosition(Vector3(1.42, -0.7, 1))
cam.setPitchYawRoll(Vector3(radians(-90), 0, 0))

#skybox = Skybox()
#skybox.loadPano("enterprise/orion-constellation-panorama.jpg")
#scene.setSkyBox(skybox)
scene.setBackgroundColor(Color('#FFF0D6'))

# setup skybox
skybox = Skybox()
#skybox.loadCubeMap("cubemaps/gradient1", "png")
#skybox.loadCubeMap("common/cubemaps/grid4", "png")
#scene.setSkyBox(skybox)

osetdataprefix("mars/")

shipModel = ModelInfo()
shipModel.name = "Mars"
shipModel.path = "mars/loadMars.wrl"
#shipModel.path = "enterprise/TextureMap/DeckA-TextureMapFBX.fbx"
shipModel.optimize = True
shipModel.usePowerOfTwoTextures = False
#shipModel.size = 40.0
scene.loadModelAsync(shipModel, 'onModelLoaded()')

model = None

def onModelLoaded():
	global model
	model = StaticObject.create("Mars")
	if(model != None):
		model.setPosition(Vector3(0, 0, 0))
		model.setEffect("textured -C -t")
		#model.roll(radians((90))
		model.getMaterial().setAlpha(0.0)
		#model.setScale(Vector3(0.02, 0.02, 0.02))


def onUpdate(frame, time, dt):
	global model
	if(model != None and dt < 0.1):
		a = model.getMaterial().getAlpha()
		if(a < 0.99): a += (1 - a) * dt * 2
		else: a = 1
		model.getMaterial().setAlpha(a)
		
setUpdateFunction(onUpdate)

