# All maintained papers share one build recipe; historical figures remain committed.
PAPERS := $(patsubst %/paper.tex,%,$(wildcard */paper.tex))
PYTHON ?= python3
LATEXMK ?= latexmk
.DEFAULT_GOAL := all

all: $(PAPERS)

$(PAPERS):
	cd "$@" && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error paper.tex

check:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'
	$(PYTHON) -m compileall -q .

clean:
	@for paper in $(PAPERS); do \
		(cd "$$paper" && $(LATEXMK) -c paper.tex && rm -f build.log) || exit; \
	done

.PHONY: all check clean $(PAPERS)
