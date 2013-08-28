# A measuring tape tool with movable ends.
from math import *
from euclid import *
from omega import *
from omegaToolkit import *
from omega import *
from cyclops import *
from omegaVtk import *

vtkModule = VtkModule.createAndInitialize()

import vtk
import csv

sondeDropsFile = "SondeAndPickedBathymetry-19July13.csv"
sondeDropsDir = "D:/Workspace/omegalib/apps/endurance/data"
sondeDropsPath = sondeDropsDir + "/" + sondeDropsFile

points = vtk.vtkPoints()
polys = vtk.vtkCellArray()
depthData = vtk.vtkFloatArray()
depthData.SetName('depth')
pointsPoly = vtk.vtkPolyData()
delny = vtk.vtkDelaunay2D()
contour = vtk.vtkContourFilter()
mapper = vtk.vtkDataSetMapper()
pointsMapper = vtk.vtkDataSetMapper()

actor = vtk.vtkActor()
ptactor = vtk.vtkActor()

node = SceneNode.create('contours')

setNearFarZ(1, 100000)

c = getDefaultCamera()
c.getController().setSpeed(1000)
c.setPosition(500,0,3000)

getSceneManager().setBackgroundColor(Color('black'))

#------------------------------------------------------------------------------
def createSondeDrop(i, data):
	stname = str(data[0])
	stx = float(data[3])
	sty = float(data[2])
	stx -= 1371377
	sty -= 435670
	depth = float(data[4])
	
	label = Text3D.create('fonts/arial.ttf', 20, stname)
	label.setPosition(sty, stx, 2)
	label.setFixedSize(True)
	label.setFontSize(26)
	label.setColor(Color('yellow'))
	
	points.InsertPoint(i, sty, stx, depth) 
	polys.InsertNextCell(1)
	polys.InsertCellPoint(i)
	depthData.InsertValue(i, depth)
	print(Vector3(stx,depth,sty))
	
#------------------------------------------------------------------------------
def createShorePoint(i, data):
	stx = float(data[0])
	sty = float(data[1])
	stx -= 1371377
	sty -= 435670
	depth = float(data[2])
	
	points.InsertPoint(i, sty, stx, depth) 
	polys.InsertNextCell(1)
	polys.InsertCellPoint(i)
	depthData.InsertValue(i, depth)
	
#------------------------------------------------------------------------------
def createContours():
	points.ComputeBounds()
	pointsPoly.SetPoints(points)
	pointsPoly.SetPolys(polys)
	pointsPoly.GetPointData().AddArray(depthData)
	pointsPoly.GetPointData().SetActiveScalars('depth')
	pointsPoly.Update()
	delny.SetInput(pointsPoly)
	delny.SetTolerance(0.001)
	delny.Update()
	contour.SetInputConnection(delny.GetOutputPort())
	contour.GenerateValues(50, 1, 50)
	mapper.SetInputConnection(contour.GetOutputPort())
	mapper.ScalarVisibilityOff()
	actor.SetMapper(mapper)
	actor.GetProperty().SetColor(255, 255, 255)
	actor.GetProperty().SetRepresentationToWireframe()
	vtkAttachProp(actor, node)
	
	pointsMapper.SetInputConnection(delny.GetOutputPort())
	pointsMapper.ScalarVisibilityOff()
	ptactor.SetMapper(pointsMapper)
	ptactor.GetProperty().SetColor(1, 0.2, 1)
	ptactor.GetProperty().SetRepresentationToPoints()
	ptactor.GetProperty().SetPointSize(10)
	vtkAttachProp(ptactor, node)


	
#------------------------------------------------------------------------------
def load():
	with open(sondeDropsPath, 'rU') as csvfile:
		reader = csv.reader(csvfile)
		headerLine = True
		i = 0
		for row in reader:
			if(not headerLine):
				print(i)
				createSondeDrop(i, row)
				i += 1
			else:
				headerLine = False
	with open(sondeDropsDir + '/WLB_shoreline.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			createShorePoint(i, row)
			i += 1
	createContours()

#------------------------------------------------------------------------------
# addpt - adds point to contur map
def addpt(x, y, depth):
	id = points.InsertNextPoint(x, y, depth) 
	points.Modified()
	polys.InsertNextCell(1)
	polys.InsertCellPoint(id)
	depthData.InsertValue(id, depth)
	print("Point Added: " + str(id) + "  -  " + str(Vector3(x, y, depth)))

#------------------------------------------------------------------------------
# ctint - set contour interval (in meters)
def ctint(interval):
	num = 40 / interval
	contour.GenerateValues(num, 1, 40)

	
load()
