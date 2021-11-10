.PHONY: test clean ioc kill-ioc

PYTHON_EXECUTABLE ?= $$(which python)
IOC_NAME := "phantasy-ioc"

test:
	# pip install pytest pytest-cov
	PYTHONPATH=../ \
	python3 -m "pytest" -v \
	 --cov-report term-missing --cov=phantasy

ioc: kill-ioc
	docker run -d --rm --name $(IOC_NAME) tonyzhang/phantasy-ioc:jessie
	sleep 2.0
	caput fac 0.0
	sleep 2.0

kill-ioc:
	docker container inspect $(IOC_NAME) > /dev/null 2>&1 && \
		docker container stop $(IOC_NAME) || [ $$? -eq 1 ]

clean:
	[ -e /tmp/phantasy_data ] && rm -rf /tmp/phantasy_data || [ $$? -eq 1 ]
