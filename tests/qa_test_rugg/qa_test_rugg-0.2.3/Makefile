# Rugg makefile
# -------------
#  Revision 1.5.1 (24-Mar-2006)
#  (c) Sébastien Pierre - XPrima Corp 2006
#  
#  This Makefile is intendended for developers only. It allows to automate
#  common tasks such as checking the code, getting statistics, listing the TODO,
#  FIXME, etc, generating the documentation, packaging a source tarball and so
#  on.
#
#  On of the main advantage is that this Makefile can "prepare" the development
#  environment quickly by creating a symblink from the main package to the
#  proper location in Python site-packages, so that testing can be done without
#  having to run 'setup.py install' each time.
#  
#  For that reason, end-users will use the setup.py, while developers will
#  typically want to use this makefile, by first running "make prepare".

# Project variables___________________________________________________________
#
# Project name. Do not put spaces.
PROJECT         = Rugg
PROJECT_VERSION = 0.2.3
PROJECT_STATUS  = BETA

DOCUMENTATION   = Documentation
SOURCES         = Sources
SCRIPTS         = Scripts
TESTS           = Tests
DISTRIBUTION    = Distribution
DISTROCONTENT   = $(DOCUMENTATION) $(SOURCES) $(SCRIPTS) $(TESTS) \
                  Makefile README LICENSE setup.py

# Project files_______________________________________________________________

PACKAGE         = rugg
MAIN            = main.py
MODULES         = rugg.main rugg.language rugg.typesystem rugg.operations rugg.core

TEST_MAIN       = $(TESTS)/$(PROJECT)Test.py
SOURCE_FILES    = $(shell find $(SOURCES) -name "*.py")
TEST_FILES      = $(shell find $(TESTS) -name "*.py")
CHECK_BLACKLIST = rugg.tpg,rugg.pyparsing

# Tools_______________________________________________________________________

PYTHON          = $(shell which python)
PYTHONHOME      = $(shell $(PYTHON) -c \
 "import sys;print filter(lambda x:x[-13:]=='site-packages',sys.path)[0]")
EPYDOC          = $(shell which epydoc)
PYCHECKER       = $(shell which pychecker)
CTAGS           = $(shell which ctags)

# Useful variables____________________________________________________________

CURRENT_ARCHIVE = $(PROJECT)-$(PROJECT_VERSION).tar.gz
# This is the project name as lower case, used in the install rule
project_lower   = $(shell echo $(PROJECT) | tr "A-Z" "a-z")
# The installation prefix, used in the install rule
prefix          = /usr/local

# Rules_______________________________________________________________________

.PHONY: help info preparing-pre clean check dist doc tags todo

help:
	@echo
	@echo " $(PROJECT) development make rules:"
	@echo
	@echo "    prepare - prepares the project, may require editing this file"
	@echo "    check   - executes pychecker"
	@echo "    clean   - cleans up build files"
	@echo "    test    - executes the test suite"
	@echo "    doc     - generates the documentation"
	@echo "    info    - displays project information"
	@echo "    tags    - generates ctags"
	@echo "    todo    - view TODO, FIXMES, etc"
	@echo "    dist    - generates distribution"
	@echo
	@echo "    Look at the makefile for overridable variables."

all: prepare clean check test doc dist 
	@echo "Making everything for $(PROJECT)"

info:
	@echo "$(PROJECT)-$(PROJECT_VERSION) ($(PROJECT_STATUS))"
	@echo Source file lines:
	@wc -l $(SOURCE_FILES)

todo:
	@grep  -R --only-matching "TODO.*$$"  $(SOURCE_FILES)
	@grep  -R --only-matching "FIXME.*$$" $(SOURCE_FILES)

prepare:
	@echo "WARNING : You may required root priviledges to execute this rule."
	@echo "Preparing python for $(PROJECT)"
#	sudo ln -snf $(PWD)/$(SOURCES)/$(PACKAGE) \
		  $(PYTHONHOME)/$(PACKAGE)
	@echo "Preparing done."

clean:
	@echo "Cleaning $(PROJECT)."
	@find . -name "*.zone" -name "*.pyc" -or -name "*.sw?" -or -name ".DS_Store" -or -name "*.bak" -or -name "*~" -exec rm '{}' ';'
	@rm -rf  build dist

check:
	@echo "Checking $(PROJECT) sources : $(SOURCE_FILES)"
ifeq ($(shell basename spam/$(PYCHECKER)),pychecker)
	@$(PYCHECKER) -b $(CHECK_BLACKLIST) $(SOURCE_FILES)
	@echo "Checking $(PROJECT) tests :"
	@$(PYCHECKER) -b $(CHECK_BLACKLIST) $(TEST_FILES)
else
	@echo "You need Pychecker to check $(PROJECT)."
	@echo "See <http://pychecker.sf.net>"
endif
	@echo "done."

test: $(SOURCE_FILES) $(TEST_FILES)
	@echo "Testing $(PROJECT)."
	@$(PYTHON) $(TEST_MAIN)

dist:
	@echo "Creating archive $(DISTRIBUTION)/$(PROJECT)-$(PROJECT_VERSION).tar.gz"
	@mkdir -p $(DISTRIBUTION)/$(PROJECT)-$(PROJECT_VERSION)
	@cp -r $(DISTROCONTENT) $(DISTRIBUTION)/$(PROJECT)-$(PROJECT_VERSION)
	@make -C $(DISTRIBUTION)/$(PROJECT)-$(PROJECT_VERSION) clean
	@make -C $(DISTRIBUTION)/$(PROJECT)-$(PROJECT_VERSION) doc
	@tar cfz $(DISTRIBUTION)/$(PROJECT)-$(PROJECT_VERSION).tar.gz \
	-C $(DISTRIBUTION) $(PROJECT)-$(PROJECT_VERSION)
	@rm -rf $(DISTRIBUTION)/$(PROJECT)-$(PROJECT_VERSION)

man: README $(DOCUMENTATION)/guide.txt
#	kiwi -m -iutf-8 README  $(DOCUMENTATION)/index.html
#	kiwi -m -iutf-8 LICENSE $(DOCUMENTATION)/license.html
#	kiwi -m -iutf-8 $(DOCUMENTATION)/guide.txt $(DOCUMENTATION)/guide.html
#	kiwi -m -iutf-8 $(DOCUMENTATION)/examples.txt $(DOCUMENTATION)/examples.html

doc: man
	@echo "Generating $(PROJECT) documentation"
ifeq ($(shell basename spam/$(EPYDOC)),epydoc)
	#@$(EPYDOC) --css $(RESOURCES)/epydoc.css --html -o $(API) --name "$(PROJECT) v.$(PROJECT_VERSION)" $(MODULES)
	sdoc -cp $(SOURCES) $(MODULES) > $(DOCUMENTATION)/api.html
else
	@echo "Epydoc is required to generate $(PROJECT) documentation."
	@echo "Please see <http://epydoc.sf.net>"
endif

tags:
	@echo "Generating $(PROJECT) tags"
ifeq ($(shell basename spam/$(CTAGS)),ctags)
	@$(CTAGS) -R
else
	@echo "Ctags is required to generate $(PROJECT) tags."
	@echo "Please see <http://ctags.sf.net>"
endif

#EOF
