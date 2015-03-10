#
# Execute the test modules for RfDataUtils.
#

export PYTHONPATH=$(realpath ..)

.PHONY: test
test: fmdata t7data lrfdata


.PHONY: fmdata
fmdata:
	python fmdata_test.py


.PHONY: t7data
t7data:
	python t7data_test.py


.PHONY: lrfdata
lrfdata:
	python lrfdata_test.py

.PHONY: nrfdata
nrfdata:
	python nrfdata_test.py
