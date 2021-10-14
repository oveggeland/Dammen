#include <stdio.h>

int main(){
	printf("Hello world\n");

	// Open file and find size
	FILE* f = fopen("p_r_0010.rd7", "r");
	fseek(f, 0, SEEK_END);
	int size = ftell(f);
	printf("Size of file is %d\n", size);
	fseek(f, 0, SEEK_SET);
	
	// Define data to read
	long my_trace_num = 0;
	int my_buffer[4];
	int n_samples = 1;



	readtrace_rd7(f, my_trace_num, my_buffer, n_samples);
	printf("\nFERDIG");

	size = ftell(f);
	printf("\nPointer is at %d\n", size);

	printf("\n%d\n%d\n%d\n%d", my_buffer[0], my_buffer[1], my_buffer[2], my_buffer[3]);

	return 0;
}

void readtrace_rd7( FILE  *fp, long tracenumber, int *buffer, int samples) {
	long pos;
	int nbytes;
	pos = samples;
	pos *= sizeof(int);
	pos *= tracenumber;   // position of targeted trace calculated


	if (fseek(fp,pos,SEEK_SET)!= 0) {
		printf("\nError 1");
		//error(ERR1);      // check if it works abort otherwise!
	}
	nbytes = samples * sizeof(int);


	if ( fread((char *)buffer,1,nbytes,fp) !=nbytes) {  // read the trace into the buffer
		printf("Error 2");
	}
}