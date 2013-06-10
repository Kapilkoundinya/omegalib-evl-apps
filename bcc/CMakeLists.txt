add_executable(bcc BCC.cpp)
set_target_properties(bcc PROPERTIES FOLDER apps)
target_link_libraries(bcc
	omega 
	omegaToolkit
    omegaOsg)
