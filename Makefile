all:
	gcc -o mul_avx2 mul_avx2.c -mavx2 -pthread -g
