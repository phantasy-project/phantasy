.PHONY: test clean

test:
	PYTHONPATH=../ \
	nosetests3 --with-coverage --cover-package=phantasy \
		--with-id -v --logging-level=INFO \
		--exclude-dir-file="skiptests"

test-py2:
	PYTHONPATH=../ \
	nosetests \
		--with-coverage --cover-package=phantasy \
		--with-id -v --logging-level=INFO \
		--exclude-dir-file="skiptests" 

ioc:
	docker run -d --name phantasy-ioc tonyzhang/phantasy-ioc:jessie
	sleep 2.0
	caput fac 0.0
	sleep 2.0

kill-ioc:
	docker container stop phantasy-ioc
	docker container rm phantasy-ioc

clean:
	[ -e /tmp/phantasy_data ] && rm -rf /tmp/phantasy_data
