# (C) 2012-2013 by Arthur Nishimoto, Electronic Visualization Laboratory, University of Illinois at Chicago
# Version: 0.5a - CAVEUTIL integration
#
# Models associated with this application (C) 2011 - 2013 by Arthur Nishimoto
# with the following exception:
# Refit Enterprise exterior modeled by Dennis Bailey. Converted by Eric Clark. Modified by Arthur Nishimoto.
#
#
# Version Notes:
#		v0.5a - CAVEUTIL integration
#		v0.4 - Localized bridge and engineering sounds, updated exterior textures
#		v0.3 - Textured mapped bridge, new drydock
#		v0.2 - Added music
#		v0.1 - Initial version

from math import *
from euclid import *
from omega import *
from cyclops import *

from caveutil import *

#--------------------------------------------------------------------------------------------------
# Setup sounds
se = getSoundEnvironment()
se.setAssetDirectory('enterprise')

se.setForceCacheOverwrite(False)
#print se.isForceCacheOverwriteEnabled()


localSoundPath = '/sounds/'

#music1 = se.loadSoundFromFile('music1', localSoundPath+ 'EnterpriseBridgeMusic01.wav')
#music2 = se.loadSoundFromFile('music2', localSoundPath+ 'KirkInSpaceShuttle.wav')
#music3 = se.loadSoundFromFile('music3', localSoundPath+ 'EnterprisingYoungMen.wav')
#music4 = se.loadSoundFromFile('music4', localSoundPath+ 'ScherzoForMotorcycleAndOrchestra.wav')
music5 = se.loadSoundFromFile('music5', localSoundPath+ 'TMP-MainTitle.wav')
music6 = se.loadSoundFromFile('loadingMusic', localSoundPath+ 'The Enterprise.wav')

bridgeAmbient = se.loadSoundFromFile('bridgeAmbient', localSoundPath+ 'TVH-Enterprise Bridge-mono.wav')
warpCoreAmbient = se.loadSoundFromFile('warpCoreAmbient', localSoundPath+ 'WarpCoreHum.wav')


musicIntroEnabled = False
musicIntroEnded = False

# Play music while loading
si_introMusic = SoundInstance(music5)
si_introMusic.setLoop(False)
si_introMusic.setVolume(0.1)
#si_introMusic.setPitch(0.918)
si_introMusic.playStereo()

simusic = SoundInstance(music6)
simusic.setLoop(True)
simusic.setVolume(0.0)
#simusic.setPitch(0.918)

def setMusic(id):
	global simusic
	global si_introMusic
	global musicIntroEnabled
	
	# Disables music intro timers if music is manually changed
	musicIntroEnabled = False
	
	if( simusic is not None ):
		simusic.stop()
		si_introMusic.stop();
        if( id == 0 ):
                simusic = SoundInstance(music1)
        elif( id == 1 ):
                simusic = SoundInstance(music2)
        elif( id == 2 ):
                simusic = SoundInstance(music3)
        elif( id == 3 ):
                simusic = SoundInstance(music6)
        elif( id == 4 ):
                simusic = SoundInstance(music4)
        elif( id == 5 ):
                simusic = SoundInstance(music5)
        simusic.setLoop(True)
        simusic.setVolume(0.2)
        simusic.playStereo()

def getSoundEnvelope(objPos, max, baseVolume ):
	camPos = cam.getPosition()
	dist = math.sqrt((camPos.x - objPos.x)**2 + (camPos.y - objPos.y)**2 + (camPos.z - objPos.z)**2)
	newVol = ( 1 - (dist / max)) * baseVolume
	if( newVol > 1 or newVol < 0 ):
		newVol = 0
	return newVol

#--------------------------------------------------------------------------------------------------
# setup caveutil

# Use Python's Pickle module to save and load previously recorded waypoints to file.
import pickle

# Set up the InterpolActor to control the camera
interp = InterpolActor(getDefaultCamera())
interp.setTransitionType(InterpolActor.SMOOTH)	# Use SMOOTH ease-in/ease-out interpolation rather than LINEAR
interp.setDuration(3)							# Set interpolation duration to 3 seconds
interp.setOperation(InterpolActor.POSITION | InterpolActor.ORIENT)	# Interpolate both position and orientation

# These variables hold the position and orientation corresponding to the stored navigational waypoints.
g_positionArray = []
g_orientationArray = []
g_arrayTraversal = 0

# This function is used to iterate over the stored navigation waypoints.
def WaypointTraversalFunc(interpObj):
	global g_arrayTraversal
	global g_positionArray
	global g_orientationArray
	
	if g_arrayTraversal < len(g_positionArray):
		interpObj.setTargetPosition(g_positionArray[g_arrayTraversal])
		interpObj.setTargetOrientation(g_orientationArray[g_arrayTraversal])
		interpObj.startInterpolation()
		g_arrayTraversal=g_arrayTraversal+1

