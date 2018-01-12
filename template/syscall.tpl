{{def_new_syscall}}{

  /* filter out non-variants */
  struct vcb *vcb = lookup_variant(current);

  if(!vcb || !vcb->in_sync){
    {{ref}}
  } 

  long retval = 0;

  unsigned int seq = atomic_inc_return(&vcb->index);

  unsigned int index = (seq - 1) & RING_MOD;
  struct sparam *pslot = vcb->rparam + index;
  struct sresult *rslot = vcb->rresult + index;
  struct ssync *sslot = vcb->rsync + index;

#ifdef DEBUG
  log_d(vcb, "SYS", __NR_{{sysname}}, "enter");
#endif

  /* variable declarations */
  {{vardef}}

  /* pre-sync operations, for both leader and follower */
  {{pre}}

  if(vcb->role){
    /* follower instance */

    {{fpre}}

    /* wait for params to be ready */
    if(down_killable(&sslot->pcount)){
      on_fatal();
    }

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "pready");
#endif

    /* compare params */
    if(pslot->sysno != __NR_{{sysname}}){
      log_e(vcb, "SYS", __NR_{{sysname}}, "deviation -> sysno"); 
      on_deviation(vcb);
    }
    {{compare}}

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "compare");
#endif

    /* show we have consumed the params */
    if(atomic_dec_and_test(&sslot->pdone)){
      {{pclean}}

      up(&sslot->pavail);

#ifdef DEBUG
      log_d(vcb, "SYS", __NR_{{sysname}}, "pclean");
#endif
    }

    /* follower specific logic */
    {{fexe}}

    /* wait for results to be ready */
    if(down_killable(&sslot->rcount)){
      on_fatal();
    }

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "rready");
#endif

    /* fetch result */
    retval = rslot->retval;
    {{fetch}}

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "fetch");
#endif

    if(atomic_dec_and_test(&sslot->rdone)){
      {{rclean}}

      up(&sslot->ravail);

#ifdef DEBUG
      log_d(vcb, "SYS", __NR_{{sysname}}, "rclean");
#endif
    }

    {{fpost}}

  } else {
    /* leader instance */

    {{lpre}}

#if !defined(LOCKSTEP) && !defined(LOCKSTEP_SYS_{{sysname}})
    /* wait for param consumption by all variants */
    if(down_killable(&sslot->pavail)){
      on_fatal();
    }

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "pavail");
#endif
#endif

    /* checkin params */
    pslot->sysno = __NR_{{sysname}};
    {{checkin}}

    /* inform all that params are ready */
    atomic_set(&sslot->pdone, vcb->nfol);
    for(int i=0;i<vcb->nfol;i++){
      up(&sslot->pcount);
    }

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "checkin");
#endif

#if defined(LOCKSTEP) || defined(LOCKSTEP_SYS_{{sysname}})
    /* wait for param consumption by all variants */
    if(down_killable(&sslot->pavail)){
      on_fatal();
    }

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "pavail");
#endif
#endif

    /* leader specific execution logic */
    {{lexe}}

    /* execute the syscall */
    {{exe}}

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "exec");
#endif

    /* wait for results consumption by all variables */
    if(down_killable(&sslot->ravail)){
      on_fatal();
    }

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "ravail");
#endif

    /* turnin results */
    rslot->retval = retval;
    {{turnin}}

    /* inform all that results are ready */
    atomic_set(&sslot->rdone, vcb->nfol);
    for(int i=0;i<vcb->nfol;i++){
      up(&sslot->rcount);
    }

#ifdef DEBUG
    log_d(vcb, "SYS", __NR_{{sysname}}, "turnin");
#endif

    {{lpost}}

#ifdef TRACE
    log_inf("%d:%d:%s:%s:%ld", 
        vcb->group->id, atomic_read(&vcb->index), 
        "SYS", "{{sysname}}", retval);
#endif
  }

  /* post-sync operations, for both leader and follower */
  {{post}}

#ifdef DEBUG
  log_d(vcb, "SYS", __NR_{{sysname}}, "exit");
#endif

  /* release pending signals */
  spin_lock(&vcb->siglock);
  if(seq == vcb->sigindex){
    sync_signal(vcb);
  }
  spin_unlock(&vcb->siglock);

  return retval;
}

