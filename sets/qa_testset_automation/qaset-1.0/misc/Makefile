
SYSTEMD_SERVICE := qaperf.service
SYSV_SERVICE := qaset
SYSV_SERVICE_INSTALL := sysv-install
ifneq (,$(findstring SLE12, $(TARGET_RELEASE)))
service: $(SYSTEMD_SERVICE)
	install -d $(DEST)/usr/lib/systemd/system/multi-user.target.wants
	install -m 644 $(SYSTEMD_SERVICE) $(DEST)/usr/lib/systemd/system/qaperf.service
endif
ifneq (,$(findstring SLE11, $(TARGET_RELEASE)))
service: $(SYSV_SERVICE) $(SYSV_SERVICE_INSTALL)
	install -d $(DEST)/etc/init.d
	install -m 755 $(SYSV_SERVICE) $(DEST)/etc/init.d
	install -m 755 $(SYSV_SERVICE_INSTALL) $(dest)/$(SYSV_SERVICE_INSTALL)
endif

install: $(service)

.PHONY: install $(service)
