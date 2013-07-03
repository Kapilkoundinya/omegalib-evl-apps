#version 150 compatibility
#extension GL_ARB_gpu_shader5 : enable

void main (void)
{
    gl_FragColor = gl_Color;
}
