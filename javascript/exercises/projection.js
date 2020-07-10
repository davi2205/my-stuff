
/*

    Exercício de projeção em perspectiva.

      Autor: Davi Villalva
        Ano: 2019

*/

const m11 =  0;
const m12 =  1;
const m13 =  2;
const m14 =  3;

const m21 =  4;
const m22 =  5;
const m23 =  6;
const m24 =  7;

const m31 =  8;
const m32 =  9;
const m33 = 10;
const m34 = 11;

const m41 = 12;
const m42 = 13;
const m43 = 14;
const m44 = 15;

function mat4_new() {
    return [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ];
}

function mat4_copy(a, b) {
    a[m11] = b[m11]; a[m12] = b[m12]; a[m13] = b[m13]; a[m14] = b[m14];
    a[m21] = b[m21]; a[m22] = b[m22]; a[m23] = b[m23]; a[m24] = b[m24];
    a[m31] = b[m31]; a[m32] = b[m32]; a[m33] = b[m33]; a[m34] = b[m34];
    a[m41] = b[m41]; a[m42] = b[m42]; a[m43] = b[m43]; a[m44] = b[m44];
}

// multiplicação de matrizes 4x4
function mat4_multiply_mat4(a, b, c) {
    /*
        c = a * b
                                        | b[m11] b[m12] b[m13] b[m14] |
                                        | b[m21] b[m22] b[m23] b[m24] |
                                        | b[m31] b[m32] b[m33] b[m34] |
                                        | b[m41] b[m42] b[m43] b[m44] |
        | a[m11] a[m12] a[m13] a[m14] |   c[m11] c[m12] c[m13] c[m14]
        | a[m21] a[m22] a[m23] a[m24] |   c[m21] c[m22] c[m23] c[m24]
        | a[m31] a[m32] a[m33] a[m34] |   c[m31] c[m32] c[m33] c[m34]
        | a[m41] a[m42] a[m43] a[m44] |   c[m41] c[m42] c[m43] c[m44]
    */

    const _11 = a[m11] * b[m11] + a[m12] * b[m21] + a[m13] * b[m31] + a[m14] * b[m41]; 
    const _12 = a[m11] * b[m12] + a[m12] * b[m22] + a[m13] * b[m32] + a[m14] * b[m42];
    const _13 = a[m11] * b[m13] + a[m12] * b[m23] + a[m13] * b[m33] + a[m14] * b[m43];
    const _14 = a[m11] * b[m14] + a[m12] * b[m24] + a[m13] * b[m34] + a[m14] * b[m44];
    
    const _21 = a[m21] * b[m11] + a[m22] * b[m21] + a[m23] * b[m31] + a[m24] * b[m41]; 
    const _22 = a[m21] * b[m12] + a[m22] * b[m22] + a[m23] * b[m32] + a[m24] * b[m42];
    const _23 = a[m21] * b[m13] + a[m22] * b[m23] + a[m23] * b[m33] + a[m24] * b[m43];
    const _24 = a[m21] * b[m14] + a[m22] * b[m24] + a[m23] * b[m34] + a[m24] * b[m44];
    
    const _31 = a[m31] * b[m11] + a[m32] * b[m21] + a[m33] * b[m31] + a[m34] * b[m41]; 
    const _32 = a[m31] * b[m12] + a[m32] * b[m22] + a[m33] * b[m32] + a[m34] * b[m42];
    const _33 = a[m31] * b[m13] + a[m32] * b[m23] + a[m33] * b[m33] + a[m34] * b[m43];
    const _34 = a[m31] * b[m14] + a[m32] * b[m24] + a[m33] * b[m34] + a[m34] * b[m44];
    
    const _41 = a[m41] * b[m11] + a[m42] * b[m21] + a[m43] * b[m31] + a[m44] * b[m41]; 
    const _42 = a[m41] * b[m12] + a[m42] * b[m22] + a[m43] * b[m32] + a[m44] * b[m42];
    const _43 = a[m41] * b[m13] + a[m42] * b[m23] + a[m43] * b[m33] + a[m44] * b[m43];
    const _44 = a[m41] * b[m14] + a[m42] * b[m24] + a[m43] * b[m34] + a[m44] * b[m44];

    c[m11] = _11; c[m12] = _12; c[m13] = _13; c[m14] = _14;
    c[m21] = _21; c[m22] = _22; c[m23] = _23; c[m24] = _24;
    c[m31] = _31; c[m32] = _32; c[m33] = _33; c[m34] = _34;
    c[m41] = _41; c[m42] = _42; c[m43] = _43; c[m44] = _44;
}

