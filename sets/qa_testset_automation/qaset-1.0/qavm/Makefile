
QAVM_DEST := $(dest)/qavm
qavm_lib := import.sh sq-control.sh sq-execute.sh sq-global.sh  sq-mach.sh sq-util.sh sq-result.sh sq-hook.sh

install: sq-fake.sh
	install -d $(QAVM_DEST)
	install -m 644 $(qavm_lib) $(QAVM_DEST)
	install -m 755 sq-fake.sh $(QAVM_DEST)

.PHONY: install
