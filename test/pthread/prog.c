#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#define NUM_THREADS	2

void *hello(void *context) {
   long tid;
   tid = (long)context;

   printf("Hello World! It's me, thread #%ld!\n", tid);
   pthread_exit(NULL);
}

int main(int argc, char *argv[]){
   pthread_t threads[NUM_THREADS];
   int rc;
   long t;

   for(t=0;t<NUM_THREADS;t++){
     rc = pthread_create(&threads[t], NULL, hello, (void *)t);
     if (rc){
       printf("ERROR; return code from pthread_create() is %d\n", rc);
       exit(-1);
     }
   }

   pthread_exit(NULL);
}
