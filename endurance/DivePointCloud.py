from math import *
from euclid import *
from omega import *
from cyclops import *
from pointCloud import *

#------------------------------------------------------------------------------
# Load GLSL shaders used to render dive point clouds
shaderPath = "./shaders";

programDepthColor = ProgramAsset()
programDepthColor.name = "points"
programDepthColor.vertexShaderName = shaderPath + "/SphereDepthColor.vert"
programDepthColor.fragmentShaderName = shaderPath + "/SphereDepthColor.frag"
programDepthColor.geometryShaderName = shaderPath + "/Sphere.geom"
programDepthColor.geometryOutVertices = 4
programDepthColor.geometryInput = PrimitiveType.Points
programDepthColor.geometryOutput = PrimitiveType.TriangleStrip
getSceneManager().addProgram(programDepthColor)

programDepthColorSimple = ProgramAsset()
programDepthColorSimple.name = "points-simple"
programDepthColorSimple.vertexShaderName = shaderPath + "/SphereDepthColorSimple.vert"
programDepthColorSimple.fragmentShaderName = shaderPath + "/SphereDepthColorSimple.frag"
getSceneManager().addProgram(programDepthColorSimple)

#------------------------------------------------------------------------------
# GLSL uniforms shared by all loaded dives
pointScale = Uniform.create('pointScale', UniformType.Float, 1)
minDepth = Uniform.create('unif_MinDepth', UniformType.Float, 1)
maxDepth = Uniform.create('unif_MaxDepth', UniformType.Float, 1)

minBox = Uniform.create('unif_MinBox', UniformType.Vector3f, 1)
maxBox = Uniform.create('unif_MaxBox', UniformType.Vector3f, 1)

minAttrib = Uniform.create('unif_MinAttrib', UniformType.Vector3f, 1)
maxAttrib = Uniform.create('unif_MaxAttrib', UniformType.Vector3f, 1)

w1 = Uniform.create('unif_W1', UniformType.Float, 1)
w2 = Uniform.create('unif_W2', UniformType.Float, 1)
w3 = Uniform.create('unif_W3', UniformType.Float, 1)
w4 = Uniform.create('unif_W4', UniformType.Float, 1)

minDepth.setFloat(10)
maxDepth.setFloat(50.0)
pointScale.setFloat(0.02)

minBox.setVector3f(Vector3(-100000,-100000,-100000))
maxBox.setVector3f(Vector3(100000,100000,100000))

w1.setFloat(1)
w2.setFloat(0)
w3.setFloat(0)
w4.setFloat(0)

# table of all loaded dives
dpcmap = {}

#------------------------------------------------------------------------------
class DivePointCloud:
	rootNode = None
	diveNode = None
	name = ''
	filename = ''
	loaded = False
	diveModel = None
	diveInfo = None
	
	#--------------------------------------------------------------------------
	def __init__(self, root, name):
		self.rootNode = root
		self.name = name
	
	#--------------------------------------------------------------------------
	def load(self, file, decimation):
		self.filename = file
		scene = getSceneManager()
		self.diveModel = ModelInfo()
		self.diveModel.name = self.name
		self.diveModel.path = file
		self.diveModel.optimize = True
		self.diveModel.options = "xyzrgba -d " + str(decimation) + " -b 1000"
		
		scene.loadModel(self.diveModel)
		self.diveLoaded(self.diveModel.name)
			
	def diveLoaded(self, name):
		segment = StaticObject.create(name)
		segment.setEffect("points")
		self.diveNode = segment
		self.rootNode.addChild(segment)
		
		# parse loader results
		self.diveInfo = eval(self.diveModel.loaderOutput)
		
		# attach shader uniforms
		mat = segment.getMaterial()
		mat.attachUniform(pointScale)
		mat.attachUniform(minDepth)
		mat.attachUniform(maxDepth)
		mat.attachUniform(minBox)
		mat.attachUniform(maxBox)
		mat.attachUniform(w1)
		mat.attachUniform(w2)
		mat.attachUniform(w3)
		mat.attachUniform(w4)
		mat.attachUniform(minAttrib)
		mat.attachUniform(maxAttrib)
	
	