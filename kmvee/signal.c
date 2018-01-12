/*
 * signal.c
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

int (*KFUNC_signal_generate)
  (int sig, struct siginfo *info, struct task_struct *p, bool group);

static int khook_KFUNC_signal_generate
  (int sig, struct siginfo *info, struct task_struct *p, bool group){

  struct vcb *vcb = lookup_variant(p);
  if(vcb && !vcb->role && vcb->in_sync){ 

    /* leader received signal */
    struct vcb *cursor;
    struct task_struct *t;
    unsigned int index;
    bool suspend;

    /* temporarily block the signal */
    spin_lock_irq(&p->sighand->siglock);
    if(!sigismember(&p->blocked, sig)){
      sigaddset(&p->blocked, sig);
      suspend = true;
    }
    spin_unlock_irq(&p->sighand->siglock);

    if(suspend){
      /* the signal will be delivered upon the next syscall */
      index = atomic_read(&vcb->index) + 1;

      spin_lock(&vcb->siglock);
      kfifo_put(&vcb->sigqueue, sig);
      if(!vcb->sigindex){
        vcb->sigindex = index;
      }
      spin_unlock(&vcb->siglock);

      /* block and then deliver signal for followers */
      list_for_each_entry(cursor, &vcb->group->followers, entry){
        t = cursor->task;
        spin_lock_irq(&t->sighand->siglock);
        sigaddset(&t->blocked, sig);
        spin_unlock_irq(&t->sighand->siglock);

        spin_lock(&cursor->siglock);
        kfifo_put(&cursor->sigqueue, sig);
        if(!cursor->sigindex){
          cursor->sigindex = index;
        }
        spin_unlock(&cursor->siglock);

        KFUNC_signal_generate(sig, info, cursor->task, group);
      }

#ifdef DEBUG
      log_d(vcb, "SIG", sig, "schedule");
#endif
    }
  }

  jprobe_return();
  return 0;
}

static struct jprobe KPROBE_signal_generate = {
  .entry      = khook_KFUNC_signal_generate,
};

int hook_signal_functions(void){
  /* acquire symbols first */
  KFUNC_signal_generate = (void *)kallsyms_lookup_name("do_send_sig_info");
  if(!KFUNC_signal_generate){
    log_err("unable to find signal generation function");
    return -1;
  }

  /* prepare jprobes */
  KPROBE_signal_generate.kp.addr = (kprobe_opcode_t *)KFUNC_signal_generate;

  int rv;
  rv = register_jprobe(&KPROBE_signal_generate);
  if(rv < 0){
    log_err("unable to hook signal generation function");
    return -1;
  }

  return 0;
}

void unhook_signal_functions(void){
  unregister_jprobe(&KPROBE_signal_generate);
}
