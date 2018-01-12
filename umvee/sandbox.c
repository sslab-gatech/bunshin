#include <elf.h>
#include <dlfcn.h>
#include <link.h>

#include <unistd.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>

/* for virtual syscalls */
#include <time.h>
#include <sys/time.h>

#include "mvee.h"
#include "logger.h"

#define LIBC_NAME             "libc.so.6"
#define LIBPTHREAD_NAME       "libpthread.so.0"

/* function prototypes */
typedef int (*main_t)
  (int, char **, char **);

typedef int (*libc_start_main_t)
  (main_t main,
   int argc,
   char **ubp_av,
   void (*init) (void),
   void (*fini) (void),
   void (*rtld_fini) (void),
   void *stack_end);

typedef int (*execve_t)
  (const char *path,
   char *const argv[],
   char *const envp[]);

typedef int (*fork_t)
  (void);

typedef int (*libc_routine_t)
  (void *);

typedef int (*clone_t)
  (libc_routine_t, void *, int, void *, ...);

typedef void *(*pthread_routine_t)
  (void *);

typedef int (*pthread_create_t)
  (pthread_t *, const pthread_attr_t *, pthread_routine_t, void *);

typedef void (*pthread_exit_t)
  (void *);

#ifdef SYNC_ORDER
typedef int (*pthread_mutex_lock_t)
  (pthread_mutex_t *);

typedef int (*pthread_spin_lock_t)
  (pthread_spinlock_t *);

typedef int (*pthread_rwlock_rdlock_t)
  (pthread_rwlock_t *);

typedef int (*pthread_rwlock_wrlock_t)
  (pthread_rwlock_t *);

typedef int (*pthread_barrier_wait_t)
  (pthread_barrier_t *);
#endif

/* structs */
struct libc_routine_wrapper{
  libc_routine_t routine;
  void *arg;
};

struct pthread_routine_wrapper{
  pthread_routine_t routine;
  void *arg;
};

/* hooked functions */
main_t                  real_main;
libc_start_main_t       real_libc_start_main;

execve_t                real_execve;
fork_t                  real_fork;
clone_t                 real_clone;

pthread_create_t        real_pthread_create;
pthread_exit_t          real_pthread_exit;

#ifdef SYNC_ORDER
pthread_mutex_lock_t    real_pthread_mutex_lock;
pthread_spin_lock_t     real_pthread_spin_lock;
pthread_rwlock_rdlock_t real_pthread_rwlock_rdlock;
pthread_rwlock_wrlock_t real_pthread_rwlock_wrlock;
pthread_barrier_wait_t  real_pthread_barrier_wait;
#endif

static void start_sync(void){ 
  syscall(SYS_MCALL, MCALL_START_SYNC);
}

static void stop_sync(void){
  syscall(SYS_MCALL, MCALL_STOP_SYNC);
}

int wrap_main(int argc, char **argv, char **environ){

	atexit(stop_sync);

  start_sync();

	return (*real_main)(argc, argv, environ);
}

int __libc_start_main(
	main_t main,
    int argc,
    char **ubp_av,
    void (*init) (void),
    void (*fini) (void),
    void (*rtld_fini) (void),
    void (* stack_end)) {

  /* store main function */
  real_main = main;

  /* resolve libc symbols */
  void *libc_handle = dlopen(LIBC_NAME, RTLD_LOCAL | RTLD_LAZY);
  if(libc_handle){
	  real_libc_start_main = dlsym(libc_handle, "__libc_start_main");
    real_execve = dlsym(libc_handle, "__execve");
    real_fork = dlsym(libc_handle, "fork");
    real_clone = dlsym(libc_handle, "__clone");

    dlclose(libc_handle);
  }

  /* resolve libpthread symbols */
  void *libpthread_handle = dlopen(LIBPTHREAD_NAME, RTLD_LOCAL | RTLD_LAZY);
  if(libpthread_handle){
    real_pthread_create = dlsym(libpthread_handle, "pthread_create");
    real_pthread_exit = dlsym(libpthread_handle, "pthread_exit");

#ifdef SYNC_ORDER
    real_pthread_mutex_lock = dlsym(libpthread_handle, "pthread_mutex_lock");
    real_pthread_spin_lock = dlsym(libpthread_handle, "pthread_spin_lock");
    real_pthread_rwlock_rdlock = dlsym(libpthread_handle, "pthread_rwlock_rdlock");
    real_pthread_rwlock_wrlock = dlsym(libpthread_handle, "pthread_rwlock_rwlock");
    real_pthread_barrier_wait = dlsym(libpthread_handle, "pthread_barrier_wait");
#endif

    dlclose(libpthread_handle);
  }

	return real_libc_start_main
    (wrap_main, argc, ubp_av, init, fini, rtld_fini, stack_end);
}

