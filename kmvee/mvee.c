/*
 * mvee.c
 *
 *  Created on: Mar 8, 2016
 *      Author: Meng
 */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/fs.h>
#include <linux/pid.h>
#include <linux/stat.h>
#include <linux/namei.h>
#include <linux/miscdevice.h>

#include "mvee.h"
#include "logger.h"
#include "sync.h"
#include "systable.h"

/* init stages */
#define ITEM_DEVICE                   1
#define ITEM_SIGNAL                   2
#define ITEM_THREAD                   4
#define ITEM_SYSTABLE                 8

/* global variables */
rwlock_t monitors_lock;
DECLARE_HASHTABLE(monitors, HASHTABLE_BITS);

atomic_t groups_count;
rwlock_t groups_lock;
DECLARE_HASHTABLE(groups, HASHTABLE_BITS);

rwlock_t variants_lock;
DECLARE_HASHTABLE(variants, HASHTABLE_BITS);

/* helpers */
static struct task_struct *pid_to_task(pid_t val){
  struct pid *pid;

  pid = find_vpid(val);
  if(!pid){
    return NULL;
  }

  return pid_task(pid, PIDTYPE_PID);
}

/* interface */
static int mvee_open(struct inode *i, struct file *f){
  return 0;
}

static int mvee_close(struct inode *i, struct file *f){
  return 0;
}

static long mvee_ioctl(struct file *f, unsigned int cmd, unsigned long arg){
  int rv;

  struct arg_create_group *arg_cg;
  struct arg_register_variant *arg_rv;

  struct task_struct *task;
  struct mcb *mcb;
  struct vcb *vcb;
  struct vgroup *group;

  /* command execution */
  switch(cmd){
    case CMD_CREATE_GROUP:
      arg_cg = (struct arg_create_group *)arg;

      task = pid_to_task(arg_cg->monitor);
      if(!task){
        log_err("unable to locate monitor %d", arg_cg->monitor);
        return -EINVAL;
      }

      mcb = create_monitor(task, arg_cg->nvar);
      if(!mcb){
        log_err("unable to create monitor");
        return -EINVAL;
      }

      rv = create_group(mcb);
      if(rv < 0){
        log_err("failed to create group for monitor %d", arg_cg->monitor);
        return -EINVAL;
      }

      return rv;

    case CMD_REGISTER_VARIANT:
      arg_rv = (struct arg_register_variant *)arg;

      task = pid_to_task(arg_rv->variant);
      if(!task){
        log_err("unable to locate variant %d", arg_rv->variant);
        return -EINVAL;
      }

      group = lookup_group(arg_rv->id);
      if(!group){
        log_err("unable to lookup group %d", arg_rv->id);
        return -EINVAL;
      }

      vcb = create_variant(group, arg_rv->role);
      if(!vcb){
        log_err("failed to register variant %d", arg_rv->variant);
        return -EINVAL;
      }

      register_variant(vcb, task);

      return 0;
  }

  log_err("command %d not recognized", cmd);
  return -EINVAL;
}

static const struct file_operations mvee_ops = {
  .owner              = THIS_MODULE,
  .open               = mvee_open,
  .release            = mvee_close,
  .unlocked_ioctl     = mvee_ioctl,
};

static struct miscdevice mvee_dev = {
  .minor              = MISC_DYNAMIC_MINOR,
  .name               = PROJECT,
  .fops               = &mvee_ops,
  .mode               = 0666,
};

static int __init mvee_start(void){
#ifdef DEBUG
  log_dbg("starting module");
#endif

  int initialized = 0;

  /* initialize global variables */
  rwlock_init(&monitors_lock);
  hash_init(monitors);

  atomic_set(&groups_count, 0);
  rwlock_init(&groups_lock);
  hash_init(groups);

  rwlock_init(&variants_lock);
  hash_init(variants);

  /* create device entry */
  if(misc_register(&mvee_dev)){
    log_err("failed to register device entry");
    goto err;
  }

  initialized |= ITEM_DEVICE;

#ifdef DEBUG
  log_dbg("device entry registered");
#endif

  /* hook signal functions */
  if(hook_signal_functions()){
    log_err("failed to hook signal functions");
    goto err;
  }

  initialized |= ITEM_SIGNAL;

#ifdef DEBUG
  log_dbg("signal functions hooked");
#endif

  /* hook thread functions */
  if(hook_thread_functions()){
    log_err("failed to hook thread functions");
    goto err;
  }

  initialized |= ITEM_THREAD;

#ifdef DEBUG
  log_dbg("thread functions hooked");
#endif

  /* hook syscall table */
  if(hook_syscall_table()){
    log_err("failed to hook syscall table");
    goto err;
  }

  initialized |= ITEM_SYSTABLE;

#ifdef DEBUG
  log_dbg("syscall table hooked");
#endif

  /* everything goes fine */
  log_inf("module started");

  return 0;

err:
  /* remove device entry */
  if(initialized & ITEM_DEVICE){
    misc_deregister(&mvee_dev);
#ifdef DEBUG
    log_dbg("device entry removed");
#endif
  }

  /* unhook signal functions */
  if(initialized & ITEM_SIGNAL){
    unhook_signal_functions();
#ifdef DEBUG
    log_dbg("signal functions unhooked");
#endif
  }

  /* unhook thread functions */
  if(initialized & ITEM_THREAD){
    unhook_thread_functions();
#ifdef DEBUG
    log_dbg("thread functions unhooked");
#endif
  }

  /* unhook syscall table */
  if(initialized & ITEM_SYSTABLE){
    unhook_syscall_table();
#ifdef DEBUG
    log_dbg("syscall table unhooked");
#endif
  }

  /* something is wrong */
  log_err("module initialization failed");

  return -1;
}

static void __exit mvee_end(void){
#ifdef DEBUG
  log_dbg("stopping module");
#endif

  /* remove device entry */
  misc_deregister(&mvee_dev);

#ifdef DEBUG
  log_dbg("device entry removed");
#endif

  /* unhook signal functions */
  unhook_signal_functions();

#ifdef DEBUG
  log_dbg("signal functions unhooked");
#endif

  /* unhook thread functions */
  unhook_thread_functions();

#ifdef DEBUG
  log_dbg("thread functions unhooked");
#endif

  /* unhook syscall table */
  unhook_syscall_table();

#ifdef DEBUG
  log_dbg("syscall table unhooked");
#endif

  log_inf("module stopped");
}

module_init(mvee_start);
module_exit(mvee_end);

MODULE_AUTHOR("Meng Xu");
MODULE_LICENSE("GPL"); 
