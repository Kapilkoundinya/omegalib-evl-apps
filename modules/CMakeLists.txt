# General module section
# In this section, add modules that require OpenSceneGraph support
if(OMEGA_BUILD_OSG_LIB)
	#pano
	set(MODULES_ENABLE_PANO false CACHE BOOL "Enables module pano.")
	if(MODULES_ENABLE_PANO)
		add_subdirectory(pano)
	endif()
endif()
