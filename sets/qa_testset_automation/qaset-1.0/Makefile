
TARGET_RELEASE := SLE12
prefix := /usr/share/qa/qaset
dest := $(DEST)/$(prefix)
export TARGET_RELEASE
export prefix
export dest

all: install

SUBDIRS = conf list misc qavm run set
subdir: $(SUBDIRS)
QASETBINS := qaset qaset-service
qasetbin: $(QASETBINS)


$(SUBDIRS):
	$(MAKE) -C $@

$(QASETBINS):
	install -m 755 $@ $(dest)
	sed -i '/^QASET_ROOT=/s#^.*$$#QASET_ROOT=$(prefix)#' $(dest)/$@;

install: subdir qasetbin

.PHONY: all install subdir qasetbin $(SUBDIRS) $(QASETBINS)
