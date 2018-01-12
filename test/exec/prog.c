#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char* argv[]){
	execl("/bin/ls", "/bin/ls", NULL);
  return 0;
}
