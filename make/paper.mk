# Shared PDF recipe. Each paper includes this file from its own directory.
.DEFAULT_GOAL := paper.pdf
LATEXMK ?= latexmk

paper.pdf: paper.tex references.bib $(wildcard figures/*.tex) $(wildcard data/*) ../make/paper.mk
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error paper.tex

clean:
	$(LATEXMK) -c paper.tex
	rm -f build.log

.PHONY: clean
