# define min requirements
cmake_minimum_required(VERSION 2.6)

#set files
SET(Sources main.cxx cerebroView_CAVE.cxx)
SET(Headers cerebroView_CAVE.h)

#define the executable
ADD_EXECUTABLE(cerebroView_CAVE ${Sources} ${Headers})

SET_TARGET_PROPERTIES(cerebroView_CAVE PROPERTIES FOLDER apps)

TARGET_LINK_LIBRARIES(cerebroView_CAVE
	omega 
	omegaToolkit
	omegaVtk
	vtkRendering
)
