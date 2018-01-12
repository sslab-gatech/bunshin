/* 
 * systable.c
 * 
 *  Created on: Mar 8, 2016
 *  	Author: Meng
 */

#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/compiler.h>
#include <linux/kallsyms.h>
#include <linux/preempt.h>

#include "logger.h"
#include "mcall.h"
#include "systable.h"

/* +++ begin of {{group_include}} +++ */
#include "stub_sys.h"
#include "stub_fs.h"
#include "stub_io.h"
#include "stub_sock.h"
#include "stub_mem.h"
#include "stub_ps.h"

/* +++ end of block +++ */

/* macro helpers */
#define HOOK_SYS(name)                              \
  hook_syscall(__NR_##name, (void **)&ref_SYS_##name, new_SYS_##name)

#define UNHOOK_SYS(name)                            \
  unhook_syscall(__NR_##name, ref_SYS_##name)

unsigned long **syscall_table; 

/* for mcall */
asmlinkage long (*ref_SYS_mcall)
  (unsigned int cmd, unsigned long arg);

#ifdef __NR_exit
asmlinkage long (*ref_SYS_exit)
  (int status);
#endif

#ifdef __NR_exit_group
asmlinkage long (*ref_SYS_exit_group)
  (int status);
#endif

/* +++ begin of {{syscall_variables}} +++ */

/* group sys */
#ifdef __NR_times
asmlinkage long (*ref_SYS_times) 
  (struct tms __user *tbuf);
#endif
#ifdef __NR_sysinfo
asmlinkage long (*ref_SYS_sysinfo) 
  (struct sysinfo __user *info);
#endif
#ifdef __NR_newuname
asmlinkage long (*ref_SYS_newuname) 
  (struct new_utsname __user *name);
#endif
#ifdef __NR_umask
asmlinkage long (*ref_SYS_umask) 
  (mode_t mask);
#endif
#ifdef __NR_sethostname
asmlinkage long (*ref_SYS_sethostname) 
  (char __user *name, 
  int len);
#endif
#ifdef __NR_setdomainname
asmlinkage long (*ref_SYS_setdomainname) 
  (char __user *name, 
  int len);
#endif
#ifdef __NR_getrlimit
asmlinkage long (*ref_SYS_getrlimit) 
  (unsigned int resource, 
  struct rlimit __user *rlim);
#endif
#ifdef __NR_setrlimit
asmlinkage long (*ref_SYS_setrlimit) 
  (unsigned int resource, 
  struct rlimit __user *rlim);
#endif
#ifdef __NR_getrusage
asmlinkage long (*ref_SYS_getrusage) 
  (int who, 
  struct rusage __user *ru);
#endif
#ifdef __NR_getpriority
asmlinkage long (*ref_SYS_getpriority) 
  (int which, 
  int who);
#endif
#ifdef __NR_setpriority
asmlinkage long (*ref_SYS_setpriority) 
  (int which, 
  int who, 
  int niceval);
#endif
#ifdef __NR_getpid
asmlinkage long (*ref_SYS_getpid) 
  (void);
#endif
#ifdef __NR_gettid
asmlinkage long (*ref_SYS_gettid) 
  (void);
#endif
#ifdef __NR_getppid
asmlinkage long (*ref_SYS_getppid) 
  (void);
#endif
#ifdef __NR_getpgrp
asmlinkage long (*ref_SYS_getpgrp) 
  (void);
#endif
#ifdef __NR_setpgid
asmlinkage long (*ref_SYS_setpgid) 
  (pid_t pid, 
  pid_t pgid);
#endif
#ifdef __NR_getsid
asmlinkage long (*ref_SYS_getsid) 
  (pid_t pid);
#endif
#ifdef __NR_setsid
asmlinkage long (*ref_SYS_setsid) 
  (void);
#endif
#ifdef __NR_getuid
asmlinkage long (*ref_SYS_getuid) 
  (void);
#endif
#ifdef __NR_setuid
asmlinkage long (*ref_SYS_setuid) 
  (uid_t uid);
#endif
#ifdef __NR_geteuid
asmlinkage long (*ref_SYS_geteuid) 
  (void);
#endif
#ifdef __NR_setreuid
asmlinkage long (*ref_SYS_setreuid) 
  (uid_t ruid, 
  uid_t euid);
#endif
#ifdef __NR_getresuid
asmlinkage long (*ref_SYS_getresuid) 
  (uid_t __user *ruidp, 
  uid_t __user *euidp, 
  uid_t __user *suidp);
#endif
#ifdef __NR_setresuid
asmlinkage long (*ref_SYS_setresuid) 
  (uid_t ruid, 
  uid_t euid, 
  uid_t suid);
#endif
#ifdef __NR_setfsuid
asmlinkage long (*ref_SYS_setfsuid) 
  (uid_t uid);
#endif
#ifdef __NR_getgid
asmlinkage long (*ref_SYS_getgid) 
  (void);
#endif
#ifdef __NR_setgid
asmlinkage long (*ref_SYS_setgid) 
  (gid_t gid);
#endif
#ifdef __NR_getegid
asmlinkage long (*ref_SYS_getegid) 
  (void);
#endif
#ifdef __NR_setregid
asmlinkage long (*ref_SYS_setregid) 
  (gid_t rgid, 
  gid_t egid);
#endif
#ifdef __NR_getresgid
asmlinkage long (*ref_SYS_getresgid) 
  (gid_t __user *rgidp, 
  gid_t __user *egidp, 
  gid_t __user *gidp);
#endif
#ifdef __NR_setresgid
asmlinkage long (*ref_SYS_setresgid) 
  (gid_t rgid, 
  gid_t ugid, 
  gid_t sgid);
#endif
#ifdef __NR_setfsgid
asmlinkage long (*ref_SYS_setfsgid) 
  (gid_t gid);
#endif
#ifdef __NR_getgroups
asmlinkage long (*ref_SYS_getgroups) 
  (int gidsetsize, 
  gid_t __user *grouplist);
#endif
#ifdef __NR_setgroups
asmlinkage long (*ref_SYS_setgroups) 
  (int gidsetsize, 
  gid_t __user *grouplist);
#endif
#ifdef __NR_getcwd
asmlinkage long (*ref_SYS_getcwd) 
  (char __user *buf, 
  unsigned long size);
#endif
#ifdef __NR_gettimeofday
asmlinkage long (*ref_SYS_gettimeofday) 
  (struct timeval __user *tv, 
  struct timezone __user *tz);
#endif
#ifdef __NR_time
asmlinkage long (*ref_SYS_time) 
  (time_t __user *t);
#endif
#ifdef __NR_clock_gettime
asmlinkage long (*ref_SYS_clock_gettime) 
  (clockid_t which_clock, 
  struct timespec __user *tp);
#endif
#ifdef __NR_clock_getres
asmlinkage long (*ref_SYS_clock_getres) 
  (clockid_t which_clock, 
  struct timespec __user *tp);
#endif
#ifdef __NR_getcpu
asmlinkage long (*ref_SYS_getcpu) 
  (unsigned int __user *cpu, 
  unsigned int __user *node, 
  void __user *cache);
#endif

/* group fs */
#ifdef __NR_access
asmlinkage long (*ref_SYS_access) 
  (const char __user *filename, 
  int mode);
#endif
#ifdef __NR_faccessat
asmlinkage long (*ref_SYS_faccessat) 
  (int dfd, 
  const char __user *filename, 
  int mode);
#endif
#ifdef __NR_readlink
asmlinkage long (*ref_SYS_readlink) 
  (const char __user *path, 
  char __user *buf, 
  int bufsiz);
#endif
#ifdef __NR_readlinkat
asmlinkage long (*ref_SYS_readlinkat) 
  (int dfd, 
  const char __user *path, 
  char __user *buf, 
  int bufsiz);
#endif
#ifdef __NR_stat
asmlinkage long (*ref_SYS_stat) 
  (const char __user *filename, 
  struct stat __user *statbuf);
#endif
#ifdef __NR_fstat
asmlinkage long (*ref_SYS_fstat) 
  (unsigned int fd, 
  struct stat __user *statbuf);
#endif
#ifdef __NR_lstat
asmlinkage long (*ref_SYS_lstat) 
  (const char __user *filename, 
  struct stat __user *statbuf);
#endif
#ifdef __NR_newfstatat
asmlinkage long (*ref_SYS_newfstatat) 
  (int dfd, 
  const char __user *filename, 
  struct stat __user *statbuf, 
  int flag);
#endif
#ifdef __NR_truncate
asmlinkage long (*ref_SYS_truncate) 
  (const  char __user *path, 
  long length);
#endif
#ifdef __NR_ftruncate
asmlinkage long (*ref_SYS_ftruncate) 
  (unsigned int fd, 
  unsigned long length);
#endif
#ifdef __NR_link
asmlinkage long (*ref_SYS_link) 
  (const char __user *oldname, 
  const char __user *newname);
#endif
#ifdef __NR_linkat
asmlinkage long (*ref_SYS_linkat) 
  (int olddfd, 
  const char __user *oldname, 
  int newdfd, 
  const char __user *newname, 
  int flags);
#endif
#ifdef __NR_symlink
asmlinkage long (*ref_SYS_symlink) 
  (const char __user *oldname, 
  const char __user *newname);
#endif
#ifdef __NR_symlinkat
asmlinkage long (*ref_SYS_symlinkat) 
  (const char __user *oldname, 
  int newdfd, 
  const char __user *newname);
#endif
#ifdef __NR_unlink
asmlinkage long (*ref_SYS_unlink) 
  (const char __user *pathname);
#endif
#ifdef __NR_unlinkat
asmlinkage long (*ref_SYS_unlinkat) 
  (int dfd, 
  const char __user *pathname, 
  int flags);
#endif
#ifdef __NR_rename
asmlinkage long (*ref_SYS_rename) 
  (const char __user *oldname, 
  const char __user *newname);
#endif
#ifdef __NR_renameat
asmlinkage long (*ref_SYS_renameat) 
  (int olddfd, 
  const char __user *oldname, 
  int newdfd, 
  const char __user *newname);
#endif
#ifdef __NR_mkdir
asmlinkage long (*ref_SYS_mkdir) 
  (const char __user *pathname, 
  umode_t mode);
#endif
#ifdef __NR_mkdirat
asmlinkage long (*ref_SYS_mkdirat) 
  (int dfd, 
  const char __user *pathname, 
  umode_t mode);
#endif
#ifdef __NR_rmdir
asmlinkage long (*ref_SYS_rmdir) 
  (const char __user *pathname);
#endif
#ifdef __NR_chdir
asmlinkage long (*ref_SYS_chdir) 
  (const char __user *filename);
#endif
#ifdef __NR_fchdir
asmlinkage long (*ref_SYS_fchdir) 
  (int fd);
#endif
#ifdef __NR_mknod
asmlinkage long (*ref_SYS_mknod) 
  (const char __user *pathname, 
  umode_t mode, 
  unsigned int dev);
#endif
#ifdef __NR_mknodat
asmlinkage long (*ref_SYS_mknodat) 
  (int dfd, 
  const char __user *pathname, 
  umode_t mode, 
  unsigned int dev);
#endif
#ifdef __NR_chmod
asmlinkage long (*ref_SYS_chmod) 
  (const char __user *filename, 
  umode_t mode);
#endif
#ifdef __NR_fchmod
asmlinkage long (*ref_SYS_fchmod) 
  (unsigned int fd, 
  umode_t mode);
#endif
#ifdef __NR_chown
asmlinkage long (*ref_SYS_chown) 
  (const char __user *filename, 
  uid_t user, 
  gid_t group);
#endif
#ifdef __NR_fchown
asmlinkage long (*ref_SYS_fchown) 
  (unsigned int fd, 
  uid_t user, 
  gid_t group);
#endif
#ifdef __NR_lchown
asmlinkage long (*ref_SYS_lchown) 
  (const char __user *filename, 
  uid_t user, 
  gid_t group);
#endif
#ifdef __NR_fchownat
asmlinkage long (*ref_SYS_fchownat) 
  (int dfd, 
  const char __user *filename, 
  uid_t user, 
  gid_t group, 
  int flag);
#endif
#ifdef __NR_setxattr
asmlinkage long (*ref_SYS_setxattr) 
  (const char __user *pathname, 
  const char __user *name, 
  const void __user *value, 
  size_t size, 
  int flags);
#endif
#ifdef __NR_fsetxattr
asmlinkage long (*ref_SYS_fsetxattr) 
  (int fd, 
  const char __user *name, 
  const void __user *value, 
  size_t size, 
  int flags);
#endif
#ifdef __NR_lsetxattr
asmlinkage long (*ref_SYS_lsetxattr) 
  (const char __user *pathname, 
  const char __user *name, 
  const void __user *value, 
  size_t size, 
  int flags);
#endif
#ifdef __NR_getxattr
asmlinkage long (*ref_SYS_getxattr) 
  (const char __user *pathname, 
  const char __user *name, 
  void __user *value, 
  size_t size);
#endif
#ifdef __NR_fgetxattr
asmlinkage long (*ref_SYS_fgetxattr) 
  (int fd, 
  const char __user *name, 
  void __user *value, 
  size_t size);
#endif
#ifdef __NR_lgetxattr
asmlinkage long (*ref_SYS_lgetxattr) 
  (const char __user *pathname, 
  const char __user *name, 
  void __user *value, 
  size_t size);
#endif
#ifdef __NR_removexattr
asmlinkage long (*ref_SYS_removexattr) 
  (const char __user *pathname, 
  const char __user *name);
#endif
#ifdef __NR_fremovexattr
asmlinkage long (*ref_SYS_fremovexattr) 
  (int fd, 
  const char __user *name);
#endif
#ifdef __NR_lremovexattr
asmlinkage long (*ref_SYS_lremovexattr) 
  (const char __user *pathname, 
  const char __user *name);
#endif
#ifdef __NR_statfs
asmlinkage long (*ref_SYS_statfs) 
  (const char __user *pathname, 
  struct statfs __user *buf);
#endif
#ifdef __NR_fstatfs
asmlinkage long (*ref_SYS_fstatfs) 
  (int fd, 
  struct statfs __user *buf);
#endif
#ifdef __NR_getdents
asmlinkage long (*ref_SYS_getdents) 
  (unsigned int fd, 
  void *dirp, 
  unsigned int count);
#endif

/* group io */
#ifdef __NR_open
asmlinkage long (*ref_SYS_open) 
  (const char __user *filename, 
  int flags, 
  umode_t mode);
#endif
#ifdef __NR_openat
asmlinkage long (*ref_SYS_openat) 
  (int dfd, 
  const char __user *filename, 
  int flags, 
  umode_t mode);
#endif
#ifdef __NR_creat
asmlinkage long (*ref_SYS_creat) 
  (const char __user *pathname, 
  umode_t mode);
#endif
#ifdef __NR_close
asmlinkage long (*ref_SYS_close) 
  (unsigned int fd);
#endif
#ifdef __NR_lseek
asmlinkage long (*ref_SYS_lseek) 
  (unsigned int fd, 
  off_t offset, 
  unsigned int whence);
#endif
#ifdef __NR_read
asmlinkage long (*ref_SYS_read) 
  (unsigned int fd, 
  char __user *buf, 
  size_t count);
#endif
#ifdef __NR_write
asmlinkage long (*ref_SYS_write) 
  (unsigned int fd, 
  const char __user *buf, 
  size_t count);
#endif
#ifdef __NR_pread64
asmlinkage long (*ref_SYS_pread64) 
  (unsigned int fd, 
  char __user *buf, 
  size_t count, 
  loff_t pos);
#endif
#ifdef __NR_pwrite64
asmlinkage long (*ref_SYS_pwrite64) 
  (unsigned int fd, 
  const char __user *buf, 
  size_t count, 
  loff_t pos);
#endif
#ifdef __NR_readv
asmlinkage long (*ref_SYS_readv) 
  (unsigned int fd, 
  struct iovec __user *vec, 
  unsigned long vlen);
#endif
#ifdef __NR_writev
asmlinkage long (*ref_SYS_writev) 
  (unsigned int fd, 
  struct iovec __user *vec, 
  unsigned long vlen);
#endif
#ifdef __NR_pipe
asmlinkage long (*ref_SYS_pipe) 
  (int __user *fildes);
#endif
#ifdef __NR_pipe2
asmlinkage long (*ref_SYS_pipe2) 
  (int __user *fildes, 
  int flags);
#endif
#ifdef __NR_eventfd
asmlinkage long (*ref_SYS_eventfd) 
  (unsigned int count);
#endif
#ifdef __NR_eventfd2
asmlinkage long (*ref_SYS_eventfd2) 
  (unsigned int count, 
  int flags);
#endif
#ifdef __NR_epoll_create
asmlinkage long (*ref_SYS_epoll_create) 
  (int size);
#endif
#ifdef __NR_epoll_create1
asmlinkage long (*ref_SYS_epoll_create1) 
  (int flags);
#endif
#ifdef __NR_epoll_ctl
asmlinkage long (*ref_SYS_epoll_ctl) 
  (int epfd, 
  int op, 
  int fd, 
  struct epoll_event __user *event);
#endif
#ifdef __NR_sendfile
asmlinkage long (*ref_SYS_sendfile) 
  (int out_fd, 
  int in_fd, 
  off_t __user *offset, 
  size_t count);
#endif
#ifdef __NR_sendfile64
asmlinkage long (*ref_SYS_sendfile64) 
  (int out_fd, 
  int in_fd, 
  loff_t __user *offset, 
  size_t count);
#endif
#ifdef __NR_dup
asmlinkage long (*ref_SYS_dup) 
  (unsigned int fildes);
#endif
#ifdef __NR_dup2
asmlinkage long (*ref_SYS_dup2) 
  (unsigned int oldfd, 
  unsigned int newfd);
#endif
#ifdef __NR_dup3
asmlinkage long (*ref_SYS_dup3) 
  (unsigned int oldfd, 
  unsigned int newfd, 
  int flags);
#endif
#ifdef __NR_poll
asmlinkage long (*ref_SYS_poll) 
  (struct pollfd __user *fds, 
  unsigned int nfds, 
  int timeout);
#endif
#ifdef __NR_ppoll
asmlinkage long (*ref_SYS_ppoll) 
  (struct pollfd __user *fds, 
  unsigned int nfds, 
  struct timespec __user *timeout, 
  void __user *sigmask, 
  size_t sigsetsize);
#endif
#ifdef __NR_select
asmlinkage long (*ref_SYS_select) 
  (int nfds, 
  fd_set __user *readfds, 
  fd_set __user *writefds, 
  fd_set __user *exceptfds, 
  struct timeval __user *timeout);
#endif
#ifdef __NR_pselect6
asmlinkage long (*ref_SYS_pselect6) 
  (int nfds, 
  fd_set __user *readfds, 
  fd_set __user *writefds, 
  fd_set __user *exceptfds, 
  struct timespec __user *timeout, 
  sigset_t __user *sigmask);
#endif
#ifdef __NR_fcntl
asmlinkage long (*ref_SYS_fcntl) 
  (unsigned int fd, 
  unsigned int cmd, 
  void *arg);
#endif
#ifdef __NR_ioctl
asmlinkage long (*ref_SYS_ioctl) 
  (unsigned int fd, 
  unsigned int cmd, 
  void *arg);
#endif

/* group sock */
#ifdef __NR_socket
asmlinkage long (*ref_SYS_socket) 
  (int domain, 
  int type, 
  int protocol);
#endif
#ifdef __NR_socketpair
asmlinkage long (*ref_SYS_socketpair) 
  (int domain, 
  int type, 
  int protocol, 
  int __user *sv);
#endif
#ifdef __NR_shutdown
asmlinkage long (*ref_SYS_shutdown) 
  (int sockfd, 
  int how);
#endif
#ifdef __NR_connect
asmlinkage long (*ref_SYS_connect) 
  (int fd, 
  struct sockaddr __user *addr, 
  int addrlen);
#endif
#ifdef __NR_bind
asmlinkage long (*ref_SYS_bind) 
  (int fd, 
  struct sockaddr __user *addr, 
  int addrlen);
#endif
#ifdef __NR_accept
asmlinkage long (*ref_SYS_accept) 
  (int fd, 
  void __user *addr, 
  int __user *addrlen);
#endif
#ifdef __NR_accept4
asmlinkage long (*ref_SYS_accept4) 
  (int fd, 
  void __user *addr, 
  int __user *addrlen, 
  int flags);
#endif
#ifdef __NR_listen
asmlinkage long (*ref_SYS_listen) 
  (int sockfd, 
  int backlog);
#endif
#ifdef __NR_getsockopt
asmlinkage long (*ref_SYS_getsockopt) 
  (int sockfd, 
  int level, 
  int optname, 
  char __user *optval, 
  int __user *optlen);
#endif
#ifdef __NR_setsockopt
asmlinkage long (*ref_SYS_setsockopt) 
  (int sockfd, 
  int level, 
  int optname, 
  char __user *optval, 
  int optlen);
#endif
#ifdef __NR_getsockname
asmlinkage long (*ref_SYS_getsockname) 
  (int sockfd, 
  void __user *addr, 
  int __user *addrlen);
#endif
#ifdef __NR_recvfrom
asmlinkage long (*ref_SYS_recvfrom) 
  (int sockfd, 
  void __user *buf, 
  size_t size, 
  unsigned int flags, 
  void __user *addr, 
  int __user *addrlen);
#endif
#ifdef __NR_sendto
asmlinkage long (*ref_SYS_sendto) 
  (int sockfd, 
  void __user *buf, 
  size_t len, 
  unsigned int flags, 
  struct sockaddr __user *addr, 
  int addrlen);
#endif
#ifdef __NR_recvmsg
asmlinkage long (*ref_SYS_recvmsg) 
  (int sockfd, 
  MSGHDR_TYPE __user *msg, 
  unsigned int flags);
#endif
#ifdef __NR_sendmsg
asmlinkage long (*ref_SYS_sendmsg) 
  (int sockfd, 
  MSGHDR_TYPE __user *msg, 
  unsigned int flags);
#endif

/* group mem */
#ifdef __NR_mmap
asmlinkage long (*ref_SYS_mmap) 
  (void *addr, 
  size_t length, 
  int prot, 
  int flags, 
  int fd, 
  loff_t offset);
#endif

/* group ps */
#ifdef __NR_wait4
asmlinkage long (*ref_SYS_wait4) 
  (pid_t upid, 
  int __user *stat, 
  int options, 
  struct rusage __user *ru);
#endif
#ifdef __NR_kill
asmlinkage long (*ref_SYS_kill) 
  (pid_t pid, 
  int sig);
#endif
#ifdef __NR_tgkill
asmlinkage long (*ref_SYS_tgkill) 
  (pid_t tgid, 
  pid_t pid, 
  int sig);
#endif

/* +++ end of block +++ */

/* page protection */
static void disable_page_protection(void){
  unsigned long value;

  preempt_disable();
  barrier();

  asm volatile("mov %%cr0, %0" : "=r" (value));

  if(!(value & 0x00010000))
    return;

  asm volatile("mov %0, %%cr0" : : "r" (value & ~0x00010000));
}
                                                                                
static void enable_page_protection(void){
  unsigned long value;

  asm volatile("mov %%cr0, %0" : "=r" (value));

  if((value & 0x00010000))
    return;

  asm volatile("mov %0, %%cr0" : : "r" (value | 0x00010000));

  barrier();
  preempt_enable();
}

static void hook_syscall(int nr, void **ref_sys, void *new_sys){
  *ref_sys = syscall_table[nr];
  syscall_table[nr] = new_sys;
}

static void unhook_syscall(int nr, void *ref_sys){
  syscall_table[nr] = ref_sys;
}

int hook_syscall_table(void){
	/* acquire syscall table first */
	syscall_table = (unsigned long **)kallsyms_lookup_name("sys_call_table");

  if(!syscall_table){
    log_err("unable to find syscall table");
    return -1;
  }

  /* enable overriding */
  disable_page_protection();

  /* for mcall */
  HOOK_SYS(mcall);
  #ifdef __NR_exit
  HOOK_SYS(exit);
  #endif
  #ifdef __NR_exit_group
  HOOK_SYS(exit_group);
  #endif

  /* +++ begin of {{syscall_hooks}} +++ */

  /* group sys */
  #ifdef __NR_times
  HOOK_SYS(times);
  #endif
  #ifdef __NR_sysinfo
  HOOK_SYS(sysinfo);
  #endif
  #ifdef __NR_newuname
  HOOK_SYS(newuname);
  #endif
  #ifdef __NR_umask
  HOOK_SYS(umask);
  #endif
  #ifdef __NR_sethostname
  HOOK_SYS(sethostname);
  #endif
  #ifdef __NR_setdomainname
  HOOK_SYS(setdomainname);
  #endif
  #ifdef __NR_getrlimit
  HOOK_SYS(getrlimit);
  #endif
  #ifdef __NR_setrlimit
  HOOK_SYS(setrlimit);
  #endif
  #ifdef __NR_getrusage
  HOOK_SYS(getrusage);
  #endif
  #ifdef __NR_getpriority
  HOOK_SYS(getpriority);
  #endif
  #ifdef __NR_setpriority
  HOOK_SYS(setpriority);
  #endif
  #ifdef __NR_getpid
  HOOK_SYS(getpid);
  #endif
  #ifdef __NR_gettid
  HOOK_SYS(gettid);
  #endif
  #ifdef __NR_getppid
  HOOK_SYS(getppid);
  #endif
  #ifdef __NR_getpgrp
  HOOK_SYS(getpgrp);
  #endif
  #ifdef __NR_setpgid
  HOOK_SYS(setpgid);
  #endif
  #ifdef __NR_getsid
  HOOK_SYS(getsid);
  #endif
  #ifdef __NR_setsid
  HOOK_SYS(setsid);
  #endif
  #ifdef __NR_getuid
  HOOK_SYS(getuid);
  #endif
  #ifdef __NR_setuid
  HOOK_SYS(setuid);
  #endif
  #ifdef __NR_geteuid
  HOOK_SYS(geteuid);
  #endif
  #ifdef __NR_setreuid
  HOOK_SYS(setreuid);
  #endif
  #ifdef __NR_getresuid
  HOOK_SYS(getresuid);
  #endif
  #ifdef __NR_setresuid
  HOOK_SYS(setresuid);
  #endif
  #ifdef __NR_setfsuid
  HOOK_SYS(setfsuid);
  #endif
  #ifdef __NR_getgid
  HOOK_SYS(getgid);
  #endif
  #ifdef __NR_setgid
  HOOK_SYS(setgid);
  #endif
  #ifdef __NR_getegid
  HOOK_SYS(getegid);
  #endif
  #ifdef __NR_setregid
  HOOK_SYS(setregid);
  #endif
  #ifdef __NR_getresgid
  HOOK_SYS(getresgid);
  #endif
  #ifdef __NR_setresgid
  HOOK_SYS(setresgid);
  #endif
  #ifdef __NR_setfsgid
  HOOK_SYS(setfsgid);
  #endif
  #ifdef __NR_getgroups
  HOOK_SYS(getgroups);
  #endif
  #ifdef __NR_setgroups
  HOOK_SYS(setgroups);
  #endif
  #ifdef __NR_getcwd
  HOOK_SYS(getcwd);
  #endif
  #ifdef __NR_gettimeofday
  HOOK_SYS(gettimeofday);
  #endif
  #ifdef __NR_time
  HOOK_SYS(time);
  #endif
  #ifdef __NR_clock_gettime
  HOOK_SYS(clock_gettime);
  #endif
  #ifdef __NR_clock_getres
  HOOK_SYS(clock_getres);
  #endif
  #ifdef __NR_getcpu
  HOOK_SYS(getcpu);
  #endif

  /* group fs */
  #ifdef __NR_access
  HOOK_SYS(access);
  #endif
  #ifdef __NR_faccessat
  HOOK_SYS(faccessat);
  #endif
  #ifdef __NR_readlink
  HOOK_SYS(readlink);
  #endif
  #ifdef __NR_readlinkat
  HOOK_SYS(readlinkat);
  #endif
  #ifdef __NR_stat
  HOOK_SYS(stat);
  #endif
  #ifdef __NR_fstat
  HOOK_SYS(fstat);
  #endif
  #ifdef __NR_lstat
  HOOK_SYS(lstat);
  #endif
  #ifdef __NR_newfstatat
  HOOK_SYS(newfstatat);
  #endif
  #ifdef __NR_truncate
  HOOK_SYS(truncate);
  #endif
  #ifdef __NR_ftruncate
  HOOK_SYS(ftruncate);
  #endif
  #ifdef __NR_link
  HOOK_SYS(link);
  #endif
  #ifdef __NR_linkat
  HOOK_SYS(linkat);
  #endif
  #ifdef __NR_symlink
  HOOK_SYS(symlink);
  #endif
  #ifdef __NR_symlinkat
  HOOK_SYS(symlinkat);
  #endif
  #ifdef __NR_unlink
  HOOK_SYS(unlink);
  #endif
  #ifdef __NR_unlinkat
  HOOK_SYS(unlinkat);
  #endif
  #ifdef __NR_rename
  HOOK_SYS(rename);
  #endif
  #ifdef __NR_renameat
  HOOK_SYS(renameat);
  #endif
  #ifdef __NR_mkdir
  HOOK_SYS(mkdir);
  #endif
  #ifdef __NR_mkdirat
  HOOK_SYS(mkdirat);
  #endif
  #ifdef __NR_rmdir
  HOOK_SYS(rmdir);
  #endif
  #ifdef __NR_chdir
  HOOK_SYS(chdir);
  #endif
  #ifdef __NR_fchdir
  HOOK_SYS(fchdir);
  #endif
  #ifdef __NR_mknod
  HOOK_SYS(mknod);
  #endif
  #ifdef __NR_mknodat
  HOOK_SYS(mknodat);
  #endif
  #ifdef __NR_chmod
  HOOK_SYS(chmod);
  #endif
  #ifdef __NR_fchmod
  HOOK_SYS(fchmod);
  #endif
  #ifdef __NR_chown
  HOOK_SYS(chown);
  #endif
  #ifdef __NR_fchown
  HOOK_SYS(fchown);
  #endif
  #ifdef __NR_lchown
  HOOK_SYS(lchown);
  #endif
  #ifdef __NR_fchownat
  HOOK_SYS(fchownat);
  #endif
  #ifdef __NR_setxattr
  HOOK_SYS(setxattr);
  #endif
  #ifdef __NR_fsetxattr
  HOOK_SYS(fsetxattr);
  #endif
  #ifdef __NR_lsetxattr
  HOOK_SYS(lsetxattr);
  #endif
  #ifdef __NR_getxattr
  HOOK_SYS(getxattr);
  #endif
  #ifdef __NR_fgetxattr
  HOOK_SYS(fgetxattr);
  #endif
  #ifdef __NR_lgetxattr
  HOOK_SYS(lgetxattr);
  #endif
  #ifdef __NR_removexattr
  HOOK_SYS(removexattr);
  #endif
  #ifdef __NR_fremovexattr
  HOOK_SYS(fremovexattr);
  #endif
  #ifdef __NR_lremovexattr
  HOOK_SYS(lremovexattr);
  #endif
  #ifdef __NR_statfs
  HOOK_SYS(statfs);
  #endif
  #ifdef __NR_fstatfs
  HOOK_SYS(fstatfs);
  #endif
  #ifdef __NR_getdents
  HOOK_SYS(getdents);
  #endif

  /* group io */
  #ifdef __NR_open
  HOOK_SYS(open);
  #endif
  #ifdef __NR_openat
  HOOK_SYS(openat);
  #endif
  #ifdef __NR_creat
  HOOK_SYS(creat);
  #endif
  #ifdef __NR_close
  HOOK_SYS(close);
  #endif
  #ifdef __NR_lseek
  HOOK_SYS(lseek);
  #endif
  #ifdef __NR_read
  HOOK_SYS(read);
  #endif
  #ifdef __NR_write
  HOOK_SYS(write);
  #endif
  #ifdef __NR_pread64
  HOOK_SYS(pread64);
  #endif
  #ifdef __NR_pwrite64
  HOOK_SYS(pwrite64);
  #endif
  #ifdef __NR_readv
  HOOK_SYS(readv);
  #endif
  #ifdef __NR_writev
  HOOK_SYS(writev);
  #endif
  #ifdef __NR_pipe
  HOOK_SYS(pipe);
  #endif
  #ifdef __NR_pipe2
  HOOK_SYS(pipe2);
  #endif
  #ifdef __NR_eventfd
  HOOK_SYS(eventfd);
  #endif
  #ifdef __NR_eventfd2
  HOOK_SYS(eventfd2);
  #endif
  #ifdef __NR_epoll_create
  HOOK_SYS(epoll_create);
  #endif
  #ifdef __NR_epoll_create1
  HOOK_SYS(epoll_create1);
  #endif
  #ifdef __NR_epoll_ctl
  HOOK_SYS(epoll_ctl);
  #endif
  #ifdef __NR_sendfile
  HOOK_SYS(sendfile);
  #endif
  #ifdef __NR_sendfile64
  HOOK_SYS(sendfile64);
  #endif
  #ifdef __NR_dup
  HOOK_SYS(dup);
  #endif
  #ifdef __NR_dup2
  HOOK_SYS(dup2);
  #endif
  #ifdef __NR_dup3
  HOOK_SYS(dup3);
  #endif
  #ifdef __NR_poll
  HOOK_SYS(poll);
  #endif
  #ifdef __NR_ppoll
  HOOK_SYS(ppoll);
  #endif
  #ifdef __NR_select
  HOOK_SYS(select);
  #endif
  #ifdef __NR_pselect6
  HOOK_SYS(pselect6);
  #endif
  #ifdef __NR_fcntl
  HOOK_SYS(fcntl);
  #endif
  #ifdef __NR_ioctl
  HOOK_SYS(ioctl);
  #endif

  /* group sock */
  #ifdef __NR_socket
  HOOK_SYS(socket);
  #endif
  #ifdef __NR_socketpair
  HOOK_SYS(socketpair);
  #endif
  #ifdef __NR_shutdown
  HOOK_SYS(shutdown);
  #endif
  #ifdef __NR_connect
  HOOK_SYS(connect);
  #endif
  #ifdef __NR_bind
  HOOK_SYS(bind);
  #endif
  #ifdef __NR_accept
  HOOK_SYS(accept);
  #endif
  #ifdef __NR_accept4
  HOOK_SYS(accept4);
  #endif
  #ifdef __NR_listen
  HOOK_SYS(listen);
  #endif
  #ifdef __NR_getsockopt
  HOOK_SYS(getsockopt);
  #endif
  #ifdef __NR_setsockopt
  HOOK_SYS(setsockopt);
  #endif
  #ifdef __NR_getsockname
  HOOK_SYS(getsockname);
  #endif
  #ifdef __NR_recvfrom
  HOOK_SYS(recvfrom);
  #endif
  #ifdef __NR_sendto
  HOOK_SYS(sendto);
  #endif
  #ifdef __NR_recvmsg
  HOOK_SYS(recvmsg);
  #endif
  #ifdef __NR_sendmsg
  HOOK_SYS(sendmsg);
  #endif

  /* group mem */
  #ifdef __NR_mmap
  HOOK_SYS(mmap);
  #endif

  /* group ps */
  #ifdef __NR_wait4
  HOOK_SYS(wait4);
  #endif
  #ifdef __NR_kill
  HOOK_SYS(kill);
  #endif
  #ifdef __NR_tgkill
  HOOK_SYS(tgkill);
  #endif

  /* +++ end of block +++ */

  /* disable overriding */
  enable_page_protection();

  return 0;
}

void unhook_syscall_table(void){
  /* enable overriding */
  disable_page_protection();

  /* for mcall */
  UNHOOK_SYS(mcall);
  #ifdef __NR_exit
  UNHOOK_SYS(exit);
  #endif
  #ifdef __NR_exit_group
  UNHOOK_SYS(exit_group);
  #endif

  /* +++ begin of {{syscall_unhooks}} +++ */

  /* group sys */
  #ifdef __NR_times
  UNHOOK_SYS(times);
  #endif
  #ifdef __NR_sysinfo
  UNHOOK_SYS(sysinfo);
  #endif
  #ifdef __NR_newuname
  UNHOOK_SYS(newuname);
  #endif
  #ifdef __NR_umask
  UNHOOK_SYS(umask);
  #endif
  #ifdef __NR_sethostname
  UNHOOK_SYS(sethostname);
  #endif
  #ifdef __NR_setdomainname
  UNHOOK_SYS(setdomainname);
  #endif
  #ifdef __NR_getrlimit
  UNHOOK_SYS(getrlimit);
  #endif
  #ifdef __NR_setrlimit
  UNHOOK_SYS(setrlimit);
  #endif
  #ifdef __NR_getrusage
  UNHOOK_SYS(getrusage);
  #endif
  #ifdef __NR_getpriority
  UNHOOK_SYS(getpriority);
  #endif
  #ifdef __NR_setpriority
  UNHOOK_SYS(setpriority);
  #endif
  #ifdef __NR_getpid
  UNHOOK_SYS(getpid);
  #endif
  #ifdef __NR_gettid
  UNHOOK_SYS(gettid);
  #endif
  #ifdef __NR_getppid
  UNHOOK_SYS(getppid);
  #endif
  #ifdef __NR_getpgrp
  UNHOOK_SYS(getpgrp);
  #endif
  #ifdef __NR_setpgid
  UNHOOK_SYS(setpgid);
  #endif
  #ifdef __NR_getsid
  UNHOOK_SYS(getsid);
  #endif
  #ifdef __NR_setsid
  UNHOOK_SYS(setsid);
  #endif
  #ifdef __NR_getuid
  UNHOOK_SYS(getuid);
  #endif
  #ifdef __NR_setuid
  UNHOOK_SYS(setuid);
  #endif
  #ifdef __NR_geteuid
  UNHOOK_SYS(geteuid);
  #endif
  #ifdef __NR_setreuid
  UNHOOK_SYS(setreuid);
  #endif
  #ifdef __NR_getresuid
  UNHOOK_SYS(getresuid);
  #endif
  #ifdef __NR_setresuid
  UNHOOK_SYS(setresuid);
  #endif
  #ifdef __NR_setfsuid
  UNHOOK_SYS(setfsuid);
  #endif
  #ifdef __NR_getgid
  UNHOOK_SYS(getgid);
  #endif
  #ifdef __NR_setgid
  UNHOOK_SYS(setgid);
  #endif
  #ifdef __NR_getegid
  UNHOOK_SYS(getegid);
  #endif
  #ifdef __NR_setregid
  UNHOOK_SYS(setregid);
  #endif
  #ifdef __NR_getresgid
  UNHOOK_SYS(getresgid);
  #endif
  #ifdef __NR_setresgid
  UNHOOK_SYS(setresgid);
  #endif
  #ifdef __NR_setfsgid
  UNHOOK_SYS(setfsgid);
  #endif
  #ifdef __NR_getgroups
  UNHOOK_SYS(getgroups);
  #endif
  #ifdef __NR_setgroups
  UNHOOK_SYS(setgroups);
  #endif
  #ifdef __NR_getcwd
  UNHOOK_SYS(getcwd);
  #endif
  #ifdef __NR_gettimeofday
  UNHOOK_SYS(gettimeofday);
  #endif
  #ifdef __NR_time
  UNHOOK_SYS(time);
  #endif
  #ifdef __NR_clock_gettime
  UNHOOK_SYS(clock_gettime);
  #endif
  #ifdef __NR_clock_getres
  UNHOOK_SYS(clock_getres);
  #endif
  #ifdef __NR_getcpu
  UNHOOK_SYS(getcpu);
  #endif

  /* group fs */
  #ifdef __NR_access
  UNHOOK_SYS(access);
  #endif
  #ifdef __NR_faccessat
  UNHOOK_SYS(faccessat);
  #endif
  #ifdef __NR_readlink
  UNHOOK_SYS(readlink);
  #endif
  #ifdef __NR_readlinkat
  UNHOOK_SYS(readlinkat);
  #endif
  #ifdef __NR_stat
  UNHOOK_SYS(stat);
  #endif
  #ifdef __NR_fstat
  UNHOOK_SYS(fstat);
  #endif
  #ifdef __NR_lstat
  UNHOOK_SYS(lstat);
  #endif
  #ifdef __NR_newfstatat
  UNHOOK_SYS(newfstatat);
  #endif
  #ifdef __NR_truncate
  UNHOOK_SYS(truncate);
  #endif
  #ifdef __NR_ftruncate
  UNHOOK_SYS(ftruncate);
  #endif
  #ifdef __NR_link
  UNHOOK_SYS(link);
  #endif
  #ifdef __NR_linkat
  UNHOOK_SYS(linkat);
  #endif
  #ifdef __NR_symlink
  UNHOOK_SYS(symlink);
  #endif
  #ifdef __NR_symlinkat
  UNHOOK_SYS(symlinkat);
  #endif
  #ifdef __NR_unlink
  UNHOOK_SYS(unlink);
  #endif
  #ifdef __NR_unlinkat
  UNHOOK_SYS(unlinkat);
  #endif
  #ifdef __NR_rename
  UNHOOK_SYS(rename);
  #endif
  #ifdef __NR_renameat
  UNHOOK_SYS(renameat);
  #endif
  #ifdef __NR_mkdir
  UNHOOK_SYS(mkdir);
  #endif
  #ifdef __NR_mkdirat
  UNHOOK_SYS(mkdirat);
  #endif
  #ifdef __NR_rmdir
  UNHOOK_SYS(rmdir);
  #endif
  #ifdef __NR_chdir
  UNHOOK_SYS(chdir);
  #endif
  #ifdef __NR_fchdir
  UNHOOK_SYS(fchdir);
  #endif
  #ifdef __NR_mknod
  UNHOOK_SYS(mknod);
  #endif
  #ifdef __NR_mknodat
  UNHOOK_SYS(mknodat);
  #endif
  #ifdef __NR_chmod
  UNHOOK_SYS(chmod);
  #endif
  #ifdef __NR_fchmod
  UNHOOK_SYS(fchmod);
  #endif
  #ifdef __NR_chown
  UNHOOK_SYS(chown);
  #endif
  #ifdef __NR_fchown
  UNHOOK_SYS(fchown);
  #endif
  #ifdef __NR_lchown
  UNHOOK_SYS(lchown);
  #endif
  #ifdef __NR_fchownat
  UNHOOK_SYS(fchownat);
  #endif
  #ifdef __NR_setxattr
  UNHOOK_SYS(setxattr);
  #endif
  #ifdef __NR_fsetxattr
  UNHOOK_SYS(fsetxattr);
  #endif
  #ifdef __NR_lsetxattr
  UNHOOK_SYS(lsetxattr);
  #endif
  #ifdef __NR_getxattr
  UNHOOK_SYS(getxattr);
  #endif
  #ifdef __NR_fgetxattr
  UNHOOK_SYS(fgetxattr);
  #endif
  #ifdef __NR_lgetxattr
  UNHOOK_SYS(lgetxattr);
  #endif
  #ifdef __NR_removexattr
  UNHOOK_SYS(removexattr);
  #endif
  #ifdef __NR_fremovexattr
  UNHOOK_SYS(fremovexattr);
  #endif
  #ifdef __NR_lremovexattr
  UNHOOK_SYS(lremovexattr);
  #endif
  #ifdef __NR_statfs
  UNHOOK_SYS(statfs);
  #endif
  #ifdef __NR_fstatfs
  UNHOOK_SYS(fstatfs);
  #endif
  #ifdef __NR_getdents
  UNHOOK_SYS(getdents);
  #endif

  /* group io */
  #ifdef __NR_open
  UNHOOK_SYS(open);
  #endif
  #ifdef __NR_openat
  UNHOOK_SYS(openat);
  #endif
  #ifdef __NR_creat
  UNHOOK_SYS(creat);
  #endif
  #ifdef __NR_close
  UNHOOK_SYS(close);
  #endif
  #ifdef __NR_lseek
  UNHOOK_SYS(lseek);
  #endif
  #ifdef __NR_read
  UNHOOK_SYS(read);
  #endif
  #ifdef __NR_write
  UNHOOK_SYS(write);
  #endif
  #ifdef __NR_pread64
  UNHOOK_SYS(pread64);
  #endif
  #ifdef __NR_pwrite64
  UNHOOK_SYS(pwrite64);
  #endif
  #ifdef __NR_readv
  UNHOOK_SYS(readv);
  #endif
  #ifdef __NR_writev
  UNHOOK_SYS(writev);
  #endif
  #ifdef __NR_pipe
  UNHOOK_SYS(pipe);
  #endif
  #ifdef __NR_pipe2
  UNHOOK_SYS(pipe2);
  #endif
  #ifdef __NR_eventfd
  UNHOOK_SYS(eventfd);
  #endif
  #ifdef __NR_eventfd2
  UNHOOK_SYS(eventfd2);
  #endif
  #ifdef __NR_epoll_create
  UNHOOK_SYS(epoll_create);
  #endif
  #ifdef __NR_epoll_create1
  UNHOOK_SYS(epoll_create1);
  #endif
  #ifdef __NR_epoll_ctl
  UNHOOK_SYS(epoll_ctl);
  #endif
  #ifdef __NR_sendfile
  UNHOOK_SYS(sendfile);
  #endif
  #ifdef __NR_sendfile64
  UNHOOK_SYS(sendfile64);
  #endif
  #ifdef __NR_dup
  UNHOOK_SYS(dup);
  #endif
  #ifdef __NR_dup2
  UNHOOK_SYS(dup2);
  #endif
  #ifdef __NR_dup3
  UNHOOK_SYS(dup3);
  #endif
  #ifdef __NR_poll
  UNHOOK_SYS(poll);
  #endif
  #ifdef __NR_ppoll
  UNHOOK_SYS(ppoll);
  #endif
  #ifdef __NR_select
  UNHOOK_SYS(select);
  #endif
  #ifdef __NR_pselect6
  UNHOOK_SYS(pselect6);
  #endif
  #ifdef __NR_fcntl
  UNHOOK_SYS(fcntl);
  #endif
  #ifdef __NR_ioctl
  UNHOOK_SYS(ioctl);
  #endif

  /* group sock */
  #ifdef __NR_socket
  UNHOOK_SYS(socket);
  #endif
  #ifdef __NR_socketpair
  UNHOOK_SYS(socketpair);
  #endif
  #ifdef __NR_shutdown
  UNHOOK_SYS(shutdown);
  #endif
  #ifdef __NR_connect
  UNHOOK_SYS(connect);
  #endif
  #ifdef __NR_bind
  UNHOOK_SYS(bind);
  #endif
  #ifdef __NR_accept
  UNHOOK_SYS(accept);
  #endif
  #ifdef __NR_accept4
  UNHOOK_SYS(accept4);
  #endif
  #ifdef __NR_listen
  UNHOOK_SYS(listen);
  #endif
  #ifdef __NR_getsockopt
  UNHOOK_SYS(getsockopt);
  #endif
  #ifdef __NR_setsockopt
  UNHOOK_SYS(setsockopt);
  #endif
  #ifdef __NR_getsockname
  UNHOOK_SYS(getsockname);
  #endif
  #ifdef __NR_recvfrom
  UNHOOK_SYS(recvfrom);
  #endif
  #ifdef __NR_sendto
  UNHOOK_SYS(sendto);
  #endif
  #ifdef __NR_recvmsg
  UNHOOK_SYS(recvmsg);
  #endif
  #ifdef __NR_sendmsg
  UNHOOK_SYS(sendmsg);
  #endif

  /* group mem */
  #ifdef __NR_mmap
  UNHOOK_SYS(mmap);
  #endif

  /* group ps */
  #ifdef __NR_wait4
  UNHOOK_SYS(wait4);
  #endif
  #ifdef __NR_kill
  UNHOOK_SYS(kill);
  #endif
  #ifdef __NR_tgkill
  UNHOOK_SYS(tgkill);
  #endif

  /* +++ end of block +++ */

  /* disable overriding */
  enable_page_protection();
}
