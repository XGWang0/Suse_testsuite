
allconf := common.conf SLE11SP3.conf  SLE11SP4.conf  SLE12.conf SLE12SP1.conf SLE12SP2.conf

CONF_DEST := $(dest)/conf

install:
	install -d $(CONF_DEST)
	install -m 644 $(allconf) $(CONF_DEST)

.PHONY: install

