BIN_DEST := $(dest)/bin

bin_list := submitlog.sh junitxml_generator.py junit_xml_gen.py openqa_runner.py

install:
	install -d $(BIN_DEST)
	install -m 755 $(bin_list) $(BIN_DEST)

.PHONY: install
