
runcaller := run-caller
allrun += acceptance-run kernel-run performance-run regression-run kernel-all-run 
kgraft_run += kgraft-kernel-run kgraft-performance-run
openqa_run += acceptance-run.openqa kernel-run.openqa regression-run.openqa kernel-all-run.openqa

allrun += $(openqa_run)

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
		install -m 755 $${run} $(RUN_DEST); \
	done

.PHONY: install
