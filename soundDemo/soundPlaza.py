from math import *
from euclid import *
from omega import *
from cyclops import *

#--------------------------------------------------------------------------------------------------
# setup lights
light = Light.create()
light.setColor(Color("white"))
light.setAmbient(Color("#202020"))
light.setPosition(Vector3(0, 33, 11.5))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("white"))
light2.setAmbient(Color("#000000"))
light2.setPosition(Vector3(0, -50, -50))
light2.setEnabled(True)

scene = getSceneManager()
scene.setBackgroundColor(Color('#000000'))
scene.setMainLight(light)

#--------------------------------------------------------------------------------------------------
# setup skybox
skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/Park2", "jpg")
scene.setSkyBox(skybox)

#--------------------------------------------------------------------------------------------------
# Setup camera
camSpeed = 1
cam = getDefaultCamera()

#--------------------------------------------------------------------------------------------------
# Setup Models
def loadModel(name, path):
	model = ModelInfo()
	model.name = name
	model.path = path
	model.optimize = True
	model.usePowerOfTwoTextures = False
	scene.loadModel(model)
	model = StaticObject.create(name)
	model.setEffect("textured");
	return model
	
modelPath = ""

loadModel("DemoPlaza", modelPath+"plaza/soundDemoPlaza.fbx")
canvasModel = loadModel("RotatingCanvas", modelPath+"plaza/soundDemoPlazaBoard.fbx")
canvasModel.setPosition(Vector3(24.53588,2.2,18.776))
 
#--------------------------------------------------------------------------------------------------
# Setup soundtrack
se = getSoundEnvironment()
#se.showDebugInfo(True)

# Used to set the initial directory which is prepended to the path given in loadSoundFromFile()
se.setAssetDirectory('/Users/evldemo/sounds/')

sound1 = se.loadSoundFromFile('sound1', 'BBC/51 - London/12 middleton square.wav')
sound2 = se.loadSoundFromFile('sound2', 'BBC/32 - Greece/06 Immense traffic, car horns and hooters.wav')
sound3 = se.loadSoundFromFile('sound3', 'BBC/50 - France/06 effiel tower.wav')
sound4 = se.loadSoundFromFile('sound4', 'BBC/50 - France/01 traffic.wav')
sound5 = se.loadSoundFromFile('sound5', 'BBC/56 - Footsteps 2/mono/01 Stone- Walking 1 - mono loop.wav')
s_waterfall = se.loadSoundFromFile('waterfall', 'BBC/11 - Water/mono/04 Waterfall - mono loop.wav')
s_bigben12 = se.loadSoundFromFile('bigben12', 'BBC/14 - City/mono/01 Big Ben - Striking 12 - mono - 23s delayed.wav')

si_waterfall = SoundInstance(s_waterfall)
si_waterfall.setPosition(Vector3(23.85632, 1.74978,-18.77636))
si_waterfall.setLoop(True)
si_waterfall.setWidth(3)
si_waterfall.play()

si_bigben = SoundInstance(s_bigben12)
si_bigben.setPosition(Vector3(8.33063, 1.74978,8.67092))
si_bigben.setLoop(True)
si_bigben.setWidth(3)
si_bigben.play()

sndInst = SoundInstance(sound1);

quietStreetSI = SoundInstance(sound1);
quietStreetSI.setLoop(True);
loudStreetSI = SoundInstance(sound2);
loudStreetSI.setLoop(True);

quietStreetSI.setVolume(1.0);
loudStreetSI.setVolume(0.0);

quietStreetSI.setPosition( canvasModel.getPosition() )
loudStreetSI.setPosition( canvasModel.getPosition() )

quietStreetSI.play();
loudStreetSI.play();

walkInst = SoundInstance(sound5);



def startWalk():
	global walkInst
	if( walkInst is not None ):
		walkInst.stop()
	
	walkInst = SoundInstance(sound5)
	walkInst.setLoop(True)
	walkInst.setVolume(0.6)
	
	# Since this is the tracked user's footsteps, play on all speakers
	walkInst.setEnvironmentSound(True)
	walkInst.play()

def stopWalk():
	global walkInst
	walkInst.stop()

def envSetReverb(value):
	se.setRoomSize(value)
	se.setWetness(value)

