# All maintained papers share one build recipe; historical figures remain committed.
PAPERS := $(patsubst %/Makefile,%,$(wildcard */Makefile))
PYTHON ?= python3
.DEFAULT_GOAL := all

all: $(PAPERS)

$(PAPERS):
	$(MAKE) -C $@

check:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'
	$(PYTHON) -m compileall -q .

clean:
	@for paper in $(PAPERS); do $(MAKE) -C "$$paper" clean || exit; done

.PHONY: all check clean $(PAPERS)
