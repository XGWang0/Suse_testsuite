
runcaller := run-caller
allrun += acceptance-run kernel-run performance-run regression-run kernel-all-run 
kgraft_run += kgraft-kernel-run kgraft-performance-run

ifneq (,$(findstring SLE12, $(TARGET_RELEASE)))
allrun += $(kgraft_run)
endif

RUN_DEST := $(dest)/run

install:
	install -d $(RUN_DEST)
	install -m 755 $(runcaller) $(RUN_DEST)
	install -m 755 performance-run.upload_Beijing $(RUN_DEST)

	sed -i '/^QASET_ROOT=/s#^.*$$#QASET_ROOT=$(prefix)#' $(RUN_DEST)/$(runcaller)
	for run in $(allrun); do \
		ln -s $(runcaller) $(RUN_DEST)/$${run}; \
	done

.PHONY: install
