/*
 * ctl.c
 *
 *  Created on: Mar 8, 2016
 *    Author: Meng
 */

#include <linux/slab.h>
#include <linux/kmod.h>
#include <linux/fs.h>
#include <linux/namei.h>
#include <linux/err.h>
#include <asm/string.h>

#include "mvee.h"
#include "logger.h"
#include "sync.h"

/* monitor management */
struct mcb *create_monitor(struct task_struct *task, unsigned short nvar){
  struct mcb *mcb = kzalloc(sizeof(struct mcb), GFP_KERNEL);

  mcb->task = task;
  mcb->nvar = nvar;

  atomic_set(&mcb->count, 0);
  mcb->gbase = atomic_read(&groups_count) + 1;

#ifdef SYNC_ORDER
  unsigned short nfol = nvar - 1;
  sema_init(&mcb->osem, ORING_SIZE);
  atomic_set(&mcb->ohead, 0);
  mcb->otails = kzalloc(sizeof(atomic_t) * nfol, GFP_KERNEL);
  mcb->owaits = kzalloc(sizeof(struct owait) * nfol, GFP_KERNEL);
  mcb->omutexes = kzalloc(sizeof(struct mutex) * nfol, GFP_KERNEL);

  struct owait *cursor;
  for(int i=0;i<nfol;i++){
    atomic_set(mcb->otails + i, 0);

    cursor = mcb->owaits + i;
    for(int j=0;j<OWAIT_SIZE;j++){
      sema_init(cursor->tokens + j, 0);
    }

    mutex_init(mcb->omutexes + i);
  }
#endif

  /* add to hashtable */
  write_lock(&monitors_lock);
  hash_add(monitors, &mcb->node, (unsigned long)task);
  write_unlock(&monitors_lock);

  return mcb;
}

void destroy_monitor(struct mcb *mcb){
  /* inform monitor */
  if(mcb->task){
    force_sig(SIGEXT, mcb->task);
  }

  /* remove from hashtable */
  write_lock(&monitors_lock);
  hash_del(&mcb->node);
  write_unlock(&monitors_lock);

  /* free itself */
#ifdef SYNC_ORDER
  kfree(mcb->otails);
  kfree(mcb->owaits);
  kfree(mcb->omutexes);
#endif

  kfree(mcb);
}

/* group management */
int create_group(struct mcb *monitor){
  struct vgroup *group = kzalloc(sizeof(struct vgroup), GFP_KERNEL);

  atomic_inc(&monitor->count);

  group->id = atomic_inc_return(&groups_count);

  group->monitor = monitor;

  struct ssync *cursor;
  for(int i=0;i<RING_SIZE;i++){
    cursor = group->rsync + i;

#ifdef LOCKSTEP
    sema_init(&cursor->pavail, 0);
#else
    sema_init(&cursor->pavail, 1);
#endif
    sema_init(&cursor->pcount, 0);
    atomic_set(&cursor->pdone, 0);

    sema_init(&cursor->ravail, 1);
    sema_init(&cursor->rcount, 0);
    atomic_set(&cursor->rdone, 0);
  }

  atomic_set(&group->order_index, 0);

  group->tgid = 0;

  group->leader = NULL;
  INIT_LIST_HEAD(&group->followers);
  spin_lock_init(&group->lock);

  sema_init(&group->init_sem, 0);
  sema_init(&group->fini_sem, 0);

  /* for thread */
  sema_init(&group->pre_start_sem, 0);
  sema_init(&group->pre_end_sem, 0);
  sema_init(&group->post_start_sem, 0);
  sema_init(&group->post_end_sem, 0);
  group->child = NULL;

  /* add to hashtable */
  write_lock(&groups_lock);
  hash_add(groups, &group->node, group->id);
  write_unlock(&groups_lock);

  return group->id;
}

void destroy_group(struct vgroup *group){
  /* inform monitor */
  struct mcb *monitor = group->monitor;
  if(atomic_dec_and_test(&monitor->count)){
    destroy_monitor(monitor);
  }

  /* remove from hashtable */
  write_lock(&groups_lock);
  hash_del(&group->node);
  write_unlock(&groups_lock);

  /* free itself */
  kfree(group);
}

struct vgroup *lookup_group(int id){
  struct vgroup *group;

  read_lock(&groups_lock);
  hash_for_each_possible(groups, group, node, id){
    if(group->id == id){
      read_unlock(&groups_lock);
      return group;
    }
  }
  read_unlock(&groups_lock);

  return NULL;
}

/* variant management */
struct vcb *create_variant(struct vgroup *group, unsigned short role){

  struct vcb *vcb;
  struct mcb *monitor = group->monitor;

  /* init basic info */
  vcb = kzalloc(sizeof(struct vcb), GFP_KERNEL);
  vcb->task = NULL;
  
  atomic_set(&vcb->index, 0);
  vcb->role = role;
  vcb->egid = group->id - monitor->gbase;
  vcb->nfol = monitor->nvar - 1;

  /* status */
  vcb->in_sync = false;

