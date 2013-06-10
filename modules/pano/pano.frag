///////////////////////////////////////////////////////////////////////////////////////////////////
uniform int unif_Eye;
uniform float unif_Alpha;

uniform sampler2D unif_PanoMapL;
uniform sampler2D unif_PanoMapR;

varying vec3 var_ReflectDir;
varying vec2 var_TexCoord;

uniform float unif_VertSpanDegrees;
uniform float unif_HorizSpanDegrees;
uniform float unif_VertStartDegrees;
uniform float unif_HorizStartDegrees;

///////////////////////////////////////////////////////////////////////////////////////////////////
void main (void)
{
	vec2 degrees = var_TexCoord * vec2(360, 180);
	if(degrees.x < unif_HorizStartDegrees) discard;
	if(degrees.x > unif_HorizStartDegrees + unif_HorizSpanDegrees) discard;
	if(degrees.y < unif_VertStartDegrees) discard;
	if(degrees.y > unif_VertStartDegrees + unif_VertSpanDegrees) discard;
	
	vec2 start = vec2(unif_HorizStartDegrees, unif_VertStartDegrees) / vec2(360, 180);
	vec2 span = vec2(unif_HorizSpanDegrees, unif_VertSpanDegrees) / vec2(360, 180);
	
	vec2 texCoord = start + var_TexCoord * span;
	vec4 color;
	if(unif_Eye == 0) color = texture2D(unif_PanoMapR, texCoord);
	else color = texture2D(unif_PanoMapL, texCoord);
	color.a = unif_Alpha;
	gl_FragColor = color;
}