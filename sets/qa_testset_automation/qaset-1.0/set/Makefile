
SET_DEST := $(dest)/set

allset := acceptance.set  kernel.set  kgraft-kernel.set  performance.set  regression.set kgraft-performance.set

install:
	install -d $(SET_DEST)
	install -m 644 $(allset) $(SET_DEST)

.PHONY: install
