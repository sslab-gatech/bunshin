#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char* argv[]){
	printf("prepare to fork\n");

	pid_t pid = fork();
	if(pid){
		printf("P: child %d created\n", pid);
	} else {
		printf("C: hello from child %d\n", getpid());
	}
}
