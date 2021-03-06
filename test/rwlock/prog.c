#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#define NUM_THREADS	4

#define CYCLES      10000000
#define MOD         1000000

pthread_rwlock_t lock;
unsigned long globe = 0;

void *count(void *context) {
  unsigned long value;
  long tid = (long)context;
 
  for(int i=0;i<CYCLES;i++){
    pthread_rwlock_rdlock(&lock);
    value = globe;
    pthread_rwlock_unlock(&lock);

    pthread_rwlock_wrlock(&lock);
    globe = value + 1;
    pthread_rwlock_unlock(&lock);

    if(value % MOD == 0){
      printf("thread: %ld, globe: %lu\n", tid, value);
    }
  }

  return NULL;
}

int main(int argc, char *argv[]){
  pthread_rwlock_init(&lock, NULL);
  pthread_t threads[NUM_THREADS];
  int rc;
  long t;
  
  for(t=0;t<NUM_THREADS;t++){
    rc = pthread_create(&threads[t], NULL, count, (void *)(t));
    if (rc){
      printf("ERROR; return code from pthread_create() is %d\n", rc);
      exit(-1);
    }
  }

  for(t=0;t<NUM_THREADS;t++){
    pthread_join(threads[t], NULL);
  }

  pthread_rwlock_destroy(&lock);
  pthread_exit(NULL);
}
