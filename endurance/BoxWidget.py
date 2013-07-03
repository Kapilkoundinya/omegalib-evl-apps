# A measuring tape tool with movable ends.
from math import *
from euclid import *
from omega import *
from omegaToolkit import *
from cyclops import *

class BoxWidget(Actor):
	root = None
	frame = None
	frameLines = []
	planes = []
	min = None
	max = None
	color + None
	
	#--------------------------------------------------------------------------
	def __init__(self, min, max, color):
		super(BoxWidget, self).__init__("boxwidget")
		
		self.frame = LineSet.create()
		self.bodyLine = self.body.addLine()
		self.bodyLine.setThickness(0.1)
		self.bodyText = Text3D.create('fonts/arial.ttf', 0.1, 'length')
		
		self.setEventsEnabled(False)
		self.setUpdateEnabled(False)
		
		self.interactor = ToolkitUtils.setupInteractor('config/interactor')
		
		# set initial handle positions.
		self.startHandle.setPosition(Vector3(-1,2,-4))
		self.endHandle.setPosition(Vector3(1,2,-4))
		
		# Set visual properties
		self.startHandle.setEffect('colored -e blue')
		self.endHandle.setEffect('colored -e blue')
		self.body.setEffect('colored -e #000060')
		self.startText.getMaterial().setDepthTestEnabled(False)
		self.endText.getMaterial().setDepthTestEnabled(False)
		self.bodyText.getMaterial().setDepthTestEnabled(False)
		#self.endText.setFacingCamera(getDefaultCamera())
		