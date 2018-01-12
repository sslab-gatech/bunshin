/*
 * mcall.c
 *
 *  Created on: Jan 11, 2016
 *  	Author: meng
 */

#include "mcall.h"

static void pre_fork(struct vcb *vcb){
  unsigned int gid;
  struct vgroup *group;

#ifdef DEBUG
  log_d(vcb, "FORK", 0, "enter");
#endif

  group = vcb->group;
  if(vcb->role){
    /* wait for new group to be created */
    if(down_killable(&group->pre_start_sem)){
      on_fatal();
    }

    /* create child */
    vcb->child = create_variant(group->child, vcb->role);

    /* inform leader on finish */
    up(&group->pre_end_sem);
  } else {
    /* create new group */
    gid = create_group(group->monitor);
    group->child = lookup_group(gid);
        
    /* inform followers */
    for(int i=0;i<vcb->nfol;i++){
      up(&group->pre_start_sem);
    }

    /* create child */
    vcb->child = create_variant(group->child, vcb->role);

    /* wait for all followers to finish */
    for(int i=0; i<vcb->nfol; i++){
      if(down_killable(&group->pre_end_sem)){
        on_fatal();
      }
    }
  }
      
#ifdef DEBUG
  log_d(vcb, "FORK", 0, "exit");
#endif
}

static pid_t post_fork(struct vcb *vcb){

#ifdef DEBUG
  log_d(vcb, "FORK", 2, "enter");
#endif
 
  /* get child pid */
  pid_t rv;
  struct vgroup *group = vcb->group;

  if(vcb->role){
    /* wait for leader child ready */
    if(down_killable(&group->post_start_sem)){
      on_fatal();
    }

    rv = group->child->tgid;

    /* inform leader on finish */
    up(&group->post_end_sem);
  } else {
    /* inform followers on child ready */
    for(int i=0;i<vcb->nfol;i++){
      up(&group->post_start_sem);
    }

    rv = group->child->tgid; 
    
    /* wait for all followers to finish */
    for(int i=0;i<vcb->nfol;i++){
      if(down_killable(&group->post_end_sem)){
        on_fatal();
      }
    }
  }

#ifdef DEBUG
  log_d(vcb, "FORK", 2, "exit");
#endif

  return rv;
}

#ifdef SYNC_ORDER
void sync_order(struct vcb *vcb){
  unsigned int seq;
  struct oslot *slot;
  struct owait *wait;

  if(vcb->role){
    /* follower instance */

    /* wait for token */
    if(down_killable(vcb->otoken)){
      on_fatal();
    }

    seq = atomic_inc_return(vcb->otail) - 1;
    slot = vcb->oring + (seq & ORING_MOD);

    /* check if last one to fetch */
    if(atomic_dec_and_test(&slot->done)){
      slot->ready = false;
      up(vcb->osem);
    }

    /* check if need to wakeup next */
    if((++seq) != atomic_read(vcb->ohead)){
      slot = vcb->oring + (seq & ORING_MOD);

      /* wait for slot ready */
      while(!slot->ready);

      /* wake up next */
      up(vcb->owait->tokens + slot->elem);
    }
  } else {
    /* leader instance */

    /* ensure there are free slots */
    if(down_killable(vcb->osem)){
      on_fatal();
    }

    /* put order info to slot */
    seq = atomic_inc_return(vcb->ohead) - 1;
    slot = vcb->oring + (seq & ORING_MOD);

    slot->elem = vcb->egid;
    atomic_set(&slot->done, vcb->nfol);
    slot->ready = true;

    /* check if need to wakeup */
    for(int i=0;i<vcb->nfol;i++){
      if(atomic_read(vcb->otail + i) == seq){
        wait = vcb->owait + i;
        up(wait->tokens + vcb->egid);
      }
    }
  }
}
#endif

asmlinkage long new_SYS_mcall
  (unsigned int cmd, unsigned long arg){

  struct vcb *vcb = lookup_variant(current);
  if(!vcb){
    return ref_SYS_mcall(cmd, arg);
  }
  
  switch(cmd){
    case MCALL_START_SYNC:
      vcb->in_sync = true;
      return 0;

    case MCALL_STOP_SYNC:
      vcb->in_sync = false;
      return 0;

    case MCALL_PRE_FORK:
      pre_fork(vcb);
      return 0;

    case MCALL_POST_FORK:
      return post_fork(vcb);

#ifdef SYNC_ORDER
    case MCALL_SYNC_ORDER:
      sync_order(vcb);
      return 0;
#endif
  }

  log_err("command %d not recognized", cmd);
  return -EINVAL;
}

#ifdef __NR_exit
asmlinkage long new_SYS_exit
  (int status){

  /* filter out non-variants */
  struct vcb *vcb = lookup_variant(current);

  if(!vcb){
    return ref_SYS_exit(status);
  }

  unregister_variant(vcb);

#ifdef TRACE
  log_inf("%d:%d:%s:%s:%d",
      vcb->group->id, atomic_read(&vcb->index), "SYS", "exit", status);
#endif
 
  return ref_SYS_exit(status);
}
#endif

#ifdef __NR_exit_group
asmlinkage long new_SYS_exit_group
  (int status){

  /* filter out non-variants */
  struct vcb *vcb = lookup_variant(current);

  if(!vcb){
    return ref_SYS_exit_group(status);
  }

  unregister_variant(vcb);

#ifdef TRACE
  log_inf("%d:%d:%s:%s:%d",
      vcb->group->id, atomic_read(&vcb->index), "SYS", "exit_group", status);
#endif
 
  return ref_SYS_exit_group(status);
}
#endif
