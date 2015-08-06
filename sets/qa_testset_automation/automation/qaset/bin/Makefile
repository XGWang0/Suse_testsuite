BIN_DEST := $(dest)/bin

bin_list := submitlog.sh cucumber_generator.jar  cu_report_generator.py

install:
	install -d $(BIN_DEST)
	install -m 755 $(bin_list) $(BIN_DEST)

.PHONY: install
