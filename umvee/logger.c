/*
 * logger.c
 *
 *  Created on: Mar 8, 2016
 *      Author: Meng
 */

#include <stdio.h>
#include <stdarg.h>

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
  
  fprintf(stderr, "[%s] %s\n", PROJECT, msg);
}
#endif

void log_inf(char *fmt, ...){
  char msg[LOG_SIZE];
  
  va_list args;
  va_start(args, fmt);
  vsnprintf(msg, LOG_SIZE, fmt, args);
  va_end(args);
  
  fprintf(stderr, "[%s] %s\n", PROJECT, msg);
}

void log_err(char *fmt, ...){
  char msg[LOG_SIZE];
  
  va_list args;
  va_start(args, fmt);
  vsnprintf(msg, LOG_SIZE, fmt, args);
  va_end(args);

  fprintf(stderr, "[%s] %s\n", PROJECT, msg);
}
