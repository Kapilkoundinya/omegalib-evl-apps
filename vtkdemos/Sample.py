from math import *
from euclid import *
from omega import *
from omegaToolkit import *
from omegaVtk import *

vtkModule = VtkModule.createAndInitialize()

import vtk

vtkNode = SceneNode.create("vtkNode")
vtkNode.setPosition(Vector3(0, 2, -2))

quadric = vtk.vtkQuadric()
quadric.SetCoefficients(.5,1,.2,0,.1,0,0,.2,0,0)

sample = vtk.vtkSampleFunction()
sample.SetSampleDimensions(50,50,50)
sample.SetImplicitFunction(quadric)

contours = vtk.vtkContourFilter()
contours.SetInput(sample.GetOutput())
contours.GenerateValues(6, 0.0, 2)

normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(contours.GetOutputPort())
normals.SetFeatureAngle(270.0)

contMapper = vtk.vtkPolyDataMapper()
contMapper.SetInput(normals.GetOutput())
contMapper.SetScalarRange(0.0, 1.2)
contMapper.SetScalarVisibility(1)
actor = vtk.vtkActor()
actor.SetMapper(contMapper)

vtkAttachProp(actor, vtkNode)

l = vtk.vtkLight()
vtkAddLight(l)
l.PositionalOn()
l.SetPosition(0, 4, 0)
