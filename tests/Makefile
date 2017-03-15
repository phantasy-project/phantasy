.PHONY: test clean

test:
	PYTHONPATH=../:$(PYTHONPATH) \
	nosetests --with-coverage --cover-package=phantasy \
		--with-id -v --logging-level=INFO \
		--exclude-dir-file="skiptests" 

clean:
	[ -e phantasy_data ] && rm -rf phantasy_data
