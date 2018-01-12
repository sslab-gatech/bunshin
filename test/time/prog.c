#include <sys/time.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]){
  char buffer[30];
  time_t curtime;

  curtime = time (NULL);

  strftime(buffer,30,"%m-%d-%Y  %T.",localtime(&curtime));
  printf("Current time: %s\n",buffer);

  return 0;
}
