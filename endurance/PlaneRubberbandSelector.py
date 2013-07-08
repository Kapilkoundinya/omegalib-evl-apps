from math import *
from euclid import *
from omega import *

# set to true to enable the rubber band selector
enabled = False

startPos = Vector2(0,0)
endPos = Vector2(0,0)
startRay = Ray3(Point3(0,0,0), Vector3(0,0,-1))
endRay = Ray3(Point3(0,0,0), Vector3(0,0,-1))
dragging = False

# define a default intersection plane
plane = Plane(Vector3(0,0,1), 0.0)

# these variables hold the final start and end points of the selection
startPoint = Vector3(0, 0, 0)
endPoint = Vector3(0, 0, 0)

# This variable holds the callback that will be invoked when the selection is
# updated. The callback accepts no argument.
selectionUpdatedCallback = None

#------------------------------------------------------------------------------
# Plane intersection computation
def updatePlaneIntersection():
	global startPoint
	global endPoint
	sp = plane.intersect(startRay)
	ep = plane.intersect(endRay)
	if(isinstance(sp, Point3) and isinstance(ep, Point3)):
		startPoint = Vector3(sp.x, sp.y, sp.z)
		endPoint = Vector3(ep.x, ep.y, ep.z)
		# if present, call the selection callback
		if(selectionUpdatedCallback != None):
			selectionUpdatedCallback()

#------------------------------------------------------------------------------
# Draw callback
def onDraw(displaySize, tileSize, camera, painter):
	global dragging
	if(dragging):
		painter.drawRect(startPos, endPos - startPos, Color(0.4, 0.4, 1.0, 0.8))


#------------------------------------------------------------------------------
# Event callback
def handleEvent():
	if(enabled):
		e = getEvent()

		global startPos
		global endPos
		global startRay
		global endRay
		global dragging

		# save wand ray
		if(e.getServiceType() == ServiceType.Pointer):
			if(e.isButtonDown(EventFlags.Button1)):
				dragging = True
				p = e.getPosition()
				startPos = Vector2(p.x, p.y)
				e.setProcessed()
				# save the start ray
				r = getRayFromEvent(e)
				startRay = Ray3(Point3(r[1].x, r[1].y, r[1].z), r[2])
				
			elif(e.getType() == EventType.Up):
				dragging = False
				# update the intersection points
				updatePlaneIntersection()
			else:
				if(dragging):
					p = e.getPosition()
					endPos = Vector2(p.x, p.y)
					e.setProcessed()
					# save the end ray
					r = getRayFromEvent(e)
					endRay = Ray3(Point3(r[1].x, r[1].y, r[1].z), r[2])


# Register the event and draw functions
setEventFunction(handleEvent)
setDrawFunction(onDraw)