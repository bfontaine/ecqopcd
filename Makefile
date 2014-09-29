# ECQPCD Makefile

.DEFAULT: all
.PHONY: all stylecheck deploy populate run

SRC=ecqopcd
VENV=venv

all: stylecheck deploy

deploy: stylecheck
	git push heroku master

deps: venv
	venv/bin/pip install -qr requirements.txt

venv:
	virtualenv venv

run:
	CLOSURE_COMPRESSOR_OPTIMIZATION=ADVANCED_OPTIMIZATIONS \
	$(VENV)/bin/gunicorn app:app

populate:
	$(VENV)/bin/python scheduler.py

stylecheck:
	pep8 $(SRC) app.py
