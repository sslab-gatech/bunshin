/*
 * sync.h
 *
 *  Created on: Sep 5, 2015
 *      Author: meng
 */

#ifndef SYNC_H_
#define SYNC_H_

#include <linux/kernel.h>
#include <linux/version.h>
#include <linux/sched.h>

#include <linux/list.h>
#include <linux/hashtable.h>
#include <linux/kfifo.h>

#include <linux/spinlock.h>
#include <linux/semaphore.h>
#include <linux/mutex.h>
#include <asm/atomic.h>

#include <linux/slab.h>
#include <linux/vmalloc.h>

#include <linux/uprobes.h>

#if LINUX_VERSION_CODE >= KERNEL_VERSION(3, 17, 0)
#include <linux/timekeeping.h>
#else
#include <linux/hrtimer.h>
#endif

/* configs */
#define HASHTABLE_BITS              8

#define PARAM_NUM                   6

#ifdef LOCKSTEP
#define RING_SIZE                   1
#define RING_MOD                    0
#else
#define RING_SIZE                   256
#define RING_MOD                    255
#endif

#define ORING_SIZE                  512
#define ORING_MOD                   511
#define OWAIT_SIZE                  16

#define SIGQUEUE_SIZE               _NSIG

/* alias types */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(3, 19, 0)
#define MSGHDR_TYPE struct user_msghdr
#else
#define MSGHDR_TYPE struct msghdr
#endif

/* ring buffer elements */
typedef union{
  long val;
  void *ptr;
} holder_t;

struct sparam{
  long sysno;
  holder_t params[PARAM_NUM];
};

struct sresult{
  long retval;
  void *results[PARAM_NUM];
};

struct ssync{
  struct semaphore pavail;
  struct semaphore pcount;
  atomic_t pdone;
  struct semaphore ravail;
  struct semaphore rcount;
  atomic_t rdone;
};

struct oslot{
  bool ready;
  atomic_t done;
  unsigned int elem;
};

struct owait{
  struct semaphore tokens[OWAIT_SIZE]; 
};

/* data structure */
struct mcb{
  /* task repr */
  struct task_struct *task;

  /* number of variants */
  unsigned short nvar;

  /* count */
  atomic_t count;

  /* gid base */
  unsigned int gbase;

#ifdef SYNC_ORDER 
  /* sync order ring buffer */
  struct oslot oring[ORING_SIZE];
  /* semaphore to procect the order ring buffer */
  struct semaphore osem;
  /* global header position */
  atomic_t ohead;
  /* variant local tail position */
  atomic_t *otails;
  /* task local tokens */
  struct owait *owaits;
  /* variant local mutex */
  struct mutex *omutexes;
#endif

  /* for `monitors` hashtable */
  struct hlist_node node;
};

struct vgroup{
  /* group id */
  unsigned int id;

  /* monitor */
  struct mcb *monitor;

  /* ring buffers */
  struct sparam rparam[RING_SIZE];
  struct sresult rresult[RING_SIZE];
  struct ssync rsync[RING_SIZE];

  /* for sync order */
  atomic_t order_index;

  /* thread group id */
  pid_t tgid;

  /* leader */
  struct vcb *leader;

  /* hold follower list */
  struct list_head followers;

  /* lock for follower list */
  spinlock_t lock;

  /* semaphores */
  struct semaphore init_sem;
  struct semaphore fini_sem;

  /* for thread */
  struct semaphore pre_start_sem;
  struct semaphore pre_end_sem;
  struct semaphore post_start_sem;
  struct semaphore post_end_sem;
  struct vgroup *child;

  /* for `vgroups` hashtable */
  struct hlist_node node;
};

struct vcb{
  /* task repr */
  struct task_struct *task;

  /* status */
  bool in_sync;

  /* index */
  atomic_t index;

  /* role (0 if leader) */
  unsigned short role;

  /* group id */
  unsigned int egid;

  /* number of followers */
  unsigned short nfol;

  /* ring buffers */
  struct sparam *rparam;
  struct sresult *rresult;
  struct ssync *rsync;

#ifdef SYNC_ORDER 
  /* for order sync */
  struct oslot *oring;
  struct semaphore *osem;
  atomic_t *ohead;
  atomic_t *otail;
  struct owait *owait;
  struct mutex *omutex;
  struct semaphore *otoken;
#endif

  /* for fast task switch */
  union{
    struct vcb *leader;
    struct list_head *followers;
  };

  /* the variant group it belongs to */
  struct vgroup *group;
  
  /* for signal */
  unsigned int sigindex;
  spinlock_t siglock;
  DECLARE_KFIFO(sigqueue, int, SIGQUEUE_SIZE);

  /* for thread */
  struct vcb *child;

  /* for `followers` linked list */
  struct list_head entry;

  /* for `variants` hashtable */
  struct hlist_node node;
};

/* global variables */
extern rwlock_t monitors_lock;
extern DECLARE_HASHTABLE(monitors, HASHTABLE_BITS);

extern atomic_t groups_count;
extern rwlock_t groups_lock;
extern DECLARE_HASHTABLE(groups, HASHTABLE_BITS);

extern rwlock_t variants_lock;
extern DECLARE_HASHTABLE(variants, HASHTABLE_BITS);

/* monitor management */
struct mcb *create_monitor(struct task_struct *task, unsigned short nvar);
void destroy_monitor(struct mcb *mcb);

/* group management */
int create_group(struct mcb *mcb);
void destroy_group(struct vgroup *group);
struct vgroup *lookup_group(int id);

/* variant management */
struct vcb *create_variant(struct vgroup *group, unsigned short role);
void register_variant(struct vcb *vcb, struct task_struct *task);
void unregister_variant(struct vcb *vcb);
void unregister_killed_variant(struct vcb *vcb);
struct vcb *lookup_variant(struct task_struct *task);

/* kernel space helpers */
int hook_signal_functions(void);
void unhook_signal_functions(void);
int hook_thread_functions(void);
void unhook_thread_functions(void);

/* signal sync */
void sync_signal(struct vcb *vcb);

/* callbacks */
void on_fatal(void);
void on_deviation(struct vcb *vcb);

#endif /* SYNC_H_ */
