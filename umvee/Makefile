CC = gcc 
CFLAGS = -Wall -std=gnu11 -D_GNU_SOURCE -march=native -O2 -flto \
				 -DSYNC_ORDER
LDFLAGS = -Wall
LDLIBS = -lrt

LAUNCHER = launcher
SANDBOX = sandbox.so 

PROG = $(LAUNCHER) $(SANDBOX) 

all: $(PROG)

release: $(PROG)

debug: CFLAGS += -DDEBUG
debug: $(PROG)

trace: CFLAGS += -DTRACE
trace: $(PROG)

$(LAUNCHER): logger.o launcher.o
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

$(SANDBOX): CFLAGS += -fPIC
$(SANDBOX): LDFLAGS += -fPIC -shared -Wl,--no-as-needed
$(SANDBOX): LDLIBS += -ldl
$(SANDBOX): logger.o sandbox.o
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

clean:
	rm -f *.o $(PROG)
