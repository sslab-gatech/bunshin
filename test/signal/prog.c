#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

int global = 0;

static void sigint_handler(int nr){
  printf("SIGINT received\n");
  global = 0;
  printf("global: %d\n", global);

  exit(0);
}

int main(int argc, char *argv[]){

  struct sigaction sa;
  memset(&sa, 0, sizeof(struct sigaction));

  sa.sa_handler = sigint_handler;
  if(sigaction(SIGINT, &sa, NULL) < 0){
    printf("unable to register SIGINT handler\n");
    exit(-1);
  }

  unsigned long i;
  while(1){
    for(i=0; i<(1UL << 28); i++){}
    printf("gloabl: %d\n", global);
    global++;
  }

  return 0;
}
