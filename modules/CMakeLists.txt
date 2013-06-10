# General module section
#flipbookPlayer
set(MODULES_ENABLE_FLIPBOOK_PLAYER true CACHE BOOL "Enables module flipbookPlayer.")
if(MODULES_ENABLE_FLIPBOOK_PLAYER)
	add_subdirectory(flipbookPlayer)
endif()

# In this section, add modules that require OpenSceneGraph support
if(OMEGA_BUILD_OSG_LIB)
	#pano
	set(MODULES_ENABLE_PANO false CACHE BOOL "Enables module pano.")
	if(MODULES_ENABLE_PANO)
		add_subdirectory(pano)
	endif()
endif()
