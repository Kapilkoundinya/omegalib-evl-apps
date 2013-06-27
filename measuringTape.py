# A measuring tape tool with movable ends.
from math import *
from euclid import *
from omega import *
from omegaToolkit import *
from cyclops import *

class MeasuringTape(Actor):
	startHandle = None
	startText = None
	endHandle = None
	endText = None
	body = None
	bodyLine = None
	bodyText = None
	interactor = None
	
	#--------------------------------------------------------------------------
	def __init__(self):
		super(MeasuringTape, self).__init__("measuringTape")
		
		self.startHandle = SphereShape.create(0.1, 2)
		self.endHandle = SphereShape.create(0.1, 2)
		self.startText = Text3D.create('fonts/arial.ttf', 0.05, 'start')
		self.startHandle.addChild(self.startText)
		self.endText = Text3D.create('fonts/arial.ttf', 0.05, 'end')
		self.endHandle.addChild(self.endText)
		self.body = LineSet.create()
		self.bodyLine = self.body.addLine()
		self.bodyLine.setThickness(0.1)
		self.bodyText = Text3D.create('fonts/arial.ttf', 0.1, 'length')
		
		self.setEventsEnabled(True)
		self.setUpdateEnabled(True)
		
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
		
	#--------------------------------------------------------------------------
	def dispose(self):
		print('Deleting measuring tape')
		
	#--------------------------------------------------------------------------
	def onUpdate(self, frame, time, dt):
		#self.startText.setFacingCamera(getDefaultCamera())
		s = self.startHandle.getPosition()
		e = self.endHandle.getPosition()
		self.startText.setText(str(s))
		self.endText.setText(str(e))
		self.bodyLine.setStart(s)
		self.bodyLine.setEnd(e)
		length = str((s - e).magnitude())
		self.bodyText.setText(length)
		self.bodyText.setPosition((s + e) / 2)
		
	#--------------------------------------------------------------------------
	def onEvent(self):
		e = getEvent()
		if(e.isButtonDown(EventFlags.Button1)):
			r = getRayFromEvent(e)
			hitData = hitNode(self.startHandle, r[1], r[2])
			if(hitData[0]):
				self.interactor.setSceneNode(self.startHandle)
			hitData = hitNode(self.endHandle, r[1], r[2])
			if(hitData[0]):
				self.interactor.setSceneNode(self.endHandle)
