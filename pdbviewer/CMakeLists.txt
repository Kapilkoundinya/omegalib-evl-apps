add_executable(pdbviewer pdbviewer.cpp)
set_target_properties(pdbviewer PROPERTIES FOLDER apps)
target_link_libraries(pdbviewer
	omega 
	omegaToolkit
    omegaVtk
	cyclops
	vtkRendering
	vtkIO)