# Tell the camera's InterpolActor to call the WaypointTraversalFunc at the end of each interpolated waypoint so that it can cue up
# the next waypoint.
interp.setEndOfInterpolationFunction(WaypointTraversalFunc)

#--------------------------------------------------------------------------------------------------
# setup lights
# Exterior 1
light = Light.create()
light.setColor(Color("#ABABAB"))
light.setAmbient(Color("#000000"))
light.setPosition(Vector3(-100, -100, 111.5))
light.setEnabled(True)

# Exterior 2
light2 = Light.create()
light2.setColor(Color("#ABABAB"))
light2.setAmbient(Color("#000000"))
light2.setPosition(Vector3(100, 100, -111.5))
light2.setEnabled(True)

# Bridge
light3 = Light.create()
light3.setColor(Color("#FFFFFF"))
light3.setAmbient(Color("#000000"))
light3.setPosition(Vector3(0.0, 34.7, 11.1))
light3.setEnabled(True)

scene = getSceneManager()
scene.setBackgroundColor(Color('#000000'))
scene.setMainLight(light)

# Bridge
class LightSphere:

	def __init__(self):
		self.light = Light.create()
		self.color = Color("#FFFFFF")
		self.sphere = SphereShape.create(0.2,4)
		self.sphere.getMaterial().setColor(self.color,self.color)
		self.sphere.setEffect("textured -v emissive")
		self.sphere.setVisible(False)
		
		self.light.setColor(self.color)
		self.light.setAmbient(Color("#000000"))	
		self.light.setEnabled(False)
		self.light.setAttenuation(0.5,0.5,0.5)	
	def setPosition(self,x,y,z):
		self.light.setPosition(x,y,z)
		self.sphere.setPosition(x,y,z)
	def setAttenuation(self,contant,linear,quadratic):
		self.light.setAttenuation(contant,linear,quadratic)	
	def setColor(self,r,g,b,a):
		self.color = Color(r,g,b,a)
		self.light.setColor(self.color)
		self.sphere.getMaterial().setColor(self.color,self.color)
		
# note conversion from Blender( x, z, -y )
bridgePortL1 = LightSphere()
bridgePortL1.setPosition(3.1,34.5,8.55)

bridgePortL2 = LightSphere()
bridgePortL2.setPosition(4.01,34.5,11.52)

bridgePortL3 = LightSphere()
bridgePortL3.setPosition(2.62,34.5,14.28)

bridgeStbdL1 = LightSphere()
bridgeStbdL1.setPosition(-3.33,34.5,8.84)

bridgeStbdL2 = LightSphere()
bridgeStbdL2.setPosition(-4.0,34.5,11.88)

bridgeStbdL3 = LightSphere()
bridgeStbdL3.setPosition(-2.32,34.5,14.5)

bridgeCenterL = LightSphere()
bridgeCenterL.setPosition(0,34.1,11.1)
bridgeCenterL.setColor( 145/255.0, 212/255.0, 209/255.0, 1.0 )

bridgeCenterBackL = LightSphere()
bridgeCenterBackL.setPosition(0,34.6,7.88)

#bridgePortTurboL = LightSphere()
#bridgePortTurboL.setPosition(2.43,34.5,6.74)

def updateLightAttenuation(contant,linear,quadratic):
	bridgePortL1.setAttenuation(contant,linear,quadratic)
	bridgePortL2.setAttenuation(contant,linear,quadratic)
	bridgePortL3.setAttenuation(contant,linear,quadratic)
	bridgeStbdL1.setAttenuation(contant,linear,quadratic)
	bridgeStbdL2.setAttenuation(contant,linear,quadratic)
	bridgeStbdL3.setAttenuation(contant,linear,quadratic)

	
updateLightAttenuation(0.5,0.5,0.5)
	
scene = getSceneManager()
scene.setBackgroundColor(Color('#000000'))
scene.setMainLight(light)

#--------------------------------------------------------------------------------------------------
# setup skybox
skybox = Skybox()
skybox.loadCubeMap("enterprise/stars2", "png")
scene.setSkyBox(skybox)

#--------------------------------------------------------------------------------------------------
# Setup camera
cam = getDefaultCamera()
cam.setPosition(Vector3(1.8,32.5,9.2))
cam.setPitchYawRoll(Vector3(0,radians(160),0))

setNearFarZ(0.1,500)

#--------------------------------------------------------------------------------------------------
def loadModel(name, path):
	model = ModelInfo()
	model.name = name
	model.path = path
	model.optimize = True
	model.usePowerOfTwoTextures = False
	scene.loadModel(model)
	model = StaticObject.create(name)
	model.setEffect("textured");
	if( name == "HangerDeck"):
		model.setEffect("textured -C");
	
