/* 
 * logger.h
 *
 *  Created on: Mar 8, 2016
 *  	Author: Meng
 */

#ifndef LOGGER_H_
#define LOGGER_H_

#include "sync.h"

#ifdef DEBUG
void log_dbg(char *fmt, ...);
void log_d(struct vcb *vcb, char *cat, int sub, char *msg);
#endif
void log_inf(char *fmt, ...);
void log_i(struct vcb *vcb, char *cat, int sub, char *msg);
void log_err(char *fmt, ...);
void log_e(struct vcb *vcb, char *cat, int sub, char *msg);

#endif /* LOGGER_H */