function mat4_multiply_vec4(a, b, c) {
    /*
        c = a * b
                                        | b[0] |
                                        | b[1] |
                                        | b[2] |
                                        | b[3] |
        | a[m11] a[m12] a[m13] a[m14] |   c[0]
        | a[m21] a[m22] a[m23] a[m24] |   c[1]
        | a[m31] a[m32] a[m33] a[m34] |   c[2]
        | a[m41] a[m42] a[m43] a[m44] |   c[3]
    */

    let x = a[m11] * b[0] + a[m12] * b[1] + a[m13] * b[2] + a[m14] * b[3];
    let y = a[m21] * b[0] + a[m22] * b[1] + a[m23] * b[2] + a[m24] * b[3];
    let z = a[m31] * b[0] + a[m32] * b[1] + a[m33] * b[2] + a[m34] * b[3];
    let w = a[m41] * b[0] + a[m42] * b[1] + a[m43] * b[2] + a[m44] * b[3];

    c[0] = x;
    c[1] = y;
    c[2] = z;
    c[3] = w;
}

function mat4_set_identity(a) {
    a[m11] = 1.0; a[m12] = 0.0; a[m13] = 0.0; a[m14] = 0.0;
    a[m21] = 0.0; a[m22] = 1.0; a[m23] = 0.0; a[m24] = 0.0;
    a[m31] = 0.0; a[m32] = 0.0; a[m33] = 1.0; a[m34] = 0.0;
    a[m41] = 0.0; a[m42] = 0.0; a[m43] = 0.0; a[m44] = 1.0;
}

function mat4_set_translation(a, x, y, z) {
    a[m11] = 1.0; a[m12] = 0.0; a[m13] = 0.0; a[m14] = x;
    a[m21] = 0.0; a[m22] = 1.0; a[m23] = 0.0; a[m24] = y;
    a[m31] = 0.0; a[m32] = 0.0; a[m33] = 1.0; a[m34] = z;
    a[m41] = 0.0; a[m42] = 0.0; a[m43] = 0.0; a[m44] = 1.0;
}

function mat4_set_rotation(a, angle, x, y, z) {
    const rad = angle * 0.0174533;
    const cos = Math.cos(rad);
    const sin = Math.sin(rad);
    const ocos = 1.0 - cos;

    a[m11] = cos + x * x * ocos;
    a[m12] = x * y * ocos - z * sin;
    a[m13] = x * z * ocos + y * sin;
    a[m14] = 0.0;

    a[m21] = y * x * ocos + z * sin;
    a[m22] = cos + y * y * ocos;
    a[m23] = y * z * ocos - x * sin;
    a[m24] = 0.0;

    a[m31] = z * x * ocos - y * sin;
    a[m32] = z * y * ocos + x * sin;
    a[m33] = cos + z * z * ocos;
    a[m34] = 0.0;

    a[m41] = 0.0;
    a[m42] = 0.0;
    a[m43] = 0.0;
    a[m44] = 1.0;
}

function mat4_set_perspective(a, fov, aspect, near, far) {
    const rad = fov * 0.0174533; // fov em radiano
    const tan = Math.tan(rad / 2.0); // cotangente de fov * 2
    const denom = near - far;

    a[m11] = 1.0 / (aspect * tan);
    a[m12] = 0.0;
    a[m13] = 0.0;
    a[m14] = 0.0;

    a[m21] = 0.0;
    a[m22] = 1.0 / tan;
    a[m23] = 0.0;
    a[m24] = 0.0;

    a[m31] = 0.0;
    a[m32] = 0.0;
    a[m33] = (near + far) / denom;
    a[m34] = (2.0 * near * far) / denom;

    a[m41] = 0.0;
    a[m42] = 0.0;
    a[m43] = -1.0;
    a[m44] = 0.0;
}

const vertex_buffer = [
    -1.0, -1.0, -1.0,
    1.0, -1.0, -1.0,
    1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,

    -1.0, -1.0,  1.0,
    1.0, -1.0,  1.0,
    1.0,  1.0,  1.0,
    -1.0,  1.0,  1.0,
];

const index_buffer = [
    0, 1,
    1, 2,
    2, 3,
    3, 0,

    4, 5,
    5, 6,
    6, 7,
    7, 4,

    0, 4,
    1, 5,
    2, 6,
    3, 7,
];

