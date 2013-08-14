from omega import *
from flipbookPlayer import *

# setImageLoaderThreads(3)
# movieDir = "/data/evl/kreda/movies/glass_3d/" + getHostname()
# player = FlipbookPlayer.createAndInitialize();
# #player.load(movieDir + "/frame_%06d.jpg", 2000, 600);
# player.loadMultidir(movieDir + "/%04d/frame_%04d.jpg", 4000, 3, 2046, 0);
# player.setFramesToBuffer(100)
# player.setFrameTime(0.1)
# player.setNumGpuBuffers(2)
# player.setPlaybackBarVisible(True)
# player.play()

player = None

def run():
	# Do not playback on master node.
	if(not isMaster()):
		global player
		setImageLoaderThreads(32)

		movieDir = "/iridium_SSD/kreda/movies/anp_3d/" + getHostname() 
		#movieDir = "/iridium_SSD/kreda/movies/organic_3d/" + getHostname() 

		player = FlipbookPlayer.createAndInitialize();

		player.loadMultidir(movieDir + "/%04d/frame_%06d.jpg", 2000, 1, 2046, 0);
		#player.loadMultidir(movieDir + "/%04d/frame_%04d.jpg", 4000, 3, 2046, 0);
		player.setFramesToBuffer(300)
		player.setFrameTime(0.001)
		player.setNumGpuBuffers(2)
		player.setPlaybackBarVisible(True)
		player.play()

#	#toggleStats('t0x0 t1x0 t2x0 t3x0 t4x0 t5x0')
#	queueCommand(':f')
#	#queueCommand(':c')

#	# Setup soundtrack
#	se = getSoundEnvironment()
#	if se != None:
#		music = se.loadSoundFromFile('music', '/Users/evldemo/sounds/music/filmic.wav')
#		simusic = SoundInstance(music)
#		simusic.setPosition(Vector3(0, 2, -1))
#		simusic.setLoop(True)
#		simusic.setReverb(0.1)
#		simusic.setMix(0.1)
#		simusic.setWidth(18)
#		simusic.setVolume(0.1)
#		simusic.playStereo()

