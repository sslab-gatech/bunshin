#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/times.h>

int main(int argc, char* argv[]){
  unsigned long time;
  __asm volatile ("rdtsc" : "=A"(time));
  printf("CPU time=%lu\n", time);

  return 0;
}
