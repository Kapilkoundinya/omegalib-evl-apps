# startup script for orun
# NOTE: variables that start with `_` are considered system-level variables: they will not be deleted
# during application switches or when calling OmegaViewer.reset(). They will also be accessible from all
# scripts.
from omegaViewer import *

_viewer = getViewer()
_drawer = _viewer.getAppDrawer()

_viewer.setAppDrawerToggleButton(EventFlags.Button4)

# Set the default scale of the drawer
_drawer.setDrawerScale(2.0)
# Set the default icon size
_drawer.setIconSize(128)

panoramaApp = AppInfo()
panoramaApp.name = "panorama"
panoramaApp.label = "Panorama Viewer"
panoramaApp.iconFile = "panorama/appIcon.png"
_drawer.addApp(panoramaApp)

surganimApp = AppInfo()
surganimApp.name = "surganim"
surganimApp.label = "Medical Animation"
surganimApp.iconFile = "surganim/appIcon.png"
_drawer.addApp(surganimApp)

modelViewApp = AppInfo()
modelViewApp.name = "modelView"
modelViewApp.label = "Model Viewer"
modelViewApp.iconFile = "modelView/appIcon.png"
_drawer.addApp(modelViewApp)

enterpriseApp = AppInfo()
enterpriseApp.name = "enterprise"
enterpriseApp.label = "Enterprise"
enterpriseApp.iconFile = "enterprise/appIcon.png"
_drawer.addApp(enterpriseApp)

brainApp = AppInfo()
brainApp.name = "brain"
brainApp.label = "Brain Vasculature"
brainApp.iconFile = "brain/appIcon.png"
_drawer.addApp(brainApp)

brain2App = AppInfo()
brain2App.name = "brain2"
brain2App.label = "Brain Vasculature 2"
brain2App.iconFile = "brain2/appIcon.png"
_drawer.addApp(brain2App)

baybridgeApp = AppInfo()
baybridgeApp.name = "baybridge"
baybridgeApp.label = "Bay Bridge Structure"
baybridgeApp.iconFile = "baybridge/appIcon.png"
_drawer.addApp(baybridgeApp)

# vtkApp = AppInfo()
# vtkApp.name = "vtkdemos/Sample"
# vtkApp.label = "Vtk Demo 1"
# vtkApp.iconFile = "vtkdemos/vtkIcon.png"
# _drawer.addApp(vtkApp)

#_scene = getSceneManager()
#_scene.displayWand(0, 0)

# Uncomment to start the specified application by default
#viewer.run("panorama")
