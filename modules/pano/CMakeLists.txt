add_library(pano SHARED Pano.cpp)
target_link_libraries(pano cyclops omega omegaToolkit omegaOsg)

# set correct, os-dependent module name
if(OMEGA_OS_WIN)
	set_target_properties(pano PROPERTIES FOLDER modules SUFFIX ".pyd")
elseif(OMEGA_OS_LINUX)
	set_target_properties(pano PROPERTIES FOLDER modules PREFIX "")
endif()

