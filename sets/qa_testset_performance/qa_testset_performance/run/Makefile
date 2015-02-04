
allrun += qaset-acceptance-run qaset-kernel-run qaset-performance-run qaset-regression-run
kgraft_run += qaset-kgraft-kernel-run qaset-kgraft-performance-run

ifneq (,$(findstring SLE12, $(TARGET_RELEASE)))
allrun += $(kgraft_run)
endif

RUN_DEST := $(dest)/run

install:
	install -d $(RUN_DEST)
	install -m 755 $(allrun) $(RUN_DEST)
	for run in $(allrun); do \
		sed -i '/^TARGET_RELEASE=/s/TARGET_RELEASE=/TARGET_RELEASE=$(TARGET_RELEASE)/' $(RUN_DEST)/$${run}; \
		sed -i '/^QASET_ROOT=/s#^.*$$#QASET_ROOT=$(prefix)#' $(RUN_DEST)/$${run}; \
	done

.PHONY: install
