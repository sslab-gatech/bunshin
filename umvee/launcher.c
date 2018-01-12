#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "mvee.h"
#include "logger.h"

int terminated = 0;

static void sigext_handler(int nr){
#ifdef DEBUG
  log_dbg("system exited");
#endif

  terminated = 1;
}

static void sigdev_handler(int nr){
  log_err("deviation detected");
}

int main(int argc, char *argv[]){
  
  int i;

  /* parse args */
  int nvar = atoi(argv[1]);
  char **bins = &argv[2];
  char **args = &argv[2 + nvar];

  /* set envs */
  const char *sandbox = getenv("mvee");
  setenv("LD_PRELOAD", sandbox, 1);

  /* fork children */
  pid_t pid;
  pid_t *children = malloc(sizeof(pid_t) * nvar);
  int failure = 0;
  
  for(i=0;i<nvar;i++){
    pid = fork();

    if(pid){
      children[i] = pid;

      /* wait for variant to stop */
      while(waitpid(pid, NULL, WSTOPPED) < 0){
        if(errno == EINTR){
          continue;
        }

        failure = 1;
        log_err("did not see variant %d stop", i);
        break;
      }
    } else {
      /* wait for OK signal */
      kill(getpid(), SIGSTOP);
      
      /* execute program */
      execv(bins[i], args);
      
      /* in case exec goes into error */
      log_err("failed to launch program");
    }
  }

  /* validate variants status */
  if(failure){
   log_err("one or more variants failed to start");
   goto fini_variants;
  }

  /* register signal handler */
  struct sigaction sa;
  memset(&sa, 0, sizeof(struct sigaction));

  sa.sa_handler = sigext_handler;
  if(sigaction(SIGEXT, &sa, NULL) < 0){
    failure = 1;
    log_err("unable to register SIGEXT handler");
    goto fini_variants;
  }

  sa.sa_handler = sigdev_handler;
  if(sigaction(SIGDEV, &sa, NULL) < 0){
    failure = 1;
    log_err("unable to register SIGDEV handler");
    goto fini_variants;
  }

  /* connect to device driver */
  int dev;
  dev = open(PATH_DEVICE, O_RDWR);
  if(dev < 0){
    failure = 1;
    log_err("unable to find kernel counterpart");
    goto fini_variants;
  }

  /* create the initial variant group */
  struct arg_create_group arg_cg;
  arg_cg.monitor = getpid();
  arg_cg.nvar = nvar;
  
  int id = ioctl(dev, CMD_CREATE_GROUP, &arg_cg);
  if(id < 0){
    failure = 1;
    log_err("failed to create variant group");
    goto fini_dev;
  }

  /* register each variant on kernel */
  struct arg_register_variant arg_rv;
  for(i=0;i<nvar;i++){
    arg_rv.id = id;
    arg_rv.role = i;
    arg_rv.variant = children[i];

    if(ioctl(dev, CMD_REGISTER_VARIANT, &arg_rv) < 0){
      failure = 1;
      log_err("failed to register variant %d", i);
    }
  }

  if(failure){
    log_err("one or more variants failed to register");
    goto fini_dev;
  }

  /* continue all variants */
  for(int i=0;i<nvar;i++){
    kill(children[i], SIGCONT);
  }

  /* wait for signal */
  do{
    pause();
  } while(!terminated);

fini_dev:
  /* close device driver */
  close(dev);

fini_variants:
  /* kill all variants */
  if(failure){
    for(i=0;i<nvar;i++){
      kill(children[i], SIGKILL);
    }

    free(children);
    return -1;
  } else {
    free(children);
    return 0;
  }
}
