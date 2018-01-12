/*
 * mcall.h
 *
 *  Created on: Jan 11, 2016
 *      Author: meng
 */

#ifndef MCALL_H_
#define MCALL_H_

#include <linux/kernel.h>
#include <linux/syscalls.h>

#include "logger.h"
#include "sync.h"
#include "mvee.h"

extern asmlinkage long (*ref_SYS_mcall) 
  (unsigned int cmd, unsigned long arg);
asmlinkage long new_SYS_mcall
  (unsigned int cmd, unsigned long arg);

#ifdef __NR_exit
extern asmlinkage long (*ref_SYS_exit)
  (int status);
asmlinkage long new_SYS_exit
  (int status);
#endif

#ifdef __NR_exit_group
extern asmlinkage long (*ref_SYS_exit_group)
  (int status);
asmlinkage long new_SYS_exit_group
  (int status);
#endif

#endif /* MCALL_H_ */
