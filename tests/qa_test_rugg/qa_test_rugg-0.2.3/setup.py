#!/usr/bin/env python
# Encoding: iso-8859-1
# vim: tw=80 ts=2 sw=2 et
# -----------------------------------------------------------------------------
# Project   : Rugg - Hard drive harness test
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre <sebastien@xprima.com>
# License   : GNU Public License <http://www.gnu.org/licenses/gpl.html>
# Creation  : 24-Mar-2006
# Last mod  : 04-Avr-2006
# History   :
#             04-Avr-2006 - Additional package information
#             24-Mar-2006 - First implementation
# -----------------------------------------------------------------------------

import sys ; sys.path.insert(0, "Sources")
from rugg import main
from distutils.core import setup

SUMMARY     = "Flexible file system and hard drive crash testing"
DESCRIPTION = """\
Rugg is a hard drive and filesystem harness tool that allows you to test and
benchmark drives and filesystems, by writing simple to complex scenarios that
can mimic the behaviour of real-world applications.\
"""
# ------------------------------------------------------------------------------
#
# SETUP DECLARATION
#
# ------------------------------------------------------------------------------

setup(
    name        = "Rugg",
    version     = main.__version__,
    author      = "Sebastien Pierre", author_email = "sebastien@xprima.com",
    description = SUMMARY, long_description = DESCRIPTION,
    license     = "GNU General Public License",
    keywords    = "disk, filesystem, harness, testing, unit, scenario,language",
    url         = "http://rugg.sourceforge.net",
    download_url= "http://prdownloads.sourceforge.net/rugg/Rugg-%s.tar.gz?download" % (main.__version__) ,
    package_dir = { "": "Sources" },
    packages    = ["rugg"],
    scripts     = ["Scripts/rugg"],
    classifiers = [
      "Development Status :: 4 - Beta",
      "Environment :: Console",
      "Intended Audience :: Information Technology",
      "Intended Audience :: System Administrators",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Operating System :: POSIX",
      "Programming Language :: Python",
      "Topic :: Software Development :: Interpreters",
      "Topic :: Software Development :: Testing",
      "Topic :: System",
      "Topic :: System :: Benchmark",
      "Topic :: System :: Filesystems"
    ]
)

# EOF