#--------------------------------------------------------------------------------------------------
def loadModelAsync(name, path):
	model = ModelInfo()
	model.name = name
	model.path = path
	model.optimize = True
	model.usePowerOfTwoTextures = False
	scene.loadModelAsync(model, "onModelLoaded('" + model.name + "')")

#--------------------------------------------------------------------------------------------------
def onModelLoaded(name):
	global bridge
	global bridgeDisplays
	
	model = StaticObject.create(name)
	model.setEffect("textured");
	if( name == "Bridge"):
		bridge = model
		bridge.getMaterial().setAlpha(30)
	elif( name == "BridgeDisplays"):
		bridgeDisplays = model
		bridgeDisplays.setEffect("textured -v emissive")
	elif( name == "HangerDeck"):
		model.setEffect("textured -C");

#--------------------------------------------------------------------------------------------------
modelPath = "models"

#loadModelAsync("Bridge", modelPath+"/DeckA.fbx")
#loadModelAsync("BridgeDisplays", modelPath+"/DeckA-displays.fbx")

loadModelAsync("Bridge", modelPath+"/DeckA-TextureMapped.fbx")
loadModelAsync("Exterior", modelPath+"/Exterior.fbx")
loadModelAsync("Drydock", modelPath+"/Drydock.fbx")
loadModelAsync("DeckBC", modelPath+"/DeckBC.fbx")
loadModelAsync("TorpedoBay", modelPath+"/TorpedoBay.fbx")
loadModelAsync("DeckD", modelPath+"/DeckD.fbx")

loadModelAsync("Engineering", modelPath+"/Engineering.fbx")
loadModelAsync("HangerDeck", modelPath+"/HangerDeck.fbx")

#--------------------------------------------------------------------------------------------------

si_bridgeAmbient = SoundInstance(bridgeAmbient)
si_bridgeAmbient.setPosition( Vector3(0.0,32.477,8.5) )
si_bridgeAmbient.setLoop(True)
si_bridgeAmbient.setVolume(0.5)
si_bridgeAmbient.setWidth(12)
si_bridgeAmbient.play()

si_warpCoreAmbient = SoundInstance(warpCoreAmbient)
si_warpCoreAmbient.setPosition( Vector3(0, -12.4, -47.3) )
si_warpCoreAmbient.setLoop(True)
si_warpCoreAmbient.setVolume(0.2)
si_warpCoreAmbient.setWidth(4)
si_warpCoreAmbient.play()

#--------------------------------------------------------------------------------------------------
def onEvent():
	global g_arrayTraversal
	global g_positionArray
	global g_orientationArray
	
	event = getEvent()
	
	if(not event.isProcessed()):
		t = event.getServiceType()
		
		if( t == ServiceType.Wand ): # CAVE2 wand controls
			# Playback navigation through all the stored waypoints
			if event.isButtonDown(EventFlags.Ctrl) or event.isButtonDown(EventFlags.ButtonUp):
				g_arrayTraversal = 0
				WaypointTraversalFunc(interp)
				
			# Record a waypoint.
			if event.isButtonDown(EventFlags.Shift) or event.isButtonDown(EventFlags.ButtonDown):
				g_positionArray.append(getDefaultCamera().getPosition())
				g_orientationArray.append(getDefaultCamera().getOrientation())
				print "SAVE WAYPOINT"
		elif( t == ServiceType.Pointer ): # Desktop controls
			# Playback navigation through all the stored waypoints
			if event.isButtonDown(EventFlags.Ctrl):
				g_arrayTraversal = 0
				WaypointTraversalFunc(interp)
				
			# Record a waypoint.
			if event.isButtonDown(EventFlags.Shift):
				g_positionArray.append(getDefaultCamera().getPosition())
				g_orientationArray.append(getDefaultCamera().getOrientation())
				print "SAVE WAYPOINT"
			
		if event.isKeyDown(ord('r')):
			print "SAVE WAYPOINT FILE"
			pickle.dump(g_positionArray, open("POS.way","wb"))
			pickle.dump(g_orientationArray, open("ORI.way","wb"))
			
		if event.isKeyDown(ord('t')):
			print "LOAD WAYPOINT FILE"
			g_positionArray = pickle.load(open("POS.way","rb"))
			g_orientationArray = pickle.load(open("ORI.way","rb"))
			
		if event.isKeyDown(ord('q')):
			g_positionArray.append(getDefaultCamera().getPosition())
			g_orientationArray.append(getDefaultCamera().getOrientation())
			print "SAVE WAYPOINT"
			
		if event.isKeyDown(ord('e')):
			g_arrayTraversal = 0
			WaypointTraversalFunc(interp)
			

