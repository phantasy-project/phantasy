.PHONY: test clean

PYTHON_EXECUTABLE ?= $$(which python)

pytest:
	# pip install pytest pytest-cov
	PYTHONPATH=../ \
	python3 -m "pytest" -v
	# --cov-report term-missing --cov=phantasy

test:
	PYTHONPATH=../ \
	$(PYTHON_EXECUTABLE) -m "nose.core" .

test-py3:
	PYTHONPATH=../ \
	nosetests3 --with-coverage --cover-package=phantasy \
		-v --logging-level=INFO
		# --with-id
		# --exclude-dir-file="skiptests"

test-py2:
	PYTHONPATH=../ \
	nosetests \
		--with-coverage --cover-package=phantasy \
		-v --logging-level=INFO
		# --with-id
		# --exclude-dir-file="skiptests"

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
