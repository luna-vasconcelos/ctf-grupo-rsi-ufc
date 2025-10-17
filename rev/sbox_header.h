#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
void initialize_sbox (unsigned char* sbox){
	size_t sbox_size = 64;
	for (int i=0; i<sbox_size;i++){
			sbox[i] = i;
	}
}
void generate_sbox (uint8_t* sbox, const char* flag){
	size_t flag_size = 64;
	int arr = 0;
	initialize_sbox(sbox);
	// Shuffle
	for (int i = 0; i < flag_size;i++){
		arr = (arr + sbox[i] + flag[i%flag_size])%64;
		uint8_t aux = sbox[i];
		sbox[i] = sbox[arr];
		sbox[arr] = aux; 
	}
	
}
void print_sbox (const uint8_t* sbox){
	printf("Sbox size: %i\n",strlen(sbox));
	printf("Sbox = {");
	for (int i = 0;i < 64;i++){
		if (i%8 == 0)
			printf("\n");
		printf("0x%02X,",sbox[i]);
	}
	printf("\n};");
}

