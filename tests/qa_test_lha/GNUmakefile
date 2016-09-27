name = lha

mandir      = @mandir@
man1dir     = $(mandir)/man8
manpage1    = qa_test$(name).8
tcffile	    = qa_$(name).tcf
runfile     = test_$(name)-run
testdir     = qa_test_$(name)

.PHONY: all
all: $(tcffile)

$(tcffile): $(testdir)/*.t
	./make-tcf $(sort $^) > $@

.PHONY: check
check:
	@mkdir -p $$PWD/fixtures
	@cram $$PWD
	@rmdir $$PWD/fixtures

.PHONY: tarball
tarball:
	git archive -o $(testdir).tar.gz --prefix $(testdir)/ HEAD

.PHONY: install
install: installdirs manpage
	install -m 0755 -t $(DESTDIR)/usr/share/qa/tools/ $(runfile)
	install -m 0644 -t $(DESTDIR)/usr/share/qa/tcf/ $(tcffile)

	cp -r $(testdir) $(DESTDIR)/usr/share/qa/


.PHONY: manpage
manpage:
	install -m 755 -d $(DESTDIR)/usr/share/man/man8
	gzip qa_test_$(name).8
	install -m 644 qa_test_$(name).8.gz $(DESTDIR)/usr/share/man/man8

.PHONY: installdirs
installdirs:
	install -m 0755 -d $(DESTDIR)/usr/share/qa/
	install -m 0755 -d $(DESTDIR)/usr/share/qa/tools/
	install -m 0755 -d $(DESTDIR)/usr/share/qa/tcf/
	install -m 0755 -d $(DESTDIR)/usr/share/qa/$(testdir)/

