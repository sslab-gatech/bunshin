ECFLAGS = -std=gnu11 -fno-omit-frame-pointer \
					-Wall -Wno-declaration-after-statement -march=native -O2 \
					-DSYNC_ORDER

obj-m += kmvee.o

kmvee-objs := logger.o mcall.o systable.o ctl.o mvee.o signal.o thread.o \
	stub_sys.o stub_fs.o stub_io.o stub_sock.o stub_mem.o stub_ps.o 

KMOD = kmvee

all: $(KMOD)

release: $(KMOD)

debug: ECFLAGS += -DDEBUG
debug: $(KMOD)

trace: ECFLAGS += -DTRACE
trace: $(KMOD)

$(KMOD): 
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) EXTRA_CFLAGS="$(ECFLAGS)" modules

clean:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) clean
	
insmod:
	sudo insmod $(obj-m:.o=.ko)
	lsmod | grep $(obj-m:.o=)
	
rmmod:
	sudo rmmod $(obj-m:.o=.ko)