  /* buffers */
  vcb->rparam = group->rparam;
  vcb->rresult = group->rresult;
  vcb->rsync = group->rsync;

#ifdef SYNC_ORDER
  /* order sync */
  vcb->oring = monitor->oring;
  vcb->osem = &monitor->osem;
  vcb->ohead = &monitor->ohead;
#endif

  /* for order sync */
  if(role){
    /* follower instance */

#ifdef SYNC_ORDER
    /* for order sync */
    vcb->otail = monitor->otails + (role - 1);
    vcb->owait = monitor->owaits + (role - 1);
    vcb->omutex = monitor->omutexes + (role - 1);
    vcb->otoken = vcb->owait->tokens + vcb->egid;
#endif

    /* wait for leader to finish init first */
    down(&group->init_sem);

    spin_lock(&group->lock);
    list_add_tail(&vcb->entry, &group->followers);
    spin_unlock(&group->lock);

    vcb->leader = group->leader;
  } else {
    /* leader instance */

#ifdef SYNC_ORDER
    /* for order sync */
    vcb->otail = monitor->otails;
    vcb->owait = monitor->owaits;
    vcb->omutex = monitor->omutexes;
    vcb->otoken = NULL;
#endif

    group->leader = vcb;
    /* inform all followers */
    for(int i=0;i<vcb->nfol;i++){
      up(&group->init_sem);
    }

    vcb->followers = &group->followers;
  }

  vcb->group = group;

  /* for signal */
  vcb->sigindex = 0;
  spin_lock_init(&vcb->siglock);
  INIT_KFIFO(vcb->sigqueue);

  /* for thread */
  vcb->child = NULL;

  return vcb;
}

void register_variant(struct vcb *vcb, struct task_struct *task){

  vcb->task = task;

  if(!vcb->role){
    vcb->group->tgid = task_pid_vnr(task);
  }

  /* add to hashtable */
  write_lock(&variants_lock);
  hash_add(variants, &vcb->node, task->pid);
  write_unlock(&variants_lock);

#ifdef DEBUG
  log_d(vcb, "VAR", 0, "register");
#endif
}

void unregister_variant(struct vcb *vcb){
#ifdef DEBUG
  log_d(vcb, "VAR", 0, "unregister");
#endif

  struct vgroup *group = vcb->group;

  if(vcb->role){
    /* follower instance */

    spin_lock(&group->lock);
    list_del(&vcb->entry);
    spin_unlock(&group->lock);

    /* inform leader on unregister */
    up(&group->fini_sem);
  } else {
    /* leader instance */

    /* wait for all followers to unregister first */
    for(int i=0;i<vcb->nfol;i++){
      down(&group->fini_sem);
    }

    /* instruct variant group to finish */
    destroy_group(group);
  }

  /* remove from hashtable */
  write_lock(&variants_lock);
  hash_del(&vcb->node);
  write_unlock(&variants_lock);

  /* free itself */
  kfree(vcb);
}

void unregister_killed_variant(struct vcb *vcb){
  struct vgroup *group = vcb->group;

  if(vcb->role){
    /* follower instance */

    spin_lock(&group->lock);
    list_del(&vcb->entry);
    spin_unlock(&group->lock);
  } 

  /* remove from hashtable */
  write_lock(&variants_lock);
  hash_del(&vcb->node);
  write_unlock(&variants_lock);

  /* free itself */
  kfree(vcb);
}

struct vcb *lookup_variant(struct task_struct *task){
  struct vcb *vcb;

  read_lock(&variants_lock);
  hash_for_each_possible(variants, vcb, node, task->pid){
    if(vcb->task == task){
      read_unlock(&variants_lock);
      return vcb;
    }
  }
  read_unlock(&variants_lock);

  return NULL;
}

/* signal sync */
void sync_signal(struct vcb *vcb){
  struct task_struct *t = vcb->task;
  int sig;

  while(!kfifo_is_empty(&vcb->sigqueue)){
    kfifo_get(&vcb->sigqueue, &sig);
    spin_lock_irq(&t->sighand->siglock);
    sigdelset(&t->blocked, sig);
    spin_unlock_irq(&t->sighand->siglock);

#ifdef DEBUG
    log_d(vcb, "SIG", sig, "deliver");
#endif
  }

  set_tsk_thread_flag(t, TIF_SIGPENDING);

  vcb->sigindex = 0;
}

/* fault and deviation handling */
void on_fatal(void){
  do_exit(-EINTR);
}

void on_deviation(struct vcb *vcb){
  struct vgroup *group = vcb->group;

  /* inform monitor */
  force_sig(SIGDEV, group->monitor->task);

  /* kill everyone except itself */
  struct vcb *cursor, *tmp;

  force_sig(SIGKILL, group->leader->task);

  list_for_each_entry(cursor, &group->followers, entry){
    if(current != cursor->task){
      force_sig(SIGKILL, cursor->task);
    }
  }

  list_for_each_entry_safe(cursor, tmp, &group->followers, entry){
    unregister_killed_variant(cursor);
  }

  destroy_group(group);

  /* exit itself */
  do_exit(-EINTR);
}
