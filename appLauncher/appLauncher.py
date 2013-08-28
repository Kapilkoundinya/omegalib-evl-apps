from math import *
from euclid import *
from omega import *
from omegaToolkit import *

import os

#------------------------------------------------------------------------------
# configuration
appHome = "D:/Workspace/omegalib/apps"

# dictionary of loaded models. will be filled up by the onModelLoaded function
appButtons = {}

# setup menu
mm = MenuManager.createAndInitialize()
menu = mm.getMainMenu()

# populate the applications menu.
for filename in os.listdir(appHome):
	filePath = appHome + "/" + filename
	# Skip hidden files and directories
	if(not filename.startswith('.')):
		if(os.path.isdir(filePath)):
			appmnu = menu.addSubMenu(filename)
			appmnu.addButton("Start", "startApp('" + filename + "')")
			umnu = appmnu.addSubMenu("Uninstall")
			umnu.addLabel("Are you sure?")
			umnu.addButton("No", "menu.close()") # we should just go back one level..
			umnu.addButton("Yes", "uninstallApp(" + filename + ")")

			
def startApp(appname):
	filePath = appHome + "/" + appname + "/" + appname + ".py"
	print("Running " + filePath)
	queueCommand(':r! ' + filePath)


def uninstallApp(appname):
	print("NOT IMPLEMENTED")