# startup script for orun
# NOTE: identifiers that start with `_` are considered system-level: they will not be deleted
# during application switches or when calling OmegaViewer.reset(). They will also be accessible from all
# scripts.
from omegaViewer import *
from omegaToolkit import *
from euclid import *

colorWidget = None

def _onLauncherStart():
	mm = MenuManager.createAndInitialize()
	sysmnu = mm.getMainMenu().addSubMenu("Applications")
	
	# default icon size
	ics = Vector2(64, 64)
	
	mi = sysmnu.addButton("ENDURANCE", "_startApp('./endurance/endurancePoints.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)

	mi = sysmnu.addButton("Connectome", "_startApp('./connectome/connectome.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)
	
	mi = sysmnu.addButton("Brain", "_startApp('./brain2/brain2.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)
	
	mi = sysmnu.addButton("Baybridge", "_startApp('./baybridge/baybridge.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)
	
	mi = sysmnu.addButton("Model Viewer", "_startApp('./modelView2/modelView.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)
	
	mi = sysmnu.addButton("Enterprise", "_startApp('./enterprise/enterprise.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)
	
	mi = sysmnu.addButton("Molecule", "_startApp('./molecule/molecule.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)
	
	mi = sysmnu.addButton("Mars", "_startApp('./mars/mars.py')")
	i = loadImage("app.png")
	mi.setImage(i)
	mi.getButton().getImage().setSize(ics)
	
def _startApp(appScript):
	queueCommand(':r! ' + appScript)
	
# append _onLauncherStart to the current application start command.
# This function will be called when an application starts.
v = getViewer()
v.setAppStartCommand(v.getAppStartCommand() + "; from euclid import *; _onLauncherStart()")

_onLauncherStart()
	