from math import *
from euclid import *
from omega import *
from cyclops import *

#--------------------------------------------------------------------------------------------------
# Scene Setup

light = Light.create()
light.setColor(Color("#ABABAB"))
light.setAmbient(Color("#020202"))
light.setPosition(Vector3(0, 50, -5))
light.setEnabled(True)

scene = getSceneManager()
scene.setMainLight(light)

# setup skybox
skybox = Skybox()
skybox.loadCubeMap("common/cubemaps/stars1", "png")
scene.setSkyBox(skybox)

#--------------------------------------------------------------------------------------------------
# Sound Setup

# Get the sound environment
env = getSoundEnvironment()

# If this is not set, you will have to set an absolute path below
# Note: The CAVE2 Audio Server assumes sound are in '/Users/evldemo/sounds/'
# and will append that file path to any additional paths
# All file path here are for the sound server!
env.setAssetDirectory("soundExample"); # Suggestion: use your application name

# Using s_ to denote a sound object verses a sound instance (si_)
# This looks for a sound file at '.../appDirectory/laser.wav'
# And will transfer it to the sound server at '/Users/evldemo/sounds/soundExample/laser.wav'
# Note that the assetDirectory path 'soundExample' has been added only on the sound server
s_laser = env.loadSoundFromFile("laser", "laser.wav");

# This looks for a sound file at '.../appDirectory/music/FrozenStar.wav'
# And will transfer it to the sound server at '/Users/evldemo/sounds/soundExample/music/FrozenStar.wav'
s_music = env.loadSoundFromFile("music", "/music/FrozenStar.wav");
s_combatMusic = env.loadSoundFromFile("music", "/music/FailingDefense.wav");

# Here we could replace the default menu sounds specified in the Omegalib configuration file for our application 
s_menuShow = env.loadSoundFromFile("showMenuSound", "/my_menu/show.wav");
s_menuHide = env.loadSoundFromFile("hideMenuSound", "/my_menu/hide.wav");
s_menuSelect = env.loadSoundFromFile("selectMenuSound", "/my_menu/select.wav");
s_menuScroll = env.loadSoundFromFile("scrollMenuSound", "/my_menu/scroll.wav");

# Set the volume scale of the menu sounds (0.0 - 1.0, default: 0.5)
s_menuShow.setVolumeScale(0.2)
s_menuHide.setVolumeScale(0.2)
s_menuSelect.setVolumeScale(0.2)
s_menuScroll.setVolumeScale(0.2)

# Play some background music at startup
# playStereo() is for ambient music and plays in a fixed left/right channel configuration
si_music = SoundInstance(s_music)
si_combatMusic = SoundInstance(s_combatMusic)

# Play our initial background looping music at the application start
si_music.setVolume(0.5)
si_music.setLoop(True)
si_music.playStereo()

# Starts playing muted. We'll fade to this sound later
si_combatMusic.setVolume(0)
si_combatMusic.setLoop(True)
si_combatMusic.playStereo()


s_music5 = env.loadSoundFromFile('music5', '/music/TMP-MainTitle.wav')
si_music5 = SoundInstance(s_music5)
#--------------------------------------------------------------------------------------------------
def fadeToCombatMusic():
	# Fade from current volume to 0 over 3 seconds
	si_music.fade( 0.0, 3 )
	
	# Stop and play from beginning
	# Calling play() or playStereo() on a play sound will stop/rewind/start it
	#si_combatMusic.playStereo()
	
	# Fade from current volume to 0.4 over 5 second
	si_combatMusic.fade( 0.4, 5 )

#--------------------------------------------------------------------------------------------------
def fadeToCalmMusic():
	# Fade from current volume to 0 over 3 seconds
	si_music.fade( 0.5, 3 )
	
	# Fade from current volume to 0.4 over 3 seconds
	si_combatMusic.fade( 0.0, 3 )

#--------------------------------------------------------------------------------------------------
def toggleMusic():
	if( si_music.isPlaying() ):
		# Immediately stop all music
		si_music.stop()
		si_combatMusic.stop()
	else:
		# Start all music
		si_music.playStereo()
		si_combatMusic.playStereo()
	
#--------------------------------------------------------------------------------------------------
# Menu
mm = MenuManager.createAndInitialize()

# Get the default menu (System menu)
menu = mm.getMainMenu()
mm.setMainMenu(menu)

musicMenu = mm.createMenu("musicMenu")
musicMenu = menu.addSubMenu("Music")

toggleMusButton = musicMenu.addButton("Enable music", "toggleMusic()")
combatButton = musicMenu.addButton("Combat music", "fadeToCombatMusic()")
calmButton = musicMenu.addButton("Calm music", "fadeToCalmMusic()")


# Set menu as checkable radio buttons
combatButton.getButton().setCheckable(True)
calmButton.getButton().setCheckable(True)
toggleMusButton.getButton().setCheckable(True)

combatButton.getButton().setRadio(True)
calmButton.getButton().setRadio(True)

toggleMusButton.getButton().setChecked(True)
calmButton.getButton().setChecked(True)