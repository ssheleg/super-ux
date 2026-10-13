#include <stdio.h>
#include <string.h>
#include "ext_scanners.c"
int main(void) { for(int n=0;n<5;n++) { unsigned char s[80]="cell"; for(int j=0;j<n;j++)s[4+j]=92; strcpy((char*)s+4+n,"|next |\n"); printf("%d %ld\n", n, _scan_table_cell(s)); } }
