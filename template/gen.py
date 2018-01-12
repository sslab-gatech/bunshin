#!/usr/bin/env python

from template import *

if __name__ == '__main__':

    # struct list

    STRUCT_tms = Struct("tms", 
            "struct tms", ["linux/times.h"])
    STRUCT_tms.add_member(
            Member("tms_utime", Field.SIMPLE))
    STRUCT_tms.add_member(
            Member("tms_stime", Field.SIMPLE))
    STRUCT_tms.add_member(
            Member("tms_cutime", Field.SIMPLE))
    STRUCT_tms.add_member(
            Member("tms_cstime", Field.SIMPLE))

    STRUCT_new_utsname = Struct("new_utsname", 
            "struct new_utsname", ["linux/utsname.h"])
    STRUCT_new_utsname.add_member(
            Member("sysname", Field.CHARS, "__NEW_UTS_LEN"))
    STRUCT_new_utsname.add_member(
            Member("nodename", Field.CHARS, "__NEW_UTS_LEN"))
    STRUCT_new_utsname.add_member(
            Member("release", Field.CHARS, "__NEW_UTS_LEN"))
    STRUCT_new_utsname.add_member(
            Member("version", Field.CHARS, "__NEW_UTS_LEN"))
    STRUCT_new_utsname.add_member(
            Member("machine", Field.CHARS, "__NEW_UTS_LEN"))
    STRUCT_new_utsname.add_member(
            Member("domainname", Field.CHARS, "__NEW_UTS_LEN"))

    STRUCT_sysinfo = Struct("sysinfo",
            "struct sysinfo", ["linux/sysinfo.h"])
    STRUCT_sysinfo.add_member(
            Member("uptime", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("loads", Field.ARRAY, fidx=3, ftype="unsigned long"))
    STRUCT_sysinfo.add_member(
            Member("totalram", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("freeram", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("sharedram", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("bufferram", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("totalswap", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("freeswap", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("procs", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("pad", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("totalhigh", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("freehigh", Field.SIMPLE))
    STRUCT_sysinfo.add_member(
            Member("mem_unit", Field.SIMPLE))

    STRUCT_rlimit = Struct("rlimit", 
            "struct rlimit", ["linux/resource.h"])
    STRUCT_rlimit.add_member(
            Member("rlim_cur", Field.SIMPLE))
    STRUCT_rlimit.add_member(
            Member("rlim_max", Field.SIMPLE))

    STRUCT_rusage = Struct("rusage",
            "struct rusage", ["linux/resource.h"])
    STRUCT_rusage.add_member(
            Member("ru_utime", Field.EMBED, ftype="struct timeval"))
    STRUCT_rusage.add_member(
            Member("ru_stime", Field.EMBED, ftype="struct timeval"))
    STRUCT_rusage.add_member(
            Member("ru_maxrss", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_ixrss", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_idrss", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_isrss", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_minflt", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_majflt", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_nswap", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_inblock", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_oublock", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_msgsnd", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_msgrcv", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_nsignals", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_nvcsw", Field.SIMPLE))
    STRUCT_rusage.add_member(
            Member("ru_nivcsw", Field.SIMPLE))

    STRUCT_timeval = Struct("timeval", 
            "struct timeval", ["linux/time.h"])
    STRUCT_timeval.add_member(
            Member("tv_sec", Field.SIMPLE))
    STRUCT_timeval.add_member(
            Member("tv_usec", Field.SIMPLE))

    STRUCT_timezone = Struct("timezone",
            "struct timezone", ["linux/time.h"])
    STRUCT_timezone.add_member(
            Member("tz_minuteswest", Field.SIMPLE))
    STRUCT_timezone.add_member(
            Member("tz_dsttime", Field.SIMPLE))

    STRUCT_timespec = Struct("timespec",
            "struct timespec", ["linux/time.h"])
    STRUCT_timespec.add_member(
            Member("tv_sec", Field.SIMPLE))
    STRUCT_timespec.add_member(
            Member("tv_nsec", Field.SIMPLE))
    
    STRUCT_sched_param = Struct("sched_param",
            "struct sched_param", ["linux/sched.h"])
    STRUCT_sched_param.add_member(
            Member("sched_priority", Field.SIMPLE))

    STRUCT_stat = Struct("stat",
            "struct stat", ["asm/stat.h"])
    STRUCT_stat.add_member(
            Member("st_dev", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_ino", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_nlink", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_mode", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_uid", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_gid", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_rdev", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_size", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_blksize", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_blocks", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_atime", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_atime_nsec", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_mtime", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_mtime_nsec", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_ctime", Field.SIMPLE))
    STRUCT_stat.add_member(
            Member("st_ctime_nsec", Field.SIMPLE))

    STRUCT_statfs = Struct("statfs",
            "struct statfs", ["asm/statfs.h"])
    STRUCT_statfs.add_member(
            Member("f_type", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_bsize", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_blocks", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_bfree", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_bavail", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_files", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_ffree", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_fsid", Field.EMBED, ftype="__kernel_fsid_t"))
    STRUCT_statfs.add_member(
            Member("f_namelen", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_frsize", Field.SIMPLE))
    STRUCT_statfs.add_member(
            Member("f_flags", Field.SIMPLE))

    STRUCT_iovec_read = Struct("iovec_read",
            "struct iovec", ["linux/uio.h"])
    STRUCT_iovec_read.add_member(
            Member("iov_base", Field.BUFFER, 
                fidx="iov_len", fdir=Flow.USER))
    STRUCT_iovec_read.add_member(
            Member("iov_len", Field.SIMPLE))

    STRUCT_iovec_write = Struct("iovec_write",
            "struct iovec", ["linux/uio.h"])
    STRUCT_iovec_write.add_member(
            Member("iov_base", Field.BUFFER, 
                fidx="iov_len", fdir=Flow.KERNEL))
    STRUCT_iovec_write.add_member(
            Member("iov_len", Field.SIMPLE))

    STRUCT_flock = Struct("flock",
            "struct flock", ["asm/fcntl.h"])
    STRUCT_flock.add_member(
            Member("l_type", Field.SIMPLE))
    STRUCT_flock.add_member(
            Member("l_whence", Field.SIMPLE))
    STRUCT_flock.add_member(
            Member("l_start", Field.SIMPLE))
    STRUCT_flock.add_member(
            Member("l_len", Field.SIMPLE))
    STRUCT_flock.add_member(
            Member("l_pid", Field.SIMPLE))

    STRUCT_termios = Struct("termios",
            "struct termios", ["asm/termbits.h"])
    STRUCT_termios.add_member(
            Member("c_iflag", Field.SIMPLE))
    STRUCT_termios.add_member(
            Member("c_oflag", Field.SIMPLE))
    STRUCT_termios.add_member(
            Member("c_cflag", Field.SIMPLE))
    STRUCT_termios.add_member(
            Member("c_lflag", Field.SIMPLE))
    STRUCT_termios.add_member(
            Member("c_line", Field.SIMPLE))
    STRUCT_termios.add_member(
            Member("c_cc", Field.ARRAY, fidx=19, ftype="cc_t"))

    STRUCT_termio = Struct("termio",
            "struct termio", ["asm/termios.h"])
    STRUCT_termio.add_member(
            Member("c_iflag", Field.SIMPLE))
    STRUCT_termio.add_member(
            Member("c_oflag", Field.SIMPLE))
    STRUCT_termio.add_member(
            Member("c_cflag", Field.SIMPLE))
    STRUCT_termio.add_member(
            Member("c_lflag", Field.SIMPLE))
    STRUCT_termio.add_member(
            Member("c_line", Field.SIMPLE))
    STRUCT_termio.add_member(
            Member("c_cc", Field.ARRAY, fidx=8, ftype="unsigned char"))

    STRUCT_winsize = Struct("winsize",
            "struct winsize", ["asm/termios.h"])
    STRUCT_winsize.add_member(
            Member("ws_row", Field.SIMPLE))
    STRUCT_winsize.add_member(
            Member("ws_col", Field.SIMPLE))
    STRUCT_winsize.add_member(
            Member("ws_xpixel", Field.SIMPLE))
    STRUCT_winsize.add_member(
            Member("ws_ypixel", Field.SIMPLE))

    STRUCT_pollfd = Struct("pollfd",
            "struct pollfd", ["asm/poll.h"])
    STRUCT_pollfd.add_member(
            Member("fd", Field.SIMPLE))
    STRUCT_pollfd.add_member(
            Member("events", Field.SIMPLE))
    STRUCT_pollfd.add_member(
            Member("revents", Field.SIMPLE))

    STRUCT_epoll_event = Struct("epoll_event",
            "struct epoll_event", ["linux/eventpoll.h"])
    STRUCT_epoll_event.add_member(
            Member("events", Field.SIMPLE))
    STRUCT_epoll_event.add_member(
            Member("data", Field.SIMPLE,
                get="", put="", compare="", clean=""))

    STRUCT_sockaddr = Struct("sockaddr",
            "struct sockaddr", ["linux/socket.h"])
    STRUCT_sockaddr.add_member(
            Member("sa_family", Field.SIMPLE))

    # sys group

    SYS_times = Syscall("times")
    SYS_times.add_struct(STRUCT_tms)
    SYS_times.add_param(
            Parameter(0, "struct tms __user *", "tbuf",
                Flow.USER, "struct tms", Element.STRUCT, 
                struct="tms"))

    SYS_sysinfo = Syscall("sysinfo")
    SYS_sysinfo.add_struct(STRUCT_sysinfo)
    SYS_sysinfo.add_param(
            Parameter(0, "struct sysinfo __user *", "info",
                Flow.USER, "struct sysinfo", Element.STRUCT,
                struct="sysinfo"))

    SYS_newuname = Syscall("newuname")
    SYS_newuname.add_struct(STRUCT_new_utsname)
    SYS_newuname.add_param(
            Parameter(0, "struct new_utsname __user *", "name",
                Flow.USER, "struct new_utsname", Element.STRUCT,
                struct="new_utsname"))

    SYS_umask = Syscall("umask")
    SYS_umask.add_param(
            Parameter(0, "mode_t", "mask",
                Flow.KERNEL, "mode_t", Element.VALUE))

    SYS_sethostname = Syscall("sethostname")
    SYS_sethostname.add_param(
            Parameter(0, "char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_sethostname.add_param(
            Parameter(1, "int", "len",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_setdomainname = Syscall("setdomainname")
    SYS_setdomainname.add_param(
            Parameter(0, "char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_setdomainname.add_param(
            Parameter(1, "int", "len", 
                Flow.KERNEL, "int", Element.VALUE))

    SYS_getrlimit = Syscall("getrlimit")
    SYS_getrlimit.add_struct(STRUCT_rlimit)
    SYS_getrlimit.add_param(
            Parameter(0, "unsigned int", "resource", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_getrlimit.add_param(
            Parameter(1, "struct rlimit __user *", "rlim",
                Flow.USER, "struct rlimit", Element.STRUCT,
                struct="rlimit"))

    SYS_setrlimit = Syscall("setrlimit")
    SYS_setrlimit.add_struct(STRUCT_rlimit)
    SYS_setrlimit.add_param(
            Parameter(0, "unsigned int", "resource",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_setrlimit.add_param(
            Parameter(1, "struct rlimit __user *", "rlim",
                Flow.KERNEL, "struct rlimit", Element.STRUCT,
                struct="rlimit"))

    SYS_getrusage = Syscall("getrusage")
    SYS_getrusage.add_struct(STRUCT_rusage)
    SYS_getrusage.add_param(
            Parameter(0, "int", "who",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_getrusage.add_param(
            Parameter(1, "struct rusage __user *", "ru",
                Flow.USER, "struct rusage", Element.STRUCT,
                struct="rusage"))

    SYS_getpriority = Syscall("getpriority")
    SYS_getpriority.add_param(
            Parameter(0, "int", "which", 
                Flow.KERNEL, "int", Element.VALUE))
    SYS_getpriority.add_param(
            Parameter(1, "int", "who",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_setpriority = Syscall("setpriority")
    SYS_setpriority.add_param(
            Parameter(0, "int", "which",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_setpriority.add_param(
            Parameter(1, "int", "who",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_setpriority.add_param(
            Parameter(2, "int", "niceval",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_getpid = Syscall("getpid")

    SYS_gettid = Syscall("gettid")

    SYS_getppid = Syscall("getppid")

    SYS_getpgrp = Syscall("getpgrp")

    SYS_setpgid = Syscall("setpgid")
    SYS_setpgid.add_param(
            Parameter(0, "pid_t", "pid",
                Flow.KERNEL, "pid_t", Element.VALUE))
    SYS_setpgid.add_param(
            Parameter(1, "pid_t", "pgid",
                Flow.KERNEL, "pid_t", Element.VALUE))

    SYS_getsid = Syscall("getsid")
    SYS_getsid.add_param(
            Parameter(0, "pid_t", "pid", 
                Flow.KERNEL, "pid_t", Element.VALUE))

    SYS_setsid = Syscall("setsid")
    
    SYS_getuid = Syscall("getuid")
    
    SYS_setuid = Syscall("setuid")
    SYS_setuid.add_param(
            Parameter(0, "uid_t", "uid",
                Flow.KERNEL, "uid_t", Element.VALUE))

    SYS_setreuid = Syscall("setreuid")
    SYS_setreuid.add_param(
            Parameter(0, "uid_t", "ruid",
                Flow.KERNEL, "uid_t", Element.VALUE))
    SYS_setreuid.add_param(
            Parameter(1, "uid_t", "euid",
                Flow.KERNEL, "uid_t", Element.VALUE))

    SYS_geteuid = Syscall("geteuid")

    SYS_getresuid = Syscall("getresuid")
    SYS_getresuid.add_param(
            Parameter(0, "uid_t __user *", "ruidp", 
                Flow.USER, "uid_t", Element.SIMPLE))
    SYS_getresuid.add_param(
            Parameter(1, "uid_t __user *", "euidp",
                Flow.USER, "uid_t", Element.SIMPLE))
    SYS_getresuid.add_param(
            Parameter(2, "uid_t __user *", "suidp",
                Flow.USER, "uid_t", Element.SIMPLE))

    SYS_setresuid = Syscall("setresuid")
    SYS_setresuid.add_param(
            Parameter(0, "uid_t", "ruid",
                Flow.KERNEL, "uid_t", Element.VALUE))
    SYS_setresuid.add_param(
            Parameter(1, "uid_t", "euid", 
                Flow.KERNEL, "uid_t", Element.VALUE))
    SYS_setresuid.add_param(
            Parameter(2, "uid_t", "suid",
                Flow.KERNEL, "uid_t", Element.VALUE))

    SYS_setfsuid = Syscall("setfsuid")
    SYS_setfsuid.add_param(
            Parameter(0, "uid_t", "uid",
                Flow.KERNEL, "uid_t", Element.VALUE))
 
    SYS_getgid = Syscall("getgid")

    SYS_setgid = Syscall("setgid")
    SYS_setgid.add_param(
            Parameter(0, "gid_t", "gid",
                Flow.KERNEL, "gid_t", Element.VALUE))

    SYS_getegid = Syscall("getegid")

    SYS_setregid = Syscall("setregid")
    SYS_setregid.add_param(
            Parameter(0, "gid_t", "rgid",
                Flow.KERNEL, "gid_t", Element.VALUE))
    SYS_setregid.add_param(
            Parameter(1, "gid_t", "egid",
                Flow.KERNEL, "gid_t", Element.VALUE))

    SYS_getresgid = Syscall("getresgid")
    SYS_getresgid.add_param(
            Parameter(0, "gid_t __user *", "rgidp",
                Flow.USER, "gid_t", Element.SIMPLE))
    SYS_getresgid.add_param(
            Parameter(1, "gid_t __user *", "egidp",
                Flow.USER, "gid_t", Element.SIMPLE))
    SYS_getresgid.add_param(
            Parameter(2, "gid_t __user *", "gidp",
                Flow.USER, "gid_t", Element.SIMPLE))

    SYS_setresgid = Syscall("setresgid")
    SYS_setresgid.add_param(
            Parameter(0, "gid_t", "rgid",
                Flow.KERNEL, "gid_t", Element.VALUE))
    SYS_setresgid.add_param(
            Parameter(1, "gid_t", "ugid",
                Flow.KERNEL, "gid_t", Element.VALUE))
    SYS_setresgid.add_param(
            Parameter(2, "gid_t", "sgid",
                Flow.KERNEL, "gid_t", Element.VALUE))

    SYS_setfsgid = Syscall("setfsgid")
    SYS_setfsgid.add_param(
            Parameter(0, "gid_t", "gid",
                Flow.KERNEL, "gid_t", Element.VALUE))

    SYS_getgroups = Syscall("getgroups")
    SYS_getgroups.add_param(
            Parameter(0, "int", "gidsetsize",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_getgroups.add_param(
            Parameter(1, "gid_t __user *", "grouplist",
                Flow.USER, "gid_t", Element.VALUE_VAR, eidx=0))

    SYS_setgroups = Syscall("setgroups")
    SYS_setgroups.add_param(
            Parameter(0, "int", "gidsetsize",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_setgroups.add_param(
            Parameter(1, "gid_t __user *", "grouplist",
                Flow.KERNEL, "gid_t", Element.VALUE_VAR, eidx=0))

    SYS_getcwd = Syscall("getcwd")
    SYS_getcwd.add_param(
            Parameter(0, "char __user *", "buf",
                Flow.USER, "char", Element.BUFFER, eidx=1))
    SYS_getcwd.add_param(
            Parameter(1, "unsigned long", "size",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_gettimeofday = Syscall("gettimeofday")
    SYS_gettimeofday.add_struct(STRUCT_timeval)
    SYS_gettimeofday.add_struct(STRUCT_timezone)
    SYS_gettimeofday.add_param(
            Parameter(0, "struct timeval __user *", "tv",
                Flow.USER, "struct timeval", Element.STRUCT,
                struct="timeval"))
    SYS_gettimeofday.add_param(
            Parameter(1, "struct timezone __user *", "tz",
                Flow.USER, "struct timezone", Element.STRUCT,
                struct="timezone"))

    SYS_time = Syscall("time")
    SYS_time.add_param(
            Parameter(0, "time_t __user *", "t",
                Flow.USER, "time_t", Element.SIMPLE))

    SYS_clock_gettime = Syscall("clock_gettime")
    SYS_clock_gettime.add_struct(STRUCT_timespec)
    SYS_clock_gettime.add_param(
            Parameter(0, "clockid_t", "which_clock", 
                Flow.KERNEL, "clockid_t", Element.VALUE))
    SYS_clock_gettime.add_param(
            Parameter(1, "struct timespec __user *", "tp",
                Flow.USER, "struct timespec", Element.STRUCT,
                struct="timespec"))

    SYS_clock_getres = Syscall("clock_getres")
    SYS_clock_getres.add_struct(STRUCT_timespec)
    SYS_clock_getres.add_param(
            Parameter(0, "clockid_t", "which_clock", 
                Flow.KERNEL, "clockid_t", Element.VALUE))
    SYS_clock_getres.add_param(
            Parameter(1, "struct timespec __user *", "tp",
                Flow.USER, "struct timespec", Element.STRUCT,
                struct="timespec"))

    SYS_sched_getparam = Syscall("sched_getparam")
    SYS_sched_getparam.add_struct(STRUCT_sched_param)
    SYS_sched_getparam.add_param(
            Parameter(0, "pid_t",  "pid",
                Flow.KERNEL, "pid_t", Element.VALUE))
    SYS_sched_getparam.add_param(
            Parameter(1, "struct sched_param __user *", "param",
                Flow.USER, "struct sched_param", Element.STRUCT,
                struct="sched_param"))

    SYS_sched_getscheduler = Syscall("sched_getscheduler")
    SYS_sched_getscheduler.add_param(
            Parameter(0, "pid_t", "pid",
                Flow.KERNEL, "pid_t", Element.VALUE))

    SYS_sched_get_priority_min = Syscall("sched_get_priority_min")
    SYS_sched_get_priority_min.add_param(
            Parameter(0, "int", "policy",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_sched_get_priority_max = Syscall("sched_get_priority_max")
    SYS_sched_get_priority_max.add_param(
            Parameter(0, "int", "policy",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_getcpu = Syscall("getcpu")
    SYS_getcpu.add_param(
            Parameter(0, "unsigned int __user *", "cpu",
                Flow.USER, "unsigned int", Element.SIMPLE))
    SYS_getcpu.add_param(
            Parameter(1, "unsigned int __user *", "node",
                Flow.USER, "unsigned int", Element.SIMPLE))
    SYS_getcpu.add_param(
            Parameter(2, "void __user *", "cache",
                Flow.USER, "void", Element.BUFFER,
                turnin="", fetch="", rclean=""))

    # fs group

    SYS_access = Syscall("access")
    SYS_access.add_param(
            Parameter(0, "const char __user *", "filename", 
                Flow.KERNEL, "char", Element.STRING))
    SYS_access.add_param(
            Parameter(1, "int", "mode",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_faccessat = Syscall("faccessat")
    SYS_faccessat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_faccessat.add_param(
            Parameter(1, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_faccessat.add_param(
            Parameter(2, "int", "mode",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_readlink = Syscall("readlink")
    SYS_readlink.add_param(
            Parameter(0, "const char __user *", "path", 
                Flow.KERNEL, "char", Element.STRING))
    SYS_readlink.add_param(
            Parameter(1, "char __user *", "buf", 
                Flow.USER, "char", Element.STRING))
    SYS_readlink.add_param(
            Parameter(2, "int", "bufsiz",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_readlinkat = Syscall("readlinkat")
    SYS_readlinkat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_readlinkat.add_param(
            Parameter(1, "const char __user *", "path", 
                Flow.KERNEL, "char", Element.STRING))
    SYS_readlinkat.add_param(
            Parameter(2, "char __user *", "buf", 
                Flow.USER, "char", Element.STRING))
    SYS_readlinkat.add_param(
            Parameter(3, "int", "bufsiz",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_stat = Syscall("stat")
    SYS_stat.add_struct(STRUCT_stat)
    SYS_stat.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_stat.add_param(
            Parameter(1, "struct stat __user *", "statbuf",
                Flow.USER, "struct stat", Element.STRUCT,
                struct="stat"))

    SYS_fstat = Syscall("fstat")
    SYS_fstat.add_struct(STRUCT_stat)
    SYS_fstat.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fstat.add_param(
            Parameter(1, "struct stat __user *", "statbuf",
                Flow.USER, "struct stat", Element.STRUCT,
                struct="stat"))

    SYS_lstat = Syscall("lstat")
    SYS_lstat.add_struct(STRUCT_stat)
    SYS_lstat.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_lstat.add_param(
            Parameter(1, "struct stat __user *", "statbuf",
                Flow.USER, "struct stat", Element.STRUCT,
                struct="stat"))

    SYS_newfstatat = Syscall("newfstatat")
    SYS_newfstatat.add_struct(STRUCT_stat)
    SYS_newfstatat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_newfstatat.add_param(
            Parameter(1, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_newfstatat.add_param(
            Parameter(2, "struct stat __user *", "statbuf",
                Flow.USER, "struct stat", Element.STRUCT,
                struct="stat"))
    SYS_newfstatat.add_param(
            Parameter(3, "int", "flag",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_truncate = Syscall("truncate")
    SYS_truncate.add_param(
            Parameter(0, "const  char __user *", "path",
                Flow.KERNEL, "char", Element.STRING))
    SYS_truncate.add_param(
            Parameter(1, "long", "length",
                Flow.KERNEL, "long", Element.VALUE))

    SYS_ftruncate = Syscall("ftruncate")
    SYS_ftruncate.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ftruncate.add_param(
            Parameter(1, "unsigned long", "length",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_link = Syscall("link")
    SYS_link.add_param(
            Parameter(0, "const char __user *", "oldname", 
                Flow.KERNEL, "char", Element.STRING))
    SYS_link.add_param(
            Parameter(1, "const char __user *", "newname", 
                Flow.KERNEL, "char", Element.STRING))

    SYS_linkat = Syscall("linkat")
    SYS_linkat.add_param(
            Parameter(0, "int", "olddfd", 
                Flow.KERNEL, "int", Element.VALUE))
    SYS_linkat.add_param(
            Parameter(1, "const char __user *", "oldname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_linkat.add_param(
            Parameter(2, "int", "newdfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_linkat.add_param(
            Parameter(3, "const char __user *", "newname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_linkat.add_param(
            Parameter(4, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_symlink = Syscall("symlink")
    SYS_symlink.add_param(
            Parameter(0, "const char __user *", "oldname", 
                Flow.KERNEL, "char", Element.STRING))
    SYS_symlink.add_param(
            Parameter(1, "const char __user *", "newname", 
                Flow.KERNEL, "char", Element.STRING))

    SYS_symlinkat = Syscall("symlinkat")
    SYS_symlinkat.add_param(
            Parameter(0, "const char __user *", "oldname", 
                Flow.KERNEL, "char", Element.STRING))
    SYS_symlinkat.add_param(
            Parameter(1, "int", "newdfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_symlinkat.add_param(
            Parameter(2, "const char __user *", "newname", 
                Flow.KERNEL, "char", Element.STRING))

    SYS_unlink = Syscall("unlink")
    SYS_unlink.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))

    SYS_unlinkat = Syscall("unlinkat")
    SYS_unlinkat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_unlinkat.add_param(
            Parameter(1, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_unlinkat.add_param(
            Parameter(2, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_rename = Syscall("rename")
    SYS_rename.add_param(
            Parameter(0, "const char __user *", "oldname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_rename.add_param(
            Parameter(1, "const char __user *", "newname",
                Flow.KERNEL, "char", Element.STRING))

    SYS_renameat = Syscall("renameat")
    SYS_renameat.add_param(
            Parameter(0, "int", "olddfd", 
                Flow.KERNEL, "int", Element.VALUE))
    SYS_renameat.add_param(
            Parameter(1, "const char __user *", "oldname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_renameat.add_param(
            Parameter(2, "int", "newdfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_renameat.add_param(
            Parameter(3, "const char __user *", "newname",
                Flow.KERNEL, "char", Element.STRING))

    SYS_mkdir = Syscall("mkdir")
    SYS_mkdir.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_mkdir.add_param(
            Parameter(1, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_mkdirat = Syscall("mkdirat")
    SYS_mkdirat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_mkdirat.add_param(
            Parameter(1, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_mkdirat.add_param(
            Parameter(2, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_rmdir = Syscall("rmdir")
    SYS_rmdir.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))

    SYS_chdir = Syscall("chdir")
    SYS_chdir.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))

    SYS_fchdir = Syscall("fchdir")
    SYS_fchdir.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_mknod = Syscall("mknod")
    SYS_mknod.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_mknod.add_param(
            Parameter(1, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))
    SYS_mknod.add_param(
            Parameter(2, "unsigned int", "dev",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_mknodat = Syscall("mknodat")
    SYS_mknodat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_mknodat.add_param(
            Parameter(1, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_mknodat.add_param(
            Parameter(2, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))
    SYS_mknodat.add_param(
            Parameter(3, "unsigned int", "dev",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_chmod = Syscall("chmod")
    SYS_chmod.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_chmod.add_param(
            Parameter(1, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_fchmod = Syscall("fchmod")
    SYS_fchmod.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "char", Element.VALUE))
    SYS_fchmod.add_param(
            Parameter(1, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_fchmodat = Syscall("fchmodat")
    SYS_fchmodat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "char", Element.VALUE))
    SYS_fchmodat.add_param(
            Parameter(1, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_fchmodat.add_param(
            Parameter(2, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_chown = Syscall("chown")
    SYS_chown.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_chown.add_param(
            Parameter(1, "uid_t", "user",
                Flow.KERNEL, "uid_t", Element.VALUE))
    SYS_chown.add_param(
            Parameter(2, "gid_t", "group",
                Flow.KERNEL, "gid_t", Element.VALUE))

    SYS_fchown = Syscall("fchown")
    SYS_fchown.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "char", Element.VALUE))
    SYS_fchown.add_param(
            Parameter(1, "uid_t", "user",
                Flow.KERNEL, "uid_t", Element.VALUE))
    SYS_fchown.add_param(
            Parameter(2, "gid_t", "group",
                Flow.KERNEL, "gid_t", Element.VALUE))

    SYS_lchown = Syscall("lchown")
    SYS_lchown.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_lchown.add_param(
            Parameter(1, "uid_t", "user",
                Flow.KERNEL, "uid_t", Element.VALUE))
    SYS_lchown.add_param(
            Parameter(2, "gid_t", "group",
                Flow.KERNEL, "gid_t", Element.VALUE))

    SYS_fchownat = Syscall("fchownat")
    SYS_fchownat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_fchownat.add_param(
            Parameter(1, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_fchownat.add_param(
            Parameter(2, "uid_t", "user",
                Flow.KERNEL, "uid_t", Element.VALUE))
    SYS_fchownat.add_param(
            Parameter(3, "gid_t", "group",
                Flow.KERNEL, "gid_t", Element.VALUE))
    SYS_fchownat.add_param(
            Parameter(4, "int", "flag",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_setxattr = Syscall("setxattr")
    SYS_setxattr.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_setxattr.add_param(
            Parameter(1, "const char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_setxattr.add_param(
            Parameter(2, "const void __user *", "value",
                Flow.KERNEL, "void", Element.BUFFER, eidx=3))
    SYS_setxattr.add_param(
            Parameter(3, "size_t", "size",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_setxattr.add_param(
            Parameter(4, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_fsetxattr = Syscall("fsetxattr")
    SYS_fsetxattr.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_fsetxattr.add_param(
            Parameter(1, "const char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_fsetxattr.add_param(
            Parameter(2, "const void __user *", "value",
                Flow.KERNEL, "void", Element.BUFFER, eidx=3))
    SYS_fsetxattr.add_param(
            Parameter(3, "size_t", "size",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_fsetxattr.add_param(
            Parameter(4, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_lsetxattr = Syscall("lsetxattr")
    SYS_lsetxattr.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_lsetxattr.add_param(
            Parameter(1, "const char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_lsetxattr.add_param(
            Parameter(2, "const void __user *", "value",
                Flow.KERNEL, "void", Element.BUFFER, eidx=3))
    SYS_lsetxattr.add_param(
            Parameter(3, "size_t", "size",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_lsetxattr.add_param(
            Parameter(4, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_getxattr = Syscall("getxattr")
    SYS_getxattr.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_getxattr.add_param(
            Parameter(1, "const char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_getxattr.add_param(
            Parameter(2, "void __user *", "value",
                Flow.USER, "void", Element.BUFFER, eidx=3))
    SYS_getxattr.add_param(
            Parameter(3, "size_t", "size",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_fgetxattr = Syscall("fgetxattr")
    SYS_fgetxattr.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_fgetxattr.add_param(
            Parameter(1, "const char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_fgetxattr.add_param(
            Parameter(2, "void __user *", "value",
                Flow.USER, "void", Element.BUFFER, eidx=3))
    SYS_fgetxattr.add_param(
            Parameter(3, "size_t", "size",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_lgetxattr = Syscall("lgetxattr")
    SYS_lgetxattr.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_lgetxattr.add_param(
            Parameter(1, "const char __user *", "name",
                Flow.KERNEL, "char", Element.STRING))
    SYS_lgetxattr.add_param(
            Parameter(2, "void __user *", "value",
                Flow.USER, "void", Element.BUFFER, eidx=3))
    SYS_lgetxattr.add_param(
            Parameter(3, "size_t", "size",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_removexattr = Syscall("removexattr")
    SYS_removexattr.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_removexattr.add_param(
            Parameter(1, "const char __user *", "name", 
                Flow.KERNEL, "char", Element.STRING))

    SYS_fremovexattr = Syscall("fremovexattr")
    SYS_fremovexattr.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_fremovexattr.add_param(
            Parameter(1, "const char __user *", "name", 
                Flow.KERNEL, "char", Element.STRING))

    SYS_lremovexattr = Syscall("lremovexattr")
    SYS_lremovexattr.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_lremovexattr.add_param(
            Parameter(1, "const char __user *", "name", 
                Flow.KERNEL, "char", Element.STRING))

    SYS_statfs = Syscall("statfs")
    SYS_statfs.add_struct(STRUCT_statfs)
    SYS_statfs.add_param(
            Parameter(0, "const char __user *", "pathname", 
                Flow.KERNEL, "char", Element.STRING))
    SYS_statfs.add_param(
            Parameter(1, "struct statfs __user *", "buf",
                Flow.USER, "struct statfs", Element.STRUCT, 
                struct="statfs"))

    SYS_fstatfs = Syscall("fstatfs")
    SYS_fstatfs.add_struct(STRUCT_statfs)
    SYS_fstatfs.add_param(
            Parameter(0, "int", "fd", 
                Flow.KERNEL, "int", Element.VALUE))
    SYS_fstatfs.add_param(
            Parameter(1, "struct statfs __user *", "buf",
                Flow.USER, "struct statfs", Element.STRUCT, 
                struct="statfs"))

    SYS_getdents = Syscall("getdents")
    SYS_getdents.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_getdents.add_param(
            Parameter(1, "void *", "dirp",
                Flow.USER, "void", Element.BUFFER, eidx=2))
    SYS_getdents.add_param(
            Parameter(2, "unsigned int", "count",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    # io

    SYS_open_1 = Syscall("open", cond="flags & O_CREAT")
    SYS_open_1.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_open_1.add_param(
            Parameter(1, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_open_1.add_param(
            Parameter(2, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_open_2 = Syscall("open", cond="!(flags & O_CREAT)")
    SYS_open_2.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_open_2.add_param(
            Parameter(1, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
 
    SYS_open = Syscall("open")
    SYS_open.add_sibling(SYS_open_1)
    SYS_open.add_sibling(SYS_open_2)
    SYS_open.add_param(
            Parameter(0, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_open.add_param(
            Parameter(1, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_open.add_param(
            Parameter(2, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_openat_1 = Syscall("openat", cond="flags & O_CREAT")
    SYS_openat_1.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_openat_1.add_param(
            Parameter(1, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_openat_1.add_param(
            Parameter(2, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_openat_1.add_param(
            Parameter(3, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_openat_2 = Syscall("openat", cond="!(flags & O_CREAT)")
    SYS_openat_2.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_openat_2.add_param(
            Parameter(1, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_openat_2.add_param(
            Parameter(2, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
 
    SYS_openat = Syscall("openat")
    SYS_openat.add_sibling(SYS_openat_1)
    SYS_openat.add_sibling(SYS_openat_2)
    SYS_openat.add_param(
            Parameter(0, "int", "dfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_openat.add_param(
            Parameter(1, "const char __user *", "filename",
                Flow.KERNEL, "char", Element.STRING))
    SYS_openat.add_param(
            Parameter(2, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_openat.add_param(
            Parameter(3, "umode_t", "mode",
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_creat = Syscall("creat")
    SYS_creat.add_param(
            Parameter(0, "const char __user *", "pathname",
                Flow.KERNEL, "char", Element.STRING))
    SYS_creat.add_param(
            Parameter(1, "umode_t", "mode", 
                Flow.KERNEL, "umode_t", Element.VALUE))

    SYS_close = Syscall("close")
    SYS_close.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_lseek = Syscall("lseek")
    SYS_lseek.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_lseek.add_param(
            Parameter(1, "off_t", "offset",
                Flow.KERNEL, "off_t", Element.VALUE))
    SYS_lseek.add_param(
            Parameter(2, "unsigned int", "whence",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_read = Syscall("read")
    SYS_read.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_read.add_param(
            Parameter(1, "char __user *", "buf",
                Flow.USER, "char", Element.BUFFER, eidx=2))
    SYS_read.add_param(
            Parameter(2, "size_t", "count",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_write = Syscall("write")
    SYS_write.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_write.add_param(
            Parameter(1, "const char __user *", "buf",
                Flow.KERNEL, "char", Element.BUFFER, eidx=2))
    SYS_write.add_param(
            Parameter(2, "size_t", "count",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_pread64 = Syscall("pread64")
    SYS_pread64.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_pread64.add_param(
            Parameter(1, "char __user *", "buf",
                Flow.USER, "char", Element.BUFFER, eidx=2))
    SYS_pread64.add_param(
            Parameter(2, "size_t", "count",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_pread64.add_param(
            Parameter(3, "loff_t", "pos",
                Flow.KERNEL, "loff_t", Element.VALUE))

    SYS_pwrite64 = Syscall("pwrite64")
    SYS_pwrite64.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_pwrite64.add_param(
            Parameter(1, "const char __user *", "buf",
                Flow.KERNEL, "char", Element.BUFFER, eidx=2))
    SYS_pwrite64.add_param(
            Parameter(2, "size_t", "count",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_pwrite64.add_param(
            Parameter(3, "loff_t", "pos",
                Flow.KERNEL, "loff_t", Element.VALUE))

    SYS_readv = Syscall("readv")
    SYS_readv.add_struct(STRUCT_iovec_read)
    SYS_readv.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_readv.add_param(
            Parameter(1, "struct iovec __user *", "vec",
                Flow.USER, "struct iovec", Element.STRUCT_VAR, eidx=2,
                struct="iovec_read"))
    SYS_readv.add_param(
            Parameter(2, "unsigned long", "vlen",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_writev = Syscall("writev")
    SYS_writev.add_struct(STRUCT_iovec_write)
    SYS_writev.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_writev.add_param(
            Parameter(1, "struct iovec __user *", "vec",
                Flow.KERNEL, "struct iovec", Element.STRUCT_VAR, eidx=2,
                struct="iovec_write"))
    SYS_writev.add_param(
            Parameter(2, "unsigned long", "vlen",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_pipe = Syscall("pipe")
    SYS_pipe.add_param(
            Parameter(0, "int __user *", "fildes",
                Flow.USER, "int", Element.VALUE_FIX, eidx=2))

    SYS_pipe2 = Syscall("pipe2")
    SYS_pipe2.add_param(
            Parameter(0, "int __user *", "fildes",
                Flow.USER, "int", Element.VALUE_FIX, eidx=2))
    SYS_pipe2.add_param(
            Parameter(1, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_eventfd = Syscall("eventfd")
    SYS_eventfd.add_param(
            Parameter(0, "unsigned int", "count",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_eventfd2 = Syscall("eventfd2")
    SYS_eventfd2.add_param(
            Parameter(0, "unsigned int", "count",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_eventfd2.add_param(
            Parameter(1, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
    
    SYS_epoll_create = Syscall("epoll_create")
    SYS_epoll_create.add_param(
            Parameter(0, "int", "size",
                Flow.KERNEL, "int", Element.VALUE))
    
    SYS_epoll_create1 = Syscall("epoll_create1")
    SYS_epoll_create1.add_param(
            Parameter(0, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_epoll_ctl = Syscall("epoll_ctl")
    SYS_epoll_ctl.add_struct(STRUCT_epoll_event)
    SYS_epoll_ctl.add_param(
            Parameter(0, "int", "epfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_epoll_ctl.add_param(
            Parameter(1, "int", "op",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_epoll_ctl.add_param(
            Parameter(2, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_epoll_ctl.add_param(
            Parameter(3, "struct epoll_event __user *", "event",
                Flow.KERNEL, "struct epoll_event", Element.STRUCT,
                struct="epoll_event"))

    SYS_dup = Syscall("dup")
    SYS_dup.add_param(
            Parameter(0, "unsigned int", "fildes",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_dup2 = Syscall("dup2")
    SYS_dup2.add_param(
            Parameter(0, "unsigned int", "oldfd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_dup2.add_param(
            Parameter(1, "unsigned int", "newfd",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_dup3 = Syscall("dup3")
    SYS_dup3.add_param(
            Parameter(0, "unsigned int", "oldfd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_dup3.add_param(
            Parameter(1, "unsigned int", "newfd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_dup3.add_param(
            Parameter(2, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_sendfile = Syscall("sendfile")
    SYS_sendfile.add_param(
            Parameter(0, "int", "out_fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_sendfile.add_param(
            Parameter(1, "int", "in_fd", 
                Flow.KERNEL, "int", Element.VALUE))
    SYS_sendfile.add_param(
            Parameter(2, "off_t __user *", "offset", 
                Flow.BOTH, "off_t", Element.SIMPLE))
    SYS_sendfile.add_param(
            Parameter(3, "size_t", "count",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_sendfile64 = Syscall("sendfile64")
    SYS_sendfile64.add_param(
            Parameter(0, "int", "out_fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_sendfile64.add_param(
            Parameter(1, "int", "in_fd", 
                Flow.KERNEL, "int", Element.VALUE))
    SYS_sendfile64.add_param(
            Parameter(2, "loff_t __user *", "offset", 
                Flow.BOTH, "loff_t", Element.SIMPLE))
    SYS_sendfile64.add_param(
            Parameter(3, "size_t", "count",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_poll = Syscall("poll")
    SYS_poll.add_struct(STRUCT_pollfd)
    SYS_poll.add_param(
            Parameter(0, "struct pollfd __user *", "fds",
                Flow.BOTH, "struct pollfd", Element.STRUCT_VAR, eidx=1,
                struct="pollfd"))
    SYS_poll.add_param(
            Parameter(1, "unsigned int", "nfds",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_poll.add_param(
            Parameter(2, "int", "timeout",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_ppoll = Syscall("ppoll")
    SYS_ppoll.add_struct(STRUCT_pollfd)
    SYS_ppoll.add_struct(STRUCT_timespec)
    SYS_ppoll.add_param(
            Parameter(0, "struct pollfd __user *", "fds",
                Flow.BOTH, "struct pollfd", Element.STRUCT_VAR, eidx=1,
                struct="pollfd"))
    SYS_ppoll.add_param(
            Parameter(1, "unsigned int", "nfds",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ppoll.add_param(
            Parameter(2, "struct timespec __user *", "timeout",
                Flow.KERNEL, "struct timespec", Element.STRUCT, 
                struct="timespec"))
    SYS_ppoll.add_param(
            Parameter(3, "void __user *", "sigmask",
                Flow.KERNEL, "void", Element.BUFFER, eidx=4))
    SYS_ppoll.add_param(
            Parameter(4, "size_t", "sigsetsize",
                Flow.KERNEL, "size_t", Element.VALUE))

    SYS_select = Syscall("select")
    SYS_select.add_struct(STRUCT_timeval)
    SYS_select.add_param(
            Parameter(0, "int", "nfds",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_select.add_param(
            Parameter(1, "fd_set __user *", "readfds",
                Flow.BOTH, "fd_set", Element.TYPE))
    SYS_select.add_param(
            Parameter(2, "fd_set __user *", "writefds",
                Flow.BOTH, "fd_set", Element.TYPE))
    SYS_select.add_param(
            Parameter(3, "fd_set __user *", "exceptfds",
                Flow.BOTH, "fd_set", Element.TYPE))
    SYS_select.add_param(
            Parameter(4, "struct timeval __user *", "timeout",
                Flow.BOTH, "struct timeval", Element.STRUCT, 
                struct="timeval"))

    SYS_pselect6 = Syscall("pselect6")
    SYS_pselect6.add_struct(STRUCT_timespec)
    SYS_pselect6.add_param(
            Parameter(0, "int", "nfds",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_pselect6.add_param(
            Parameter(1, "fd_set __user *", "readfds",
                Flow.BOTH, "fd_set", Element.TYPE))
    SYS_pselect6.add_param(
            Parameter(2, "fd_set __user *", "writefds",
                Flow.BOTH, "fd_set", Element.TYPE))
    SYS_pselect6.add_param(
            Parameter(3, "fd_set __user *", "exceptfds",
                Flow.BOTH, "fd_set", Element.TYPE))
    SYS_pselect6.add_param(
            Parameter(4, "struct timespec __user *", "timeout",
                Flow.KERNEL, "struct timespec", Element.STRUCT, 
                struct="timespec"))
    SYS_pselect6.add_param(
            Parameter(5, "sigset_t __user *", "sigmask",
                Flow.KERNEL, "sigset_t", Element.TYPE))


    SYS_fcntl_1 = Syscall("fcntl", "cmd == F_DUPFD")
    SYS_fcntl_1.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_1.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_1.add_param(
            Parameter(2, "unsigned long", "arg",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_fcntl_2 = Syscall("fcntl", "cmd == F_SETFD")
    SYS_fcntl_2.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_2.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_2.add_param(
            Parameter(2, "unsigned long", "arg",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_fcntl_3 = Syscall("fcntl", "cmd == F_GETFD")
    SYS_fcntl_3.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_3.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_fcntl_4 = Syscall("fcntl", "cmd == F_SETFL")
    SYS_fcntl_4.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_4.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_4.add_param(
            Parameter(2, "unsigned long", "arg",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_fcntl_5 = Syscall("fcntl", "cmd == F_GETFL")
    SYS_fcntl_5.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_5.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_fcntl_6 = Syscall("fcntl", "cmd == F_GETLK")
    SYS_fcntl_6.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_6.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_6.add_param(
            Parameter(2, "struct flock __user *", "arg",
                Flow.USER, "struct flock", Element.STRUCT,
                struct="flock"))

    SYS_fcntl_7 = Syscall("fcntl", "cmd == F_SETLK")
    SYS_fcntl_7.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_7.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_7.add_param(
            Parameter(2, "struct flock __user *", "arg",
                Flow.KERNEL, "struct flock", Element.STRUCT,
                struct="flock"))

    SYS_fcntl_8 = Syscall("fcntl", "cmd == F_SETOWN")
    SYS_fcntl_8.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_8.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_8.add_param(
            Parameter(2, "unsigned long", "arg",
                Flow.KERNEL, "unsigned long", Element.VALUE))

    SYS_fcntl_9 = Syscall("fcntl", "cmd == F_GETOWN")
    SYS_fcntl_9.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl_9.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    SYS_fcntl = Syscall("fcntl")
    SYS_fcntl.add_struct(STRUCT_flock)
    SYS_fcntl.add_sibling(SYS_fcntl_1)
    SYS_fcntl.add_sibling(SYS_fcntl_2)
    SYS_fcntl.add_sibling(SYS_fcntl_3)
    SYS_fcntl.add_sibling(SYS_fcntl_4)
    SYS_fcntl.add_sibling(SYS_fcntl_5)
    SYS_fcntl.add_sibling(SYS_fcntl_6)
    SYS_fcntl.add_sibling(SYS_fcntl_7)
    SYS_fcntl.add_sibling(SYS_fcntl_8)
    SYS_fcntl.add_sibling(SYS_fcntl_9)
    SYS_fcntl.add_param(
            Parameter(0, "unsigned int", "fd", 
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_fcntl.add_param(
            Parameter(2, "void *", "arg",
                Flow.KERNEL, "void", Element.VALUE))

    SYS_ioctl_1 = Syscall("ioctl", "cmd == TCGETS")
    SYS_ioctl_1.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_1.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_1.add_param(
            Parameter(2, "struct termios __user *", "arg",
                Flow.USER, "struct termios", Element.STRUCT,
                struct="termios"))

    SYS_ioctl_2 = Syscall("ioctl", "cmd == TCSETS")
    SYS_ioctl_2.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_2.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_2.add_param(
            Parameter(2, "struct termios __user *", "arg",
                Flow.KERNEL, "struct termios", Element.STRUCT,
                struct="termios"))

    SYS_ioctl_3 = Syscall("ioctl", "cmd == TCGETA")
    SYS_ioctl_3.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_3.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_3.add_param(
            Parameter(2, "struct termio __user *", "arg",
                Flow.USER, "struct termio", Element.STRUCT,
                struct="termio"))

    SYS_ioctl_4 = Syscall("ioctl", "cmd == TCSETA")
    SYS_ioctl_4.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_4.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_4.add_param(
            Parameter(2, "struct termios __user *", "arg",
                Flow.KERNEL, "struct termio", Element.STRUCT,
                struct="termio"))

    SYS_ioctl_5 = Syscall("ioctl", "cmd == TIOCGWINSZ")
    SYS_ioctl_5.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_5.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_5.add_param(
            Parameter(2, "struct winsize __user *", "arg",
                Flow.USER, "struct winsize", Element.STRUCT,
                struct="winsize"))

    SYS_ioctl_6 = Syscall("ioctl", "cmd == TCSETS")
    SYS_ioctl_6.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_6.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_6.add_param(
            Parameter(2, "struct winsize __user *", "arg",
                Flow.KERNEL, "struct winsize", Element.STRUCT,
                struct="winsize"))

    SYS_ioctl_7 = Syscall("ioctl", "cmd == FIONREAD")
    SYS_ioctl_7.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_7.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_7.add_param(
            Parameter(2, "int __user *", "arg",
                Flow.USER, "int", Element.TYPE))

    SYS_ioctl_8 = Syscall("ioctl", "cmd == FIONBIO")
    SYS_ioctl_8.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_8.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_8.add_param(
            Parameter(2, "int __user *", "arg",
                Flow.KERNEL, "int", Element.TYPE))

    SYS_ioctl_9 = Syscall("ioctl", "cmd == FIOASYNC")
    SYS_ioctl_9.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_9.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl_9.add_param(
            Parameter(2, "int __user *", "arg",
                Flow.KERNEL, "int", Element.TYPE))

    SYS_ioctl = Syscall("ioctl")
    SYS_ioctl.add_struct(STRUCT_termios)
    SYS_ioctl.add_struct(STRUCT_termio)
    SYS_ioctl.add_struct(STRUCT_winsize)
    SYS_ioctl.add_sibling(SYS_ioctl_1)
    SYS_ioctl.add_sibling(SYS_ioctl_2)
    SYS_ioctl.add_sibling(SYS_ioctl_3)
    SYS_ioctl.add_sibling(SYS_ioctl_4)
    SYS_ioctl.add_sibling(SYS_ioctl_5)
    SYS_ioctl.add_sibling(SYS_ioctl_6)
    SYS_ioctl.add_sibling(SYS_ioctl_7)
    SYS_ioctl.add_sibling(SYS_ioctl_8)
    SYS_ioctl.add_sibling(SYS_ioctl_9)
    SYS_ioctl.add_param(
            Parameter(0, "unsigned int", "fd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl.add_param(
            Parameter(1, "unsigned int", "cmd",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_ioctl.add_param(
            Parameter(2, "void *", "arg",
                Flow.KERNEL, "void", Element.VALUE))

    # sock

    SYS_socket = Syscall("socket")
    SYS_socket.add_param(
            Parameter(0, "int", "domain",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_socket.add_param(
            Parameter(1, "int", "type",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_socket.add_param(
            Parameter(2, "int", "protocol",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_connect = Syscall("connect")
    SYS_connect.add_struct(STRUCT_sockaddr)
    SYS_connect.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_connect.add_param(
            Parameter(1, "struct sockaddr __user *", "addr",
                Flow.KERNEL, "struct sockaddr", Element.STRUCT,
                struct="sockaddr"))
    SYS_connect.add_param(
            Parameter(2, "int", "addrlen",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_bind = Syscall("bind")
    SYS_bind.add_struct(STRUCT_sockaddr)
    SYS_bind.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_bind.add_param(
            Parameter(1, "struct sockaddr __user *", "addr",
                Flow.KERNEL, "struct sockaddr", Element.STRUCT, 
                struct="sockaddr")) 
    SYS_bind.add_param(
            Parameter(2, "int", "addrlen",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_accept = Syscall("accept")
    SYS_accept.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_accept.add_param(
            Parameter(2, "int __user *", "addrlen",
                Flow.BOTH, "int", Element.SIMPLE))
    SYS_accept.add_param(
            Parameter(1, "void __user *", "addr",
                Flow.USER, "void", Element.IBUFFER, eidx=2))

    SYS_accept4 = Syscall("accept4")
    SYS_accept4.add_param(
            Parameter(0, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_accept4.add_param(
            Parameter(2, "int __user *", "addrlen",
                Flow.BOTH, "int", Element.SIMPLE))
    SYS_accept4.add_param(
            Parameter(1, "void __user *", "addr",
                Flow.USER, "void", Element.IBUFFER, eidx=2))
    SYS_accept4.add_param(
            Parameter(3, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_listen = Syscall("listen")
    SYS_listen.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_listen.add_param(
            Parameter(1, "int", "backlog",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_shutdown = Syscall("shutdown")
    SYS_shutdown.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_shutdown.add_param(
            Parameter(1, "int", "how",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_socketpair = Syscall("socketpair")
    SYS_socketpair.add_param(
            Parameter(0, "int", "domain",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_socketpair.add_param(
            Parameter(1, "int", "type",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_socketpair.add_param(
            Parameter(2, "int", "protocol",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_socketpair.add_param(
            Parameter(3, "int __user *", "sv",
                Flow.USER, "int", Element.VALUE_FIX, eidx=2))

    SYS_setsockopt = Syscall("setsockopt")
    SYS_setsockopt.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_setsockopt.add_param(
            Parameter(1, "int", "level",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_setsockopt.add_param(
            Parameter(2, "int", "optname",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_setsockopt.add_param(
            Parameter(3, "char __user *", "optval",
                Flow.KERNEL, "char", Element.BUFFER, eidx=4))
    SYS_setsockopt.add_param(
            Parameter(4, "int", "optlen",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_getsockopt = Syscall("getsockopt")
    SYS_getsockopt.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_getsockopt.add_param(
            Parameter(1, "int", "level",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_getsockopt.add_param(
            Parameter(2, "int", "optname",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_getsockopt.add_param(
            Parameter(4, "int __user *", "optlen",
                Flow.BOTH, "int", Element.SIMPLE))
    SYS_getsockopt.add_param(
            Parameter(3, "char __user *", "optval",
                Flow.USER, "char", Element.IBUFFER, eidx=4))

    SYS_getsockname = Syscall("getsockname")
    SYS_getsockname.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_getsockname.add_param(
            Parameter(2, "int __user *", "addrlen",
                Flow.BOTH, "int", Element.SIMPLE))
    SYS_getsockname.add_param(
            Parameter(1, "void __user *", "addr",
                Flow.USER, "void", Element.IBUFFER, eidx=2))

    SYS_recvfrom = Syscall("recvfrom")
    SYS_recvfrom.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_recvfrom.add_param(
            Parameter(1, "void __user *", "buf",
                Flow.USER, "void", Element.BUFFER, eidx=2))
    SYS_recvfrom.add_param(
            Parameter(2, "size_t", "size",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_recvfrom.add_param(
            Parameter(3, "unsigned int", "flags",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_recvfrom.add_param(
            Parameter(5, "int __user *", "addrlen",
                Flow.BOTH, "int", Element.SIMPLE))
    SYS_recvfrom.add_param(
            Parameter(4, "void __user *", "addr",
                Flow.USER, "void", Element.IBUFFER, eidx=5))

    sendto_buf_compare = \
'''
if(buf){
\tif(len > 0){
\t\tif(!temp_buf || memcmp(buf, temp_buf, len)){
\t\t\tlog_e(vcb, "SYS", __NR_sendto, "deviation -> buf");
\t\t\ton_deviation(vcb);
\t\t}
\t}
} else if(temp_buf){
\tlog_e(vcb, "SYS", __NR_sendto, "deviation -> buf");
\ton_deviation(vcb);
}
'''

    SYS_sendto = Syscall("sendto")
    SYS_sendto.add_struct(STRUCT_sockaddr)
    SYS_sendto.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_sendto.add_param(
            Parameter(1, "void __user *", "buf",
                Flow.KERNEL, "void", Element.BUFFER, eidx=2,
                compare=sendto_buf_compare))
    SYS_sendto.add_param(
            Parameter(2, "size_t", "len",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_sendto.add_param(
            Parameter(3, "unsigned int", "flags",
                Flow.KERNEL, "unsigned int", Element.VALUE))
    SYS_sendto.add_param(
            Parameter(4, "struct sockaddr __user *", "addr",
                Flow.KERNEL, "struct sockaddr", Element.STRUCT, 
                struct="sockaddr"))
    SYS_sendto.add_param(
            Parameter(5, "int", "addrlen",
                Flow.KERNEL, "int", Element.VALUE))

    recvmsg_msg_fetch = \
'''
if(msg){
\tif(msg->msg_name){
\t\tcopy_to_user(msg->msg_name, temp_msg->msg_name, temp_msg->msg_namelen);
\t}
\tstruct iovec *iov = msg->msg_iov;
\tsize_t iov_count = msg->msg_iovlen;
\tstruct iovec *temp_iov;
\tif(iov){
\t\ttemp_iov = temp_msg->msg_iov;
\t\tfor(int i=0; i<iov_count; i++){
\t\t\tiov[i].iov_len = temp_iov[i].iov_len;
\t\t\tcopy_to_user(iov[i].iov_base, temp_iov[i].iov_base, temp_iov[i].iov_len);
\t\t}
\t}
\tif(msg->msg_control){
\t\tcopy_to_user(msg->msg_control, temp_msg->msg_control, temp_msg->msg_controllen);
\t}
\tmsg->msg_controllen = temp_msg->msg_controllen;
\tmsg->msg_flags = temp_msg->msg_flags;
}
'''
    recvmsg_msg_turnin = \
'''
if(msg){
\ttemp_msg = vmalloc(sizeof(MSGHDR_TYPE));
\tcopy_from_user(temp_msg, msg, sizeof(MSGHDR_TYPE));
\tif(msg->msg_name){
\t\ttemp_msg->msg_name = vmalloc(msg->msg_namelen);
\t\tcopy_from_user(temp_msg->msg_name, msg->msg_name, msg->msg_namelen);
\t}
\tstruct iovec *iov = msg->msg_iov;
\tsize_t iov_count = msg->msg_iovlen;
\tstruct iovec *temp_iov;
\tif(iov){
\t\ttemp_msg->msg_iov = vmalloc(sizeof(struct iovec) * iov_count);
\t\ttemp_iov = temp_msg->msg_iov;
\t\tfor(int i=0; i<iov_count; i++){
\t\t\ttemp_iov[i].iov_len = iov[i].iov_len;
\t\t\ttemp_iov[i].iov_base = vmalloc(iov[i].iov_len);
\t\t\tcopy_from_user(temp_iov[i].iov_base, iov[i].iov_base, iov[i].iov_len);
\t\t}
\t}
\tif(msg->msg_control){
\t\ttemp_msg->msg_control = vmalloc(msg->msg_controllen);
\t\tcopy_from_user(temp_msg->msg_control, msg->msg_control, msg->msg_controllen);
\t}
} else {
\ttemp_msg = NULL;
}
'''

    recvmsg_msg_rclean = \
'''
if(temp_msg){
\tif(temp_msg->msg_name){
\t\tvfree(temp_msg->msg_name);
\t}
\tstruct iovec *iov = temp_msg->msg_iov;
\tsize_t iov_count = temp_msg->msg_iovlen;
\tif(iov){
\t\tfor(int i=0; i<iov_count; i++){
\t\t\tvfree(iov[i].iov_base);
\t\t}
\t\tvfree(iov);
\t}
\tif(temp_msg->msg_control){
\t\tvfree(temp_msg->msg_control);
\t}
\tvfree(temp_msg);
}
'''

    SYS_recvmsg = Syscall("recvmsg", includes=["linux/socket.h"])
    SYS_recvmsg.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_recvmsg.add_param(
            Parameter(1, "MSGHDR_TYPE __user *", "msg",
                Flow.USER, "MSGHDR_TYPE", Element.STRUCT,
                turnin=recvmsg_msg_turnin, 
                fetch=recvmsg_msg_fetch, 
                rclean=recvmsg_msg_rclean))
    SYS_recvmsg.add_param(
            Parameter(2, "unsigned int", "flags",
                Flow.KERNEL, "unsigned int", Element.VALUE))

    sendmsg_msg_compare = \
'''
if(msg){
\tif(msg->msg_namelen != temp_msg->msg_namelen){
\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\ton_deviation(vcb);
\t}
\tif(msg->msg_name){
\t\tif(!temp_msg->msg_name || memcmp(msg->msg_name, temp_msg->msg_name, msg->msg_namelen)){
\t\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\t\ton_deviation(vcb);
\t\t} 
\t} else if(temp_msg->msg_name){
\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\ton_deviation(vcb);
\t}
\tstruct iovec *iov = msg->msg_iov;
\tsize_t iov_count = msg->msg_iovlen;
\tstruct iovec *temp_iov = temp_msg->msg_iov;
\tsize_t temp_iov_count = temp_msg->msg_iovlen;
\tif(iov_count != temp_iov_count){
\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\ton_deviation(vcb);
\t}
\tif(iov){
\t\tfor(int i=0; i<iov_count; i++){
\t\t\tif(iov[i].iov_len != temp_iov[i].iov_len){
\t\t\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\t\t\ton_deviation(vcb);
\t\t\t}
\t\t\tif(iov[i].iov_base){
\t\t\t\tif(!temp_iov[i].iov_base || memcmp(iov[i].iov_base, temp_iov[i].iov_base, iov[i].iov_len)){
\t\t\t\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\t\t\t\ton_deviation(vcb);
\t\t\t\t}
\t\t\t} else if(temp_iov[i].iov_base){
\t\t\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\t\t\ton_deviation(vcb);
\t\t\t}
\t\t}
\t}
\tif(msg->msg_controllen != temp_msg->msg_controllen){
\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\ton_deviation(vcb);
\t}
\tif(msg->msg_control){
\t\tif(!temp_msg->msg_control || memcmp(msg->msg_control, temp_msg->msg_control, msg->msg_controllen)){
\t\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\t\ton_deviation(vcb);
\t\t}
\t} else if(temp_msg->msg_control){
\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg"); 
\t\ton_deviation(vcb);
\t}
\tif(msg->msg_flags != temp_msg->msg_flags){
\t\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\t\ton_deviation(vcb);
\t}
} else if(temp_msg){
\tlog_e(vcb, "SYS", __NR_sendmsg, "deviation -> msg");
\ton_deviation(vcb);
}
'''
    sendmsg_msg_checkin = \
'''
if(msg){
\ttemp_msg = vmalloc(sizeof(MSGHDR_TYPE));
\tcopy_from_user(temp_msg, msg, sizeof(MSGHDR_TYPE));
\tif(msg->msg_name){
\t\ttemp_msg->msg_name = vmalloc(msg->msg_namelen);
\t\tcopy_from_user(temp_msg->msg_name, msg->msg_name, msg->msg_namelen);
\t}
\tstruct iovec *iov = msg->msg_iov;
\tsize_t iov_count = msg->msg_iovlen;
\tstruct iovec *temp_iov;
\tif(iov){
\t\ttemp_msg->msg_iov = vmalloc(sizeof(struct iovec) * iov_count);
\t\ttemp_iov = temp_msg->msg_iov;
\t\tfor(int i=0; i<iov_count; i++){
\t\t\ttemp_iov[i].iov_len = iov[i].iov_len;
\t\t\ttemp_iov[i].iov_base = vmalloc(iov[i].iov_len);
\t\t\tcopy_from_user(temp_iov[i].iov_base, iov[i].iov_base, iov[i].iov_len);
\t\t}
\t}
\tif(msg->msg_control){
\t\ttemp_msg->msg_control = vmalloc(msg->msg_controllen);
\t\tcopy_from_user(temp_msg->msg_control, msg->msg_control, msg->msg_controllen);
\t}
} else {
\ttemp_msg = NULL;
}
'''

    sendmsg_msg_pclean = \
'''
if(temp_msg){
\tif(temp_msg->msg_name){
\t\tvfree(temp_msg->msg_name);
\t}
\tstruct iovec *iov = temp_msg->msg_iov;
\tsize_t iov_count = temp_msg->msg_iovlen;
\tif(iov){
\t\tfor(int i=0; i<iov_count; i++){
\t\t\tvfree(iov[i].iov_base);
\t\t}
\t\tvfree(iov);
\t}
\tif(temp_msg->msg_control){
\t\tvfree(temp_msg->msg_control);
\t}
\tvfree(temp_msg);
}
'''

    SYS_sendmsg = Syscall("sendmsg", includes=["linux/socket.h"])
    SYS_sendmsg.add_param(
            Parameter(0, "int", "sockfd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_sendmsg.add_param(
            Parameter(1, "MSGHDR_TYPE __user *", "msg",
                Flow.KERNEL, "MSGHDR_TYPE", Element.STRUCT,
                checkin=sendmsg_msg_checkin, 
                compare=sendmsg_msg_compare, 
                pclean=sendmsg_msg_pclean, 
                turnin="", fetch="", rclean=""))
    SYS_sendmsg.add_param(
            Parameter(2, "unsigned int", "flags",
                Flow.KERNEL, "unsigned int", Element.VALUE))


    # mem

    mmap_pre = \
'''
if(fd == -1){
\treturn ref_SYS_mmap(addr, length, prot, flags, fd, offset);
}
'''

    mmap_fpre = \
'''
int nprot = prot | PROT_WRITE;
int nflags = flags | MAP_ANONYMOUS;

addr = (void *)ref_SYS_mmap(addr, length, nprot, nflags, -1, 0);
'''

    mmap_fpost = \
'''
retval = (unsigned long)addr;
'''

    mmap_addr_turnin = \
'''
if(retval > 0){
\ttemp_addr = vmalloc(length);
\tcopy_from_user(temp_addr, (void *)retval, length);
} else {
\ttemp_addr = NULL;
}
'''

    SYS_mmap = Syscall("mmap",
            pre=mmap_pre, fpre=mmap_fpre, fpost=mmap_fpost,
            includes=["asm/mman.h"])
    SYS_mmap.add_param(
            Parameter(0, "void *", "addr",
                Flow.USER, "void", Element.BUFFER, eidx=1,
                compare="", turnin=mmap_addr_turnin))
    SYS_mmap.add_param(
            Parameter(1, "size_t", "length",
                Flow.KERNEL, "size_t", Element.VALUE))
    SYS_mmap.add_param(
            Parameter(2, "int", "prot",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_mmap.add_param(
            Parameter(3, "int", "flags",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_mmap.add_param(
            Parameter(4, "int", "fd",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_mmap.add_param(
            Parameter(5, "loff_t", "offset",
                Flow.KERNEL, "loff_t", Element.VALUE))

    # ps

    SYS_wait4 = Syscall("wait4")
    SYS_wait4.add_struct(STRUCT_rusage)
    SYS_wait4.add_param(
            Parameter(0, "pid_t", "upid",
                Flow.KERNEL, "pid_t", Element.VALUE))
    SYS_wait4.add_param(
            Parameter(1, "int __user *", "stat",
                Flow.USER, "int", Element.SIMPLE))
    SYS_wait4.add_param(
            Parameter(2, "int", "options",
                Flow.KERNEL, "int", Element.VALUE))
    SYS_wait4.add_param(
            Parameter(3, "struct rusage __user *", "ru",
                Flow.USER, "struct rusage", Element.STRUCT,
                struct="rusage"))

    SYS_kill = Syscall("kill")
    SYS_kill.add_param(
            Parameter(0, "pid_t", "pid", 
                Flow.KERNEL, "pid_t", Element.VALUE))
    SYS_kill.add_param(
            Parameter(1, "int", "sig",
                Flow.KERNEL, "int", Element.VALUE))

    SYS_tgkill = Syscall("tgkill")
    SYS_tgkill.add_param(
            Parameter(0, "pid_t", "tgid", 
                Flow.KERNEL, "pid_t", Element.VALUE))
    SYS_tgkill.add_param(
            Parameter(1, "pid_t", "pid",
                Flow.KERNEL, "pid_t", Element.VALUE))
    SYS_tgkill.add_param(
            Parameter(2, "int", "sig",
                Flow.KERNEL, "int", Element.VALUE))

    # automatic code generation

    GROUPS = []

    # collect syscalls
    GROUP_sys = Group("sys")
    GROUP_sys.add_syscall(SYS_times)
    GROUP_sys.add_syscall(SYS_sysinfo)
    GROUP_sys.add_syscall(SYS_newuname)
    GROUP_sys.add_syscall(SYS_umask)

    GROUP_sys.add_syscall(SYS_sethostname)
    GROUP_sys.add_syscall(SYS_setdomainname)

    GROUP_sys.add_syscall(SYS_getrlimit)
    GROUP_sys.add_syscall(SYS_setrlimit)
    GROUP_sys.add_syscall(SYS_getrusage)

    GROUP_sys.add_syscall(SYS_getpriority)
    GROUP_sys.add_syscall(SYS_setpriority)

    GROUP_sys.add_syscall(SYS_getpid)
    GROUP_sys.add_syscall(SYS_gettid)
    GROUP_sys.add_syscall(SYS_getppid)
    GROUP_sys.add_syscall(SYS_getpgrp)
    GROUP_sys.add_syscall(SYS_setpgid)

    GROUP_sys.add_syscall(SYS_getsid)
    GROUP_sys.add_syscall(SYS_setsid)

    GROUP_sys.add_syscall(SYS_getuid)
    GROUP_sys.add_syscall(SYS_setuid)
    GROUP_sys.add_syscall(SYS_geteuid)
    GROUP_sys.add_syscall(SYS_setreuid)
    GROUP_sys.add_syscall(SYS_getresuid)
    GROUP_sys.add_syscall(SYS_setresuid)
    GROUP_sys.add_syscall(SYS_setfsuid)

    GROUP_sys.add_syscall(SYS_getgid)
    GROUP_sys.add_syscall(SYS_setgid)
    GROUP_sys.add_syscall(SYS_getegid)
    GROUP_sys.add_syscall(SYS_setregid)
    GROUP_sys.add_syscall(SYS_getresgid)
    GROUP_sys.add_syscall(SYS_setresgid)
    GROUP_sys.add_syscall(SYS_setfsgid)
    GROUP_sys.add_syscall(SYS_getgroups)
    GROUP_sys.add_syscall(SYS_setgroups)

    GROUP_sys.add_syscall(SYS_getcwd)
    GROUP_sys.add_syscall(SYS_gettimeofday)
    GROUP_sys.add_syscall(SYS_time)
    GROUP_sys.add_syscall(SYS_clock_gettime)
    GROUP_sys.add_syscall(SYS_clock_getres)

    #GROUP_sys.add_syscall(SYS_sched_getparam)
    #GROUP_sys.add_syscall(SYS_sched_getscheduler)
    #GROUP_sys.add_syscall(SYS_sched_get_priority_min)
    #GROUP_sys.add_syscall(SYS_sched_get_priority_max)
    
    GROUP_sys.add_syscall(SYS_getcpu)

    GROUP_fs = Group("fs")
    GROUP_fs.add_syscall(SYS_access)
    GROUP_fs.add_syscall(SYS_faccessat)
    GROUP_fs.add_syscall(SYS_readlink)
    GROUP_fs.add_syscall(SYS_readlinkat)

    GROUP_fs.add_syscall(SYS_stat)
    GROUP_fs.add_syscall(SYS_fstat)
    GROUP_fs.add_syscall(SYS_lstat)
    GROUP_fs.add_syscall(SYS_newfstatat)

    GROUP_fs.add_syscall(SYS_truncate)
    GROUP_fs.add_syscall(SYS_ftruncate)

    GROUP_fs.add_syscall(SYS_link)
    GROUP_fs.add_syscall(SYS_linkat)
    GROUP_fs.add_syscall(SYS_symlink)
    GROUP_fs.add_syscall(SYS_symlinkat)
    GROUP_fs.add_syscall(SYS_unlink)
    GROUP_fs.add_syscall(SYS_unlinkat)
    GROUP_fs.add_syscall(SYS_rename)
    GROUP_fs.add_syscall(SYS_renameat)

    GROUP_fs.add_syscall(SYS_mkdir)
    GROUP_fs.add_syscall(SYS_mkdirat)
    GROUP_fs.add_syscall(SYS_rmdir)
    GROUP_fs.add_syscall(SYS_chdir)
    GROUP_fs.add_syscall(SYS_fchdir)
    GROUP_fs.add_syscall(SYS_mknod)
    GROUP_fs.add_syscall(SYS_mknodat)

    GROUP_fs.add_syscall(SYS_chmod)
    GROUP_fs.add_syscall(SYS_fchmod)
    GROUP_fs.add_syscall(SYS_chown)
    GROUP_fs.add_syscall(SYS_fchown)
    GROUP_fs.add_syscall(SYS_lchown)
    GROUP_fs.add_syscall(SYS_fchownat)

    GROUP_fs.add_syscall(SYS_setxattr)
    GROUP_fs.add_syscall(SYS_fsetxattr)
    GROUP_fs.add_syscall(SYS_lsetxattr)
    GROUP_fs.add_syscall(SYS_getxattr)
    GROUP_fs.add_syscall(SYS_fgetxattr)
    GROUP_fs.add_syscall(SYS_lgetxattr)
    GROUP_fs.add_syscall(SYS_removexattr)
    GROUP_fs.add_syscall(SYS_fremovexattr)
    GROUP_fs.add_syscall(SYS_lremovexattr)

    GROUP_fs.add_syscall(SYS_statfs)
    GROUP_fs.add_syscall(SYS_fstatfs)

    GROUP_fs.add_syscall(SYS_getdents)

    GROUP_io = Group("io")
    GROUP_io.add_syscall(SYS_open)
    GROUP_io.add_syscall(SYS_openat)
    GROUP_io.add_syscall(SYS_creat)
    GROUP_io.add_syscall(SYS_close)
    
    GROUP_io.add_syscall(SYS_lseek)
    GROUP_io.add_syscall(SYS_read)
    GROUP_io.add_syscall(SYS_write)
    GROUP_io.add_syscall(SYS_pread64)
    GROUP_io.add_syscall(SYS_pwrite64)
    GROUP_io.add_syscall(SYS_readv)
    GROUP_io.add_syscall(SYS_writev)

    GROUP_io.add_syscall(SYS_pipe)
    GROUP_io.add_syscall(SYS_pipe2)
    GROUP_io.add_syscall(SYS_eventfd)
    GROUP_io.add_syscall(SYS_eventfd2)
    GROUP_io.add_syscall(SYS_epoll_create)
    GROUP_io.add_syscall(SYS_epoll_create1)
    GROUP_io.add_syscall(SYS_epoll_ctl)

    GROUP_io.add_syscall(SYS_sendfile)
    GROUP_io.add_syscall(SYS_sendfile64)

    GROUP_io.add_syscall(SYS_dup)
    GROUP_io.add_syscall(SYS_dup2)
    GROUP_io.add_syscall(SYS_dup3)

    GROUP_io.add_syscall(SYS_poll)
    GROUP_io.add_syscall(SYS_ppoll)
    GROUP_io.add_syscall(SYS_select)
    GROUP_io.add_syscall(SYS_pselect6)

    GROUP_io.add_syscall(SYS_fcntl)
    GROUP_io.add_syscall(SYS_ioctl)

    GROUP_sock = Group("sock")
    GROUP_sock.add_syscall(SYS_socket)
    GROUP_sock.add_syscall(SYS_socketpair)
    GROUP_sock.add_syscall(SYS_shutdown)
    
    GROUP_sock.add_syscall(SYS_connect)
    GROUP_sock.add_syscall(SYS_bind)
    GROUP_sock.add_syscall(SYS_accept)
    GROUP_sock.add_syscall(SYS_accept4)
    GROUP_sock.add_syscall(SYS_listen)

    GROUP_sock.add_syscall(SYS_getsockopt)
    GROUP_sock.add_syscall(SYS_setsockopt)
    GROUP_sock.add_syscall(SYS_getsockname)

    GROUP_sock.add_syscall(SYS_recvfrom)
    GROUP_sock.add_syscall(SYS_sendto)
    GROUP_sock.add_syscall(SYS_recvmsg)
    GROUP_sock.add_syscall(SYS_sendmsg)

    GROUP_mem = Group("mem")
    GROUP_mem.add_syscall(SYS_mmap)

    GROUP_ps = Group("ps")
    GROUP_ps.add_syscall(SYS_wait4)
    GROUP_ps.add_syscall(SYS_kill)
    GROUP_ps.add_syscall(SYS_tgkill)

    # collect groups
    GROUPS.append(GROUP_sys)
    GROUPS.append(GROUP_fs)
    GROUPS.append(GROUP_io)
    GROUPS.append(GROUP_sock)
    GROUPS.append(GROUP_mem)
    GROUPS.append(GROUP_ps)

    # generate code
    for group in GROUPS:
        group.output_all()

    generate_from_comments(GROUPS, "%s/systable.c" % SOURCE)

    # generate list
    with open(SYSLIST, "w+") as f:
        for group in GROUPS:
            for syscall in group.syscalls:
                f.write("%s\n" % syscall.name)
