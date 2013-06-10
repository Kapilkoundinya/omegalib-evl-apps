#version 150 compatibility
#extension GL_ARB_gpu_shader5 : enable

varying float var_Depth;

uniform float unif_MaxDepth;
uniform float unif_MinDepth;

void main(void)
{

    gl_FrontColor = gl_Color;

    // return projection position
    gl_Position = gl_ModelViewMatrix * gl_Vertex;
	
	var_Depth = (gl_Vertex.z - unif_MinDepth) / (unif_MaxDepth - unif_MinDepth);
}
