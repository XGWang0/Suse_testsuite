NAME:=qa_test_subversion
SOURCE0:=${NAME}
SOURCE1:=qa_subversion.tcf
SOURCE2:=test_subversion-run
SOURCE3:=qa_test_subversion.8

build:

install:

	install -m 755 -d ${DESTDIR}/usr/share/man/man8/
	install -m 644 ${SOURCE3} ${DESTDIR}/usr/share/man/man8
	gzip ${DESTDIR}/usr/share/man/man8/${NAME}.8
	install -m 755 -d ${DESTDIR}/usr/share/qa/${NAME}/tcf
	install -m 755 -d ${DESTDIR}/usr/share/qa/tcf
	install -m 755 -d ${DESTDIR}/usr/share/qa/tools
	install -m 644 ${SOURCE1} ${DESTDIR}/usr/share/qa/${NAME}/tcf
	ln -nfs ../${NAME}/tcf/qa_subversion.tcf ${DESTDIR}/usr/share/qa/tcf/
	install -m 755 ${SOURCE2} ${DESTDIR}/usr/share/qa/tools
	cp -a ${SOURCE0}/* ${DESTDIR}/usr/share/qa/${NAME}
	chmod 755 ${DESTDIR}/usr/share/qa/${NAME}/svn.sh
	find ${DESTDIR}/usr/share/qa/${NAME} -depth -type d \( -name CVS -or -name .svn \) -exec rm -rf {} \;
