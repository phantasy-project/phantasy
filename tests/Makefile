.PHONY: test clean

test:
	PYTHONPATH=../:$(PYTHONPATH) \
	nosetests --with-coverage --cover-package=phantasy \
		--with-id -v --logging-level=INFO \
		--exclude-dir-file="skiptests" 

ioc:
	docker run -d tonyzhang/phantasy-ioc:jessie
	caput fac 0.0
	sleep 2.0

clean:
	[ -e /tmp/phantasy_data ] && rm -rf /tmp/phantasy_data
