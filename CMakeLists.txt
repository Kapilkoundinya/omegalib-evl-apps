# Add modules
add_subdirectory(modules)

# In this section, add applications that require OpenSceneGraph support
if(OMEGA_BUILD_OSG_LIB)
	# railSimmodeshapes
	if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/railSimmodeshapes)
		add_subdirectory(railSimmodeshapes)
	endif()
	# bcc (from John Bell)
	if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/bcc)
		add_subdirectory(bcc)
	endif()
endif()

# In this section, add applications that require VTK support
if(OMEGA_BUILD_VTK_LIB)
	if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/pdbviewer)
		add_subdirectory(pdbviewer)
	endif()
	if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/cerebroView_CAVE)
		add_subdirectory(cerebroView_CAVE)
	endif()
	if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/lglass)
		add_subdirectory(lglass)
	endif()
endif()

