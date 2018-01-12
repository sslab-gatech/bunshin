/* 
 * logger.h
 *
 *  Created on: Mar 8, 2016
 *  	Author: Meng
 */

#ifndef LOGGER_H_
#define LOGGER_H_

#ifdef DEBUG
void log_dbg(char *fmt, ...);
#endif
void log_inf(char *fmt, ...);
void log_err(char *fmt, ...);

#endif /* LOGGER_H */
