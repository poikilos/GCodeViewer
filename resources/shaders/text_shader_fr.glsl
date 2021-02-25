// #version 330 core
#version 310 es
precision mediump float;

in vec4 color;
in vec2 texCoord;
out vec4 fColor;

uniform sampler2D texture_data;

void main(){
    fColor = color * texture(texture_data, texCoord);
}
