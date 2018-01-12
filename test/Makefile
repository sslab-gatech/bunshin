DIRS = $(wildcard */) 

define runall
	@for d in $(DIRS); do \
	  echo "==================================================="; \
	  echo "[*] $1 $$d"; \
	  $(MAKE) --no-print-directory -C $$d $2; \
	done
endef

all:
	$(call runall,"Building")

clean:
	$(call runall,"Cleaning",clean)

.PHONY: all clean

