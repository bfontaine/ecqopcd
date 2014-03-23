# ECQPCD Makefile

.DEFAULT: all
.PHONY: all stylecheck deploy populate run

SRC=ecqopcd
INITSHELL=source venv/bin/activate

all: stylecheck deploy

deploy:
	git push

populate:
	$(INITSHELL); \
	python scheduler.py

run:
	$(INITSHELL); \
	CLOSURE_COMPRESSOR_OPTIMIZATION=ADVANCED_OPTIMIZATIONS \
	gunicorn app:app

stylecheck:
	pep8 $(SRC) app.py
