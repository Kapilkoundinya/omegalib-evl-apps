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

#------------------------------------------------------------------------------
# GLSL uniforms shared by all loaded dives
pointScale = Uniform.create('pointScale', UniformType.Float, 1)
globalAlpha = Uniform.create('globalAlpha', UniformType.Float, 1)
minDepth = Uniform.create('unif_MinDepth', UniformType.Float, 1)
maxDepth = Uniform.create('unif_MaxDepth', UniformType.Float, 1)
minDepth.setFloat(10)
maxDepth.setFloat(50.0)
pointScale.setFloat(0.02)
globalAlpha.setFloat(1.0)	

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
		self.diveModel.options = "xyzrgba -d " + str(decimation)
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
		mat.attachUniform(globalAlpha)
		mat.attachUniform(minDepth)
		mat.attachUniform(maxDepth)
	
	