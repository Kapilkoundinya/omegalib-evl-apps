#version 150 compatibility
#extension GL_ARB_gpu_shader5 : enable

varying vec3 var_WorldPos;
varying vec3 var_Attribs;

uniform float unif_Alpha;

uniform float unif_MaxDepth;
uniform float unif_MinDepth;

// Weights for the 4 output color components
uniform float unif_W1;
uniform float unif_W2;
uniform float unif_W3;
uniform float unif_W4;


void main(void)
{
    //gl_FrontColor = gl_Color;

	// Color field contains point attributes.
	var_Attribs = gl_Color.rgb;
	
	var_WorldPos = gl_Vertex.xyz;
    // return projection position
    gl_Position = gl_ModelViewMatrix * gl_Vertex;
	
	vec3 w = vec3(unif_W1, unif_W2, unif_W3);
	
	float colorW = (dot(w.rgb, gl_Color.rgb) - unif_MinDepth) / (unif_MaxDepth - unif_MinDepth);
	
	vec3 startColor = vec3(0.1, 0.1, 1.0);
	vec3 endColor = vec3(1.0, 0.1, 0.0);
	
	gl_FrontColor.rgb = mix(startColor, endColor, colorW);
	gl_FrontColor.rgb = mix(gl_FrontColor.rgb, gl_FrontMaterial.diffuse.rgb, unif_W4);
    gl_FrontColor.a = unif_Alpha;
}
