from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *

# models to load
modelNames = {
		'Drainage': ("T1Block11_One_Quarter_Drainage.fbx", True, 'green'),
		'Top Slab Rebar': ("T1Block02_OneQuarter_TopSlabRebar.fbx", True, 'yellow'),
		'Bottom Slab Rebar': ("T1Block03_OneQuarter_BotSlabRebar.fbx", True, 'blue'),
		'Steel Struct': ("T1Block01A_OneQuarter_StructSteel_noPiles.fbx", False, 'red'),
		'Cutout Rebar': ("T1Block04_One_Quarter_CutOutRebar.fbx", False, '#ff00ff'),
		'Walls': ("T1Block05_OneQuarter_Walls.fbx", False, '#00ffff'),
		'Fender Rebars': ("T1Block06_One_Quarter_FendersRebars.fbx", False, 'green'),
		'Skirt Rebar': ("T1Block07_OneQuarter_SkirtRebar.fbx", False, 'yellow'),
		'Skirt AB Layout': ("T1Block08_One_Quarter_SkirtABLayout.fbx", False, 'blue'),
		'Pile Rebar': ("T1Block09_OneQuarter_PileRebar.fbx", False, 'red'),
		'WWF': ("T1Block10_One_Quarter_WWF.fbx", False, 'teal') }
		
models = {}

light = Light.create()
light.setColor(Color("#505050"))
light.setAmbient(Color("#202020"))
light.setPosition(Vector3(0, 50, -5))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#505030"))
light2.setPosition(Vector3(50, 0, 50))
light2.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/grid4", "png")
scene.setSkyBox(skybox)

# setup menu
mm = MenuManager.createAndInitialize()
menu = mm.getMainMenu()
mm.setMainMenu(menu)

mi1 = menu.addButton("Toggle Background", "toggleBackground(%value%)")
mi1.getButton().setCheckable(True)
mi1.getButton().setChecked(True)

# Queue models for loading
for name,model in modelNames.iteritems():
	mi = ModelInfo()
	mi.name = name
	mi.optimize = True
	mi.path = "baybridge/baybridge/" + model[0]
	scene.loadModelAsync(mi, "onModelLoaded('" + name + "')")

#--------------------------------------------------------------------------------------------------
# Model loaded callback: create objects
def onModelLoaded(name):
	global models
	model = StaticObject.create(name)
	if(model != None):
		model.setPosition(Vector3(0, 2, 0))
		model.setEffect("colored -g 1.0 -d " + modelNames[name][2])
		model.setVisible(modelNames[name][1])
		#model.setAlpha(0.0)
		model.setScale(Vector3(0.001, 0.001, 0.001))
		models[name] = model
		global menu
		mi = menu.addItem(MenuItemType.Button)
		mi.setText(name)
		mi.setCommand("toggleModel('" + name + "')")
		mi.getButton().setCheckable(True)
		mi.getButton().setChecked(modelNames[name][1])
#--------------------------------------------------------------------------------------------------
def toggleModel(name):
	global models
	models[name].setVisible(not models[name].isVisible())
#--------------------------------------------------------------------------------------------------
def toggleBackground(enabled):
	if(enabled):
		scene.setSkyBox(skybox)
	else:
		scene.setSkyBox(None)
		scene.setBackgroundColor(Color('#000000'))
#--------------------------------------------------------------------------------------------------
# Update callback
#def onUpdate(frame, time, dt):
	# if dt < 0.1:
		# for name,model in models.iteritems():
			# a = model.getAlpha()
			# if a < 0.99:
				# a += (1.0 - a) * dt * 2
				# model.setAlpha(a)
			# elif a != 1.0:
				# model.setAlpha(1.0)
		
#setUpdateFunction(onUpdate)
