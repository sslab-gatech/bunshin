CC = gcc
PROG = prog
SRCS = prog.c
FLAGS = -Wall -std=gnu11 -D_GNU_SOURCE -O2 

all: $(PROG)

$(PROG): $(SRCS)
	$(CC) $(FLAGS) $^ -o $@

clean:
	@rm -rf $(PROG)

.PHONY: all clean
