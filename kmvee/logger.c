/*
 * logger.c
 *
 *  Created on: Mar 8, 2016
 *      Author: Meng
 */

#include <linux/kernel.h>

#include "mvee.h"
#include "logger.h"

#define LOG_SIZE 512

#ifdef DEBUG
void log_dbg(char *fmt, ...){
  char msg[LOG_SIZE];

  va_list args;
  va_start(args, fmt);
  vsnprintf(msg, LOG_SIZE, fmt, args);
  va_end(args);
  
  printk(KERN_INFO "[%s] %s\n", PROJECT, msg);
}

void log_d(struct vcb *vcb, char *cat, int sub, char *msg){
  log_dbg("%d:%hd:%d:%d:%s:%d:%s", 
      vcb->group->id, vcb->role, vcb->task->pid, atomic_read(&vcb->index), 
      cat, sub, msg);
}
#endif

void log_inf(char *fmt, ...){
  char msg[LOG_SIZE];
  
  va_list args;
  va_start(args, fmt);
  vsnprintf(msg, LOG_SIZE, fmt, args);
  va_end(args);
  
  printk(KERN_NOTICE "[%s] %s\n", PROJECT, msg);
}

void log_i(struct vcb *vcb, char *cat, int sub, char *msg){
  log_inf("%d:%hd:%d:%d:%s:%d:%s",
      vcb->group->id, vcb->role, vcb->task->pid, atomic_read(&vcb->index), 
      cat, sub, msg);
}

void log_err(char *fmt, ...){
  char msg[LOG_SIZE];
  
  va_list args;
  va_start(args, fmt);
  vsnprintf(msg, LOG_SIZE, fmt, args);
  va_end(args);

  printk(KERN_ERR "[%s] %s\n", PROJECT, msg);
}

void log_e(struct vcb *vcb, char *cat, int sub, char *msg){
  log_err("%d:%hd:%d:%d:%s:%d:%s",
      vcb->group->id, vcb->role, vcb->task->pid, 
      atomic_read(&vcb->index), cat, sub, msg);
}
