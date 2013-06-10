add_library(flipbookPlayer SHARED flipbookPlayer.cpp)
target_link_libraries(flipbookPlayer omega)

set_target_properties(flipbookPlayer PROPERTIES PREFIX "")
if(WIN32)
	set_target_properties(flipbookPlayer PROPERTIES FOLDER modules SUFFIX ".pyd")
endif()