def playSoundInstance(soundID):
	global sndInst
	if( sndInst is not None ):
		sndInst.stop()
		
	if( soundID == 1 ):
		sndInst = SoundInstance(sound1);
	elif( soundID == 2 ):
		sndInst = SoundInstance(sound2);
	elif( soundID == 3 ):
		sndInst = SoundInstance(sound3);
	elif( soundID == 4 ):
		sndInst = SoundInstance(sound4);
	elif( soundID == 5 ):
		sndInst = SoundInstance(sound5);
	sndInst.play()

def getSoundEnvelope(objPos, max, baseVolume ):
	camPos = cam.getPosition()
	dist = math.sqrt((camPos.x - objPos.x)**2 + (camPos.y - objPos.y)**2 + (camPos.z - objPos.z)**2)
	newVol = ( 1 - (dist / max)) * baseVolume
	if( newVol > 1 or newVol < 0 ):
		newVol = 0
	return newVol
	
#--------------------------------------------------------------------------------------------------
stopLightTime = 20
stopLightTimer = stopLightTime
lightState = 0
playStopLight = True

camMoveVector = Vector3(0,0,0)
camMoveLastVector = Vector3(0,0,0)
walking = False

canvasRotation = 0
def onUpdate(frame, t, dt):
	global camMoveVector
	global camMoveLastVector
	global walking
	
	camMoveVector = cam.getPosition() - camMoveLastVector
	
	# Check the velocity of the camera and play walking sound if moving
	if( camMoveVector.x != 0 and camMoveVector.y != 0 and camMoveVector.z != 0 ):
		if( not walking ):
			startWalk()
			walking = True
	else:
		stopWalk()
		walking = False
	
	cam.getController().setSpeed(camSpeed)
	
	if( cam.getPosition().x > 30 ):
		envSetReverb(0.7)
	else:
		envSetReverb(0.0)
		
	movePos = cam.getPosition()
	movePos.y = 0 # Keep camera on ground
	cam.setPosition(movePos)
	
	camMoveLastVector = cam.getPosition();
	#if( walkInst is not None ):
	#	walkInst.setPosition(cam.getPosition())
		
	# Fade between two sounds every 'stopLightTime' seconds
	global playStopLight
	global stopLightTimer
	global lightState
	
	# Rotating canvas
	global canvasModel
	global canvasRotation
	
	rotateSpeed = 0.5
	
	if( playStopLight ):
		if( stopLightTimer > 0 ):
			stopLightTimer -= dt
			if( lightState == 0 ):
				if( canvasRotation < 3.14159 ):
					canvasRotation += dt * rotateSpeed
			if( lightState == 1 ):
				if( canvasRotation > 0 ):
					canvasRotation -= dt * rotateSpeed
					
			#print canvasRotation
			q = Quaternion.new_rotate_axis(canvasRotation, Vector3(0, 0, 1))
			canvasModel.setOrientation(q)
		else:
			stopLightTimer = stopLightTime
			if( lightState == 1 ):
				quietStreetSI.fade( 1.0, 2 )
				loudStreetSI.fade( 0.0, 2 )
				lightState = 0
			else:
				loudStreetSI.fade( 1.0, 2 )
				quietStreetSI.fade( 0.0, 2 )
				lightState = 1
	else:
		loudStreetSI.fade( 0.0, 2 )
		quietStreetSI.fade( 0.0, 2 )
	
	# Very simple sound falloff implementation
	si_waterfall.setVolume( getSoundEnvelope(si_waterfall.getPosition(), 30, 1.0) )
	si_bigben.setVolume( getSoundEnvelope(si_bigben.getPosition(), 60, 1.0) )
	
#--------------------------------------------------------------------------------------------------
def onEvent():
	global playStopLight
	global moveVector
	
	e = getEvent()
	if(e.getServiceType() == ServiceType.Wand):
		
		#if(e.isButtonDown( EventFlags.Button3 )): # Cross
		#if(e.isButtonDown( EventFlags.Button2 )): # Circle

		#if(e.isButtonDown( EventFlags.Button6 )): # Analog Button (L3)
		#if(e.isButtonUp( EventFlags.Button6 )):
			
		if(e.isButtonDown( EventFlags.ButtonLeft )):
			playStopLight = True
		if(e.isButtonDown( EventFlags.ButtonRight )):
			playStopLight = False
			
		#if(e.isButtonDown( EventFlags.ButtonUp )):
		#if(e.isButtonDown( EventFlags.ButtonDown )):

#--------------------------------------------------------------------------------------------------
setUpdateFunction(onUpdate)
setEventFunction(onEvent)