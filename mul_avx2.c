#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <immintrin.h>

float *mat1, *mat2, *result;

float avx2vec_sum(__m256 x) {
    // hiQuad = ( x7, x6, x5, x4 )
    const __m128 hiQuad = _mm256_extractf128_ps(x, 1);
    // loQuad = ( x3, x2, x1, x0 )
    const __m128 loQuad = _mm256_castps256_ps128(x);
    // sumQuad = ( x3 + x7, x2 + x6, x1 + x5, x0 + x4 )
    const __m128 sumQuad = _mm_add_ps(loQuad, hiQuad);
    // loDual = ( -, -, x1 + x5, x0 + x4 )
    const __m128 loDual = sumQuad;
    // hiDual = ( -, -, x3 + x7, x2 + x6 )
    const __m128 hiDual = _mm_movehl_ps(sumQuad, sumQuad);
    // sumDual = ( -, -, x1 + x3 + x5 + x7, x0 + x2 + x4 + x6 )
    const __m128 sumDual = _mm_add_ps(loDual, hiDual);
    // lo = ( -, -, -, x0 + x2 + x4 + x6 )
    const __m128 lo = sumDual;
    // hi = ( -, -, -, x1 + x3 + x5 + x7 )
    const __m128 hi = _mm_shuffle_ps(sumDual, sumDual, 0x1);
    // sum = ( -, -, -, x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 )
    const __m128 sum = _mm_add_ss(lo, hi);

    return _mm_cvtss_f32(sum);
}

// mat1: row major
// mat2: col major
// store: row major
void matrix88mul(float* mat1, float* mat2, float* result) {
    for(int i = 0;i < 8;i++) {
        for(int j = 0;j < 8;j++) {
            __m256 a = _mm256_loadu_ps(mat1 + i * 8);
            __m256 b = _mm256_loadu_ps(mat2 + j * 8);
            __m256 res = _mm256_mul_ps(a, b);

            result[i * 8 + j] += avx2vec_sum(res);
        }
    }
}

void* threadfun(void* args) {
    int* ij = (int*)args;
    int i = ij[0];
    int j = ij[1];
    int dim = ij[2];

    for(int k = 0;k < dim;k++) {
        int mat1_offset = (i * dim + k) * 64;
        int mat2_offset = (j + k * dim) * 64;
        int res_offset = (i * dim + j) * 64;
        matrix88mul(mat1 + mat1_offset, mat2 + mat2_offset, result + res_offset);
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    int s1x, s1y, s2x, s2y;

    // read in first matrix, row major
    scanf("%d%d", &s1x, &s1y);
    mat1 = (float*)malloc(sizeof(float) * s1x * s1y);

    for(int i = 0, x88 = 0;i + x88 * 8 < s1x;i++) {
        if(i >= 8) {
            i = 0;
            x88++;
        }
        for(int j = 0, y88 = 0;j + y88 * 8 < s1y;j++) {
            if(j >= 8) {
                j = 0;
                y88++;
            }
            int base = (y88 + (s1y / 8) * x88) * 64;
            scanf("%f", mat1 + base + i * 8 + j);
        }
    }

    // read in second matrix, col major
    scanf("%d%d", &s2x, &s2y);
    mat2 = (float*)malloc(sizeof(float) * s2x * s2y);

    for(int i = 0, x88 = 0;i + x88 * 8 < s2x;i++) {
        if(i >= 8) {
            i = 0;
            x88++;
        }
        for(int j = 0, y88 = 0;j + y88 * 8 < s2y;j++) {
            if(j >= 8) {
                j = 0;
                y88++;
            }
            int base = (y88 + (s2y / 8) * x88) * 64;
            scanf("%f", mat2 + base + i + j * 8);
        }
    }

    result = (float*)malloc(sizeof(float) * s1x * s2y);
    pthread_t *threads = (pthread_t*)malloc(sizeof(pthread_t) * (s1y / 8) * (s2y / 8));
    int threadcnt = 0;

    for(int i = 0;i < s1x / 8;i++) {
        for(int j = 0;j < s2x / 8;j++) {
            int *arg = (int*)malloc(sizeof(int) * 3); // i, j, s1y / 8
            arg[0] = i;
            arg[1] = j;
            arg[2] = s1y / 8;
            pthread_create(&threads[threadcnt++], NULL, threadfun, (void*)arg);
        }
    }

    for(int i = 0;i < threadcnt;i++) {
        pthread_join(*(threads + i), NULL);
    }

    /*for(int i = 0;i < s1y / 8;i++) {
        for(int si = 0;si < 8;si++) {
            for(int j = 0;j < s1y / 8;j++) {
                for(int sj = 0;sj < 8;sj++) {
                    printf("%.0f ", result[(i * (s1y / 8) + j) * 64 + (si * 8 + sj)]);
                }
            }
            puts("");
        }
    }*/

    return 0;
}
