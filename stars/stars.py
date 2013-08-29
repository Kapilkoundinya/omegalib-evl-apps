from cyclops import *
import csv

starDataPath = "hyparcusxyz.csv"

starModel = ModelGeometry.create('stars')
getSceneManager().addModel(starModel)
getSceneManager().setBackgroundColor(Color('black'))

numStars = 0

def createStar(data, i):
	stx = float(data[3])
	sty = float(data[4])
	stz = float(data[5])
	mag = float(data[1])
	spec = data[2]
	
	starModel.addVertex(Vector3(stx, sty, stz))
	c = Color(1,1,1,1)
	if(len(spec) > 0):
		if(spec[0] == 'O'): c = Color('0xffbfbf')
		elif(spec[0] == 'B'): c = Color('0xffcfcf')
		elif(spec[0] == 'A'): c = Color('0xffdfdf')
		elif(spec[0] == 'F'): c = Color('0xffefef')
		elif(spec[0] == 'G'): c = Color('0xdfffff')
		elif(spec[0] == 'K'): c = Color('0xdfdfff')
		elif(spec[0] == 'M'): c = Color('0x8fbfff')
	c.alpha = mag
	starModel.addColor(c)


def load():
	i = 0
	with open(starDataPath, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		headerLine = True
		for row in reader:
			if(not headerLine):
				createStar(row, i)
			else:
				headerLine = False
			i+=1
	global numStars
	numStars = i
	starModel.addPrimitive(PrimitiveType.Points, 0, numStars)

load()

# create the star shader
starProgram = ProgramAsset()
starProgram.name = "stars"
starProgram.vertexShaderName = "star.vert"
starProgram.fragmentShaderName = "star.frag"
starProgram.geometryShaderName = "star.geom"
starProgram.geometryOutVertices = 4
starProgram.geometryInput = PrimitiveType.Points
starProgram.geometryOutput = PrimitiveType.TriangleStrip
getSceneManager().addProgram(starProgram)

# create the stars
sky = StaticObject.create('stars')
sky.getMaterial().setProgram('stars')
sky.getMaterial().setTransparent(True)
sky.getMaterial().setAdditive(True)
sky.getMaterial().setDepthTestEnabled(True)

