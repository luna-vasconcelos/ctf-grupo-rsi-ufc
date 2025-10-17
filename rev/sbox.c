#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "sbox_header.h"
// 6-bit input (64 entries)
uint8_t s_box [64] = {};
int main (int narg,char** argv[]){
	generate_sbox(s_box,"RSI{3sp3c14l15t4_3m_cr1pt0gr4f14_sb0x_zwqeqalHffy4WEn6ekl7xRPQd}"); 
	print_sbox(s_box);
	return 0;
}
