#version 150 compatibility
#extension GL_EXT_geometry_shader4: enable
#extension GL_ARB_gpu_shader5 : enable

uniform float pointScale;

uniform vec3 unif_MinBox;
uniform vec3 unif_MaxBox;

flat out vec3 vertex_light_position;
flat out vec4 eye_position;
flat out float sphere_radius;

varying in float var_Depth[];
varying out float depth;

uniform float globalAlpha;

varying in vec3 var_WorldPos[];

void
main(void)
{
	vec3 worldPos = var_WorldPos[0];
	
	if(all(greaterThan(worldPos, unif_MinBox)) && all(lessThan(worldPos, unif_MaxBox)))
	{
		sphere_radius =  pointScale * 2.0;
		float halfsize = sphere_radius * 0.5;
		
		depth = var_Depth[0];

		gl_FrontColor = gl_FrontColorIn[0];
		gl_FrontColor.a = globalAlpha;

		eye_position = gl_PositionIn[0];
		vertex_light_position = normalize(gl_LightSource[0].position.xyz - eye_position.xyz);

		gl_TexCoord[0].st = vec2(1.0,-1.0);
		gl_Position = gl_PositionIn[0];
		gl_Position.xy += vec2(halfsize, -halfsize);
		gl_Position = gl_ProjectionMatrix * gl_Position;
		EmitVertex();

		gl_TexCoord[0].st = vec2(1.0,1.0);
		gl_Position = gl_PositionIn[0];
		gl_Position.xy += vec2(halfsize, halfsize);
		gl_Position = gl_ProjectionMatrix * gl_Position;
		EmitVertex();

		gl_TexCoord[0].st = vec2(-1.0,-1.0);
		gl_Position = gl_PositionIn[0];
		gl_Position.xy += vec2(-halfsize, -halfsize);
		gl_Position = gl_ProjectionMatrix * gl_Position;
		EmitVertex();

		gl_TexCoord[0].st = vec2(-1.0,1.0);
		gl_Position = gl_PositionIn[0];
		gl_Position.xy += vec2(-halfsize, halfsize);
		gl_Position = gl_ProjectionMatrix * gl_Position;
		EmitVertex();

		EndPrimitive();
	}
}