/* exec */
int __execve(const char *path, char *const argv[], char *const envp[]){
  stop_sync();
  return real_execve(path, argv, envp);
}

/* threading */
pid_t fork(void){
  syscall(SYS_MCALL, MCALL_PRE_FORK);

  pid_t rv = real_fork();

  if(rv == -1){
    return rv;
  }

  if(rv){
    rv = syscall(SYS_MCALL, MCALL_POST_FORK);
  }

  return rv;
}

void *wrap_pthread_routine(void *ctx){
  struct pthread_routine_wrapper *wrapper = ctx;

  pthread_routine_t routine = wrapper->routine;
  void *arg = wrapper->arg;

  free(wrapper);

  void *rv = routine(arg);
  stop_sync();

  return rv;
}

int pthread_create(pthread_t *newthread, const pthread_attr_t *attr, 
    pthread_routine_t routine, void *arg){

  struct pthread_routine_wrapper *wrapper = 
    malloc(sizeof(struct pthread_routine_wrapper));

  wrapper->routine = routine;
  wrapper->arg = arg;

  return real_pthread_create(newthread, attr, wrap_pthread_routine, wrapper);
}

void pthread_exit(void *retval){
  stop_sync();
  real_pthread_exit(retval);
}

int wrap_libc_routine(void *ctx){
  struct libc_routine_wrapper *wrapper = ctx;

  libc_routine_t routine = wrapper->routine;
  void *arg = wrapper->arg;

  free(wrapper);

  int rv = routine(arg);
  stop_sync();

  return rv;
}

int __clone(libc_routine_t routine, void *child_stack, int flags, void *arg, 
    ...){

  pid_t *ptid = NULL;
  struct user_desc *tls = NULL;
  pid_t *ctid = NULL;

  va_list opt;
  va_start(opt, arg);

  if(flags & CLONE_PARENT_SETTID){
    ptid = va_arg(opt, pid_t *);
  }
  if(flags & CLONE_SETTLS){
    tls = va_arg(opt, struct user_desc *);
  }
  if(flags & (CLONE_CHILD_CLEARTID | CLONE_CHILD_SETTID)){
    ctid = va_arg(opt, pid_t *);
  }

  va_end(opt);

  struct libc_routine_wrapper *wrapper = 
    malloc(sizeof(struct libc_routine_wrapper));

  wrapper->routine = routine;
  wrapper->arg = arg;

  syscall(SYS_MCALL, MCALL_PRE_FORK);

  int rv = real_clone(wrap_libc_routine, child_stack, flags, wrapper, 
      ptid, tls, ctid);

  if(rv == -1){
    return rv;
  }

  pid_t tid = syscall(SYS_MCALL, MCALL_POST_FORK);

  if(ptid){
    *ptid = tid;
  }

  return tid;
}

#ifdef SYNC_ORDER
int pthread_mutex_lock(pthread_mutex_t *mutex){
  syscall(SYS_MCALL, MCALL_SYNC_ORDER);
  return real_pthread_mutex_lock(mutex);
}
int pthread_spin_lock(pthread_spinlock_t *lock){
  syscall(SYS_MCALL, MCALL_SYNC_ORDER);
  return real_pthread_spin_lock(lock);
}
int pthread_rwlock_rdlock(pthread_rwlock_t *lock){
  syscall(SYS_MCALL, MCALL_SYNC_ORDER);
  return real_pthread_rwlock_rdlock(lock);
}
int pthread_rwlock_wrlock(pthread_rwlock_t *lock){
  syscall(SYS_MCALL, MCALL_SYNC_ORDER);
  return real_pthread_rwlock_wrlock(lock);
}

int pthread_barrier_wait(pthread_barrier_t *barrier){
  syscall(SYS_MCALL, MCALL_SYNC_ORDER);
  return real_pthread_barrier_wait(barrier);
}
#endif

/*
 * the glibc wrapper function for getpid() caches PIDs to
 * avoid calling getpid() repeatedly, which makes getpid()
 * behave as a "library function", so we do monkey patch 
 * using preload
 */
pid_t getpid(void) {
	return syscall(SYS_getpid);
}

/* 
 * forcing virtual syscall to invoke actual syscall
 */
int gettimeofday(struct timeval *tv, struct timezone *tz) {
	return syscall(SYS_gettimeofday, tv, tz);
}

int clock_gettime(clockid_t clk_id, struct timespec *tp) {
	return syscall(SYS_clock_gettime, clk_id, tp);
}

time_t time(time_t *t) {
	return syscall(SYS_time, t);
}

int getcpu(unsigned *cpu, unsigned *node, void *cache){
  return syscall(SYS_getcpu, cpu, node, NULL);
}
