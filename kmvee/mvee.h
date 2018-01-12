/* 
 * mvee.h
 *
 *  Created on: Mar 8, 2015
 *    Author: Meng
 */

#ifndef MVEE_H_
#define MVEE_H_

#include <linux/ioctl.h>

/* project meta */
#define PROJECT               "mvee"

#define PATH_DEVICE           "/dev/mvee"

#define ID_IOCTL              31

#define SIGEXT                SIGUSR1
#define SIGDEV                SIGUSR2

#define __NR_mcall            __NR_tuxcall

/* shared structs with userspace */
struct arg_create_group{
  pid_t monitor;
  unsigned short nvar;
};

struct arg_register_variant{
  unsigned int id;
  unsigned short role;
  pid_t variant;
};

/* ioctl commands */
#define CMD_CREATE_GROUP      _IOW(ID_IOCTL, 1, struct arg_create_group)
#define CMD_REGISTER_VARIANT  _IOW(ID_IOCTL, 2, struct arg_register_variant)

/* mcall commands */
#define MCALL_START_SYNC        1
#define MCALL_STOP_SYNC         2

#define MCALL_PRE_FORK          3
#define MCALL_POST_FORK         4

#ifdef SYNC_ORDER
#define MCALL_SYNC_ORDER        5
#endif

#endif /* MVEE_H */