#--------------------------------------------------------------------------------------------------
def onUpdate(frame, t, dt):
	global musicIntroEnded
	
	if( t > 80 and not musicIntroEnded ):
		musicIntroEnded = True
		si_introMusic.fade(0.0, 5.0)
		simusic.fade(0.2, 5.0)
	
	# Simple sound distance falloff implementation
	si_bridgeAmbient.setVolume( getSoundEnvelope(si_bridgeAmbient.getPosition(), 20, 0.5) )
	si_warpCoreAmbient.setVolume( getSoundEnvelope(si_warpCoreAmbient.getPosition(), 80, 0.2) )

	
setEventFunction(onEvent)
setUpdateFunction(onUpdate)

def warpTo( locID ):
	if( locID == 0 ): # Bridge - Port turbolift at CAVE2 entrance 
		cam.setPosition(Vector3(1.8,32.5,9.2)); cam.setPitchYawRoll(Vector3(0,radians(160),0))
	elif( locID == 101 ): # Bridge - Lower floor, helm console in CAVE, viewsceeen at entrance
		cam.setPosition(Vector3(0.16, 32.14, 12.01)); cam.setPitchYawRoll(Vector3(0,radians(0),0))
	elif( locID == 102 ): # Bridge - Command chair at CAVE2 center
		cam.setPosition(Vector3(0.0,32.477,8.5)); cam.setPitchYawRoll(Vector3(0,radians(180),0))
	elif( locID == 1 ): # Officer's Lounge
		cam.setPosition(Vector3(0.5, 27.3, -4)); cam.setPitchYawRoll(Vector3(0,radians(90),0))
	elif( locID == 2 ): # Transporter Room
		cam.setPosition(Vector3(-15, 22.9, 19)); cam.setPitchYawRoll(Vector3(0,radians(90),0))
	elif( locID == 3 ): # Main Engineering
		cam.setPosition(Vector3(1.1, -12.4, -44.3)); cam.setPitchYawRoll(Vector3(0,radians(90),0))
	elif( locID == 4 ): # Exterior Front
		cam.setPosition(Vector3(0.5, 29, 176)); cam.setPitchYawRoll(Vector3(0,radians(0),0))
	elif( locID == 5 ): # Drydock reception
		cam.setPosition(Vector3(89.25, 17.41, -5.43)); cam.setPitchYawRoll(Vector3(0,radians(90),0))
	elif( locID == 6 ): # Cargo bay
		cam.setPosition(Vector3(7.27, -18.43, -106.54)); cam.setPitchYawRoll(Vector3(0,radians(90),0))
	elif( locID == 7 ): # Torpedo Bay
		cam.setPosition(Vector3(2,-1.7,-61)); cam.setPitchYawRoll(Vector3(0,radians(160),0))

#--------------------------------------------------------------------------------------------------
mm = MenuManager.createAndInitialize()
mnu = mm.getMainMenu()
mm.setMainMenu(mnu)

mi = mnu.addImage(loadImage("appIcon.png"))
ics = mi.getImage().getSize() * 0.5
mi.getImage().setSize(ics)

bridgeMenu = mm.createMenu("Go to Bridge")
bridgeMenu = mnu.addSubMenu("Go to Bridge")
bridgeMenu.addButton("View 1", "warpTo(0)")
bridgeMenu.addButton("View 2", "warpTo(101)")
bridgeMenu.addButton("View 3", "warpTo(102)")

#mnu.addButton("Go to Bridge", "warpTo(0)")
mnu.addButton("Go to Officer's Lounge", "warpTo(1)")
mnu.addButton("Go to Transporter Room", "warpTo(2)")
mnu.addButton("Go to Torpedo Bay", "warpTo(7)")
mnu.addButton("Go to Engineering", "warpTo(3)")
mnu.addButton("Go to Cargo/Hanger Deck", "warpTo(6)")
mnu.addButton("Go to Drydock Reception", "warpTo(5)")
mnu.addButton("Go to front", "warpTo(4)")

musmnu = mm.createMenu("Music")
musmnu = mnu.addSubMenu("Music")
#musmnu.addButton("Enterprise Clears Moorings", "setMusic(0)")
#musmnu.addButton("Kirk in Space Shuttle", "setMusic(1)")
#musmnu.addButton("Enterprising Young Men", "setMusic(2)")
musmnu.addButton("The Enterprise", "setMusic(3)")
musmnu.addButton("Main Title (The Motion Picture)", "setMusic(5)")
#musmnu.addButton("Music 5", "setMusic(4)")
musmnu.addButton("Stop Music", "simusic.stop()")


