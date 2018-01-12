/*
 * thread.c
 *
 *  Created on: Mar 8, 2016,
 *    Author: Meng
 *
 */

#include <linux/kernel.h>
#include <linux/kprobes.h>
#include <linux/kallsyms.h>
#include <asm/signal.h>

#include "mvee.h"
#include "logger.h"
#include "sync.h"

void (*KFUNC_thread_init)
  (struct task_struct *t);

static void khook_KFUNC_thread_init
  (struct task_struct *t){

  struct vcb *vcb = lookup_variant(current);

  if(vcb && vcb->in_sync){
    register_variant(vcb->child, t);
    vcb->child->in_sync = true;

#ifdef DEBUG
    log_d(vcb->child, "FORK", 1, "init");
#endif

  }

  jprobe_return();
}

static struct jprobe KPROBE_thread_init = {
  .entry      = khook_KFUNC_thread_init,
};

int hook_thread_functions(void){
  /* acquire symbols first */
  KFUNC_thread_init = (void *)kallsyms_lookup_name("wake_up_new_task");
  if(!KFUNC_thread_init){
    log_err("unable to find thread init function");
    return -1;
  }

  /* prepare jprobes */
  KPROBE_thread_init.kp.addr = (kprobe_opcode_t *)KFUNC_thread_init;

  int rv;
  rv = register_jprobe(&KPROBE_thread_init);
  if(rv < 0){
    log_err("unable to hook thread init function");
    return -1;
  }

  return 0;
}

void unhook_thread_functions(void){
  unregister_jprobe(&KPROBE_thread_init);
}