/** @type {HTMLCanvasElement} */
const canvas = document.getElementById("screen");
const ctx = canvas.getContext("2d");

const projection = mat4_new();
const modelview = mat4_new();
const combined = mat4_new();

const tmp = mat4_new();
const tmp_vec0 = [0.0, 0.0, 0.0, 0.0];
const tmp_vec1 = [0.0, 0.0, 0.0, 0.0];

mat4_set_perspective(projection, 45.0, canvas.width / canvas.height, 0.01, 100.0);

function render_line(x0, y0, x1, y1) {
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.closePath();
    ctx.stroke();
}

let delta = 0.0;

function render() {
    delta += 0.7;

    window.requestAnimationFrame(render);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // modelview = identity
    mat4_set_identity(modelview);

    // modelview = translation * rotation_y * rotation_z
    // glTranslatef
    mat4_set_translation(tmp, 0, 0, -6.0);
    mat4_multiply_mat4(modelview, tmp, modelview);

    // glRotatef (no eixo y)
    mat4_set_rotation(tmp, delta, 0.0, 1.0, 0.0);
    mat4_multiply_mat4(modelview, tmp, modelview);

    // glRotatef (no eixo z)
    mat4_set_rotation(tmp, delta / 2.0, 0.0, 0.0, 1.0);
    mat4_multiply_mat4(modelview, tmp, modelview);

    // combined = projection * modelview
    mat4_copy(combined, projection);
    mat4_multiply_mat4(combined, modelview, combined);

    const cnt = index_buffer.length / 2;

    for (let i = 0; i < cnt; ++i) {
        const idx = index_buffer[i * 2] * 3;
        const next_idx = index_buffer[i * 2 + 1] * 3;

        // armazenando as coordenadas temporariamente em dois vetores de ordem 4
        tmp_vec0[0] = vertex_buffer[idx];
        tmp_vec0[1] = vertex_buffer[idx + 1];
        tmp_vec0[2] = vertex_buffer[idx + 2];
        tmp_vec0[3] = 1.0; // deve ser 1.0, usaremos para fazer a divisão de perspectiva depois

        tmp_vec1[0] = vertex_buffer[next_idx];
        tmp_vec1[1] = vertex_buffer[next_idx + 1];
        tmp_vec1[2] = vertex_buffer[next_idx + 2];
        tmp_vec1[3] = 1.0; // deve ser 1.0, usaremos para fazer a divisão de perspectiva depois

        // fazemos a projeção do ponto 3d em 2d através da transformação (multiplicação) da matriz 
        // combinada pelo vetor de ordem 4 (que também pode ser interpretado como uma matriz 4x1)
        // vetor_final = combined * vetor
        mat4_multiply_vec4(combined, tmp_vec0, tmp_vec0);
        mat4_multiply_vec4(combined, tmp_vec1, tmp_vec1);

        // divisão de perspectiva, essa divisão é que dá a ilusão de profundidade
        // no espaço (se a matriz de projeção for alguma perspectiva).
        // vetor_final /= vetor_final.w
        tmp_vec0[0] /= tmp_vec0[3];
        tmp_vec0[1] /= tmp_vec0[3];
        tmp_vec0[2] /= tmp_vec0[3];

        tmp_vec1[0] /= tmp_vec1[3];
        tmp_vec1[1] /= tmp_vec1[3];
        tmp_vec1[2] /= tmp_vec1[3];


        /*
            feita a projeção e a divisão de perspectiva o sistema de coordenadas 2D
            onde os estarão será:

                        1.0
                        |
                        |
            -1.0 <------------> 1.0
                        |
                        |
                        -1.0

            Precisamos ajustar isso para as coordenadas da tela onde desenharemos
            as linhas.
        */

        tmp_vec0[0] = (tmp_vec0[0] * 0.5 + 0.5) * canvas.width; 
        tmp_vec0[1] = (tmp_vec0[1] * 0.5 + 0.5) * canvas.height;
        tmp_vec1[0] = (tmp_vec1[0] * 0.5 + 0.5) * canvas.width; 
        tmp_vec1[1] = (tmp_vec1[1] * 0.5 + 0.5) * canvas.height;

        render_line(tmp_vec0[0], tmp_vec0[1], tmp_vec1[0], tmp_vec1[1]);
    }
}

render();
