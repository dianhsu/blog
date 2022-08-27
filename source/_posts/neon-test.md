---
title: 一个ARM-NEON的demo
math: false
date: 2022-08-17 13:02:20
categories:
    - C/C++
tags:
    - ISA
    - NEON
    - C/C++
index_img: https://cdn.dianhsu.com/img/2022-08-17-13-14-11.jpeg
---

之前和炮姐聊天的时候，打开了新世界的大门。手边有一台Macbook Pro M1，就用这台设备写了一个简单的demo。Apple M1 chip 支持ARMv8-a指令集，同时支持NEON拓展指令集。 测试数据基于google benchmark。

# RGB deinterleaving
```cpp
#include "benchmark/benchmark.h"
#include "arm_neon.h"

void rgb_deinterleave_c(uint8_t *r, uint8_t *g, uint8_t *b, uint8_t *rgb, int len_color) {
    /*
     * Take the elements of "rgb" and store the individual colors "r", "g", and "b".
     */
    for (int i=0; i < len_color; i++) {
        r[i] = rgb[3*i];
        g[i] = rgb[3*i+1];
        b[i] = rgb[3*i+2];
    }
}
void rgb_deinterleave_neon(uint8_t *r, uint8_t *g, uint8_t *b, uint8_t *rgb, int len_color) {
    /*
     * Take the elements of "rgb" and store the individual colors "r", "g", and "b"
     */
    int num8x16 = len_color / 16;
    uint8x16x3_t intlv_rgb;
    for (int i=0; i < num8x16; i++) {
        intlv_rgb = vld3q_u8(rgb+3*16*i);
        vst1q_u8(r+16*i, intlv_rgb.val[0]);
        vst1q_u8(g+16*i, intlv_rgb.val[1]);
        vst1q_u8(b+16*i, intlv_rgb.val[2]);
    }
}
#define LEN_COLOR 1000
uint8_t r[LEN_COLOR], g[LEN_COLOR], b[LEN_COLOR], rgb[LEN_COLOR * 3];
void testC(benchmark::State& state){
    for(auto _ : state){
        rgb_deinterleave_c(r, g, b, rgb, LEN_COLOR);
    }
}

BENCHMARK(testC);
void testNeon(benchmark::State& state){
    for(auto _ : state){
        rgb_deinterleave_neon(r, g, b, rgb, LEN_COLOR);
    }
}

BENCHMARK(testNeon);
BENCHMARK_MAIN();

/*
Run on (8 X 24.1206 MHz CPU s)
CPU Caches:
  L1 Data 64 KiB
  L1 Instruction 128 KiB
  L2 Unified 4096 KiB (x8)
Load Average: 2.51, 2.79, 2.99
-----------------------------------------------------
Benchmark           Time             CPU   Iterations
-----------------------------------------------------
testC            1928 ns         1927 ns       350642
testNeon          396 ns          395 ns      1768137
*/
```

# Accumulate Array

```cpp
#include "benchmark/benchmark.h"
#include "arm_neon.h"

float brr[4] = {0, 0, 0, 0};
float add_result_neon(float* arr, int len){
    float32x4_t tmp = vld1q_f32(brr);
    int num = len / 4;
    for(int i = 0; i < num; ++i){
        float32x4_t flv = vld1q_f32(arr + i * 4);
        tmp += flv;
    }
    float res = 0;
    vst1q_f32(brr, tmp);
    for(float i : brr){
        res += i;
    }
    return res;
}
float add_result_c(float* arr, int len){
    float res = 0;
    for(int i = 0; i < len; ++i){
        res += arr[i];
    }
    return res;
}
#define LEN 1000
float arr[LEN];
void testC(benchmark::State& state){
    for(auto _: state){
        add_result_c(arr, LEN);
    }
}
void testNeon(benchmark::State& state){
    for(auto _: state){
        add_result_neon(arr, LEN);
    }
}

BENCHMARK(testC);
BENCHMARK(testNeon);
BENCHMARK_MAIN();

/*
Run on (8 X 24.1212 MHz CPU s)
CPU Caches:
  L1 Data 64 KiB
  L1 Instruction 128 KiB
  L2 Unified 4096 KiB (x8)
Load Average: 4.72, 4.17, 3.73
-----------------------------------------------------
Benchmark           Time             CPU   Iterations
-----------------------------------------------------
testC            3428 ns         3422 ns       203604
testNeon          873 ns          872 ns       79435
*/
```