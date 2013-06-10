from euclid import *
from omega import *
from omegaToolkit import *
from cyclops import *

light = Light.create()
light.setColor(Color("white"))
light.setAmbient(Color("#404020"))
light.setPosition(Vector3(0, 10, 0))
light.setEnabled(True)

light2 = Light.create()
light2.setColor(Color("#202040"))
light2.setPosition(Vector3(0, -10, 0))
light2.setEnabled(True)

light3 = Light.create()
light3.setColor(Color("#503030"))
light3.setPosition(Vector3(10, 0, 0))
light3.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

defScale = Vector3(0.01, 0.01, 0.01)
defPos = Vector3(0, 1, -2)

interactor = ToolkitUtils.setupInteractor("config/interactor")
rt = SceneNode.create('root')
getScene().addChild(rt)
rt.setPosition(Vector3(-2.28, -0.76, 0.35))
rt.setScale(Vector3(1.4, 1.4, 1.4))
interactor.setSceneNode(rt)

# sequence 1
seq1Model = ModelInfo()
seq1Model.name = "seq1"
seq1Model.path = "surganim/data/surgseq1.fbx"
seq1Model.usePowerOfTwoTextures = False
scene.loadModel(seq1Model)
seq1 = AnimatedObject.create("seq1")
seq1.setScale(defScale)
seq1.setPosition(defPos)
seq1.setVisible(False)
seq1.setEffect("textured")
rt.addChild(seq1)

# sequence 1
seq2Model = ModelInfo()
seq2Model.name = "seq2"
seq2Model.path = "surganim/data/surgseq2.fbx"
seq2Model.usePowerOfTwoTextures = False
scene.loadModel(seq2Model)
seq2 = AnimatedObject.create("seq2")
seq2.setScale(defScale)
seq2.setPosition(defPos)
seq2.setVisible(False)
seq2.setEffect("textured")
rt.addChild(seq2)

seq3Model = ModelInfo()
seq3Model.name = "seq3"
seq3Model.path = "surganim/data/surgseq3.fbx"
seq3Model.usePowerOfTwoTextures = False
scene.loadModel(seq3Model)
seq3 = AnimatedObject.create("seq3")
seq3.setScale(defScale)
seq3.setPosition(defPos)
seq3.setVisible(False)
seq3.setEffect("textured")
rt.addChild(seq3)

seq4Model = ModelInfo()
seq4Model.name = "seq4"
seq4Model.path = "surganim/data/surgseq4.fbx"
seq4Model.usePowerOfTwoTextures = False
scene.loadModel(seq4Model)
seq4 = AnimatedObject.create("seq4")
seq4.setScale(defScale)
seq4.setPosition(defPos)
seq4.setVisible(False)
seq4.setEffect("textured")
rt.addChild(seq4)

# setup menu
mm = MenuManager.createAndInitialize()
menu = mm.createMenu("main")
mm.setMainMenu(menu)

mnui = menu.addItem(MenuItemType.Button)
mnui.setText("Start Animation 1")
mnui.setCommand("playseq1()")

mnui = menu.addItem(MenuItemType.Button)
mnui.setText("Start Animation 2")
mnui.setCommand("playseq2()")

mnui = menu.addItem(MenuItemType.Button)
mnui.setText("Start Animation 3")
mnui.setCommand("playseq3()")

mnui = menu.addItem(MenuItemType.Button)
mnui.setText("Start Animation 4")
mnui.setCommand("playseq4()")

skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/grid4", "png")
#scene.setSkyBox(skybox)
scene.setBackgroundColor(Color('#202020'))
scene.displayWand(0, 1)

def playseq1():
	# Set the first sequence as visible and start playback.
	# The other sequences will be triggered in the OnAnimationEnded events
	seq2.setVisible(False)
	seq3.setVisible(False)
	seq4.setVisible(False)
	seq1.playAnimation(0)
	seq1.setVisible(True)

def playseq2():
	seq1.setVisible(False)
	seq3.setVisible(False)
	seq4.setVisible(False)
	seq2.playAnimation(0)
	seq2.setVisible(True)
	
def playseq3():
	seq1.setVisible(False)
	seq2.setVisible(False)
	seq4.setVisible(False)
	seq3.playAnimation(0)
	seq3.setVisible(True)
	
def playseq4():
	seq1.setVisible(False)
	seq2.setVisible(False)
	seq3.setVisible(False)
	seq4.playAnimation(0)
	seq4.setVisible(True)
