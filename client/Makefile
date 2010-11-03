# This Makefile is only used when building Debian packages

PYTHON=/usr/bin/python2.5
DESTDIR=/

all:

source:
	$(PYTHON) setup.py sdist

install: source
	$(PYTHON) setup.py install --root $(DESTDIR) --no-compile -O0

clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete
