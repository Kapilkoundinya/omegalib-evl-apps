# Basic example showing how to load a static model, and display it in a basic scene.
from math import *
from euclid import *
from omega import *
from cyclops import *

scene = getSceneManager()
scene.createProgramFromString("depthColor", 
# Vertex shader
'''
	@vertexShader
	varying float var_Depth;

	uniform float unif_MaxDepth;
	uniform float unif_MinDepth;
	
	///////////////////////////////////////////////////////////////////////////////////////////////////
	void setupSurfaceData(vec4 eyeSpacePosition)
	{
		//float unif_MaxDepth = 50;
		//float unif_MinDepth = 0;		
		var_Depth = (gl_Vertex.y - unif_MinDepth) / (unif_MaxDepth - unif_MinDepth);
	}
''',
# Fragment shader
'''
	@surfaceShader
	
	uniform float unif_Shininess;
	uniform float unif_Gloss;
	
	varying vec3 var_Normal;
	varying float var_Depth;

	SurfaceData getSurfaceData(void)
	{
		SurfaceData sd;
		//sd.albedo = vec4(0.3, 0.3, 0.3, 1.0);
		sd.albedo.rgb = mix(vec3(0.2, 0.2, 1.0), vec3(1.0, 0.2, 0.2), var_Depth);	
		sd.albedo.a = 1.0;
		sd.emissive = gl_FrontMaterial.emission;
		sd.shininess = unif_Shininess;
		sd.gloss = unif_Gloss;
		sd.normal = normalize(var_Normal);
		
		return sd;
	}
''')

#--------------------------------------------------------------------------------------------------
# Load a static model
lakeModel = ModelInfo()
lakeModel.name = "lake"
lakeModel.path = "data/bonney-all-hires-1m16x.fbx"
lakeModel.size = 2.0
lakeModel.optimize = True
lakeModel.generateNormals = True
lakeModel.normalizeNormals = True
scene.loadModel(lakeModel)

# Create a scene object using the loaded model
lake = StaticObject.create("lake")
#torus.pitch(radians(45))
lake.setEffect("depthColor -C")
#lake.setEffect("colored -d red")
minDepth = lake.getMaterial().addUniform('unif_MinDepth', UniformType.Float)
maxDepth = lake.getMaterial().addUniform('unif_MaxDepth', UniformType.Float)

minDepth.setFloat(0)
maxDepth.setFloat(40)

pivot = SceneNode.create('pivot')
pivot.addChild(lake)
lake.setPosition(-lake.getBoundCenter())
pivot.setPosition(Vector3(0, 2, -4))
pivot.setScale(Vector3(1, 1, 1))

interactor1 = ToolkitUtils.setupInteractor("config/interactor")
interactor1.setSceneNode(pivot)

# second light
light = Light.create()
light.setColor(Color(1.0, 1.0, 1.0, 1))
light.setAmbient(Color(0.2, 0.2, 0.2, 1))
light.setPosition(Vector3(0, 0, 0))
light.setLightType(LightType.Point)
#light.setAmbient(Color(0.1, 0.1, 0.1, 1))
#light.setLightDirection(Vector3(0, -1, 0))
light.setEnabled(True)
getDefaultCamera().addChild(light)

skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/grid3", "png")
scene.setSkyBox(skybox)

globalScale = 10.0
curScale = 1.0

queueCommand(':hint displayWand')

# Event callback
def handleEvent():
	e = getEvent()
	global globalScale
	if(not e.isProcessed()):
		cam = getDefaultCamera()
		if(e.getServiceType() == ServiceType.Mocap and e.getSourceId() == 1):
			light.setPosition(e.getPosition())
		if(e.isButtonDown(EventFlags.ButtonLeft)): 
			cam.setPosition(Vector3(0, -1, 0))
			cam.setYawPitchRoll(Vector3(0, 0, 0))
		if(e.isButtonDown(EventFlags.ButtonUp)): 
			if(cam.isControllerEnabled()): globalScale = globalScale * 2.0
		if(e.isButtonDown(EventFlags.ButtonDown)): 
			if(cam.isControllerEnabled()): globalScale = globalScale / 2.0
		
setEventFunction(handleEvent)

#--------------------------------------------------------------------------------------------------
def onUpdate(frame, time, dt):
	global curScale
	global globalScale
	curScale += (globalScale - curScale) * dt
	if(abs(curScale - globalScale) > 0.01):
		pivot.setScale(Vector3(curScale, curScale, curScale))
		
setUpdateFunction(onUpdate)
