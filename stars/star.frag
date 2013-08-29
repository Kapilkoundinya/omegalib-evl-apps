#version 150 compatibility
#extension GL_ARB_gpu_shader5 : enable

flat in float sphere_radius;

void main (void)
{
    float x = gl_TexCoord[0].x;
    float y = gl_TexCoord[0].y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )	discard;

    float z = sqrt(zz);

    //vec3 normal = vec3(x, y, z);

    gl_FragColor = gl_Color;
	gl_FragColor.a = pow(zz, 16);
}
