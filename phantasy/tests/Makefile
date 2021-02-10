.PHONY: test clean ioc kill-ioc

PYTHON_EXECUTABLE ?= $$(which python)

test:
	# pip install pytest pytest-cov
	PYTHONPATH=../ \
	python3 -m "pytest" -v \
	 --cov-report term-missing --cov=phantasy

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
