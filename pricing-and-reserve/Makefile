paper.pdf: paper.tex references.bib $(wildcard figures/*.tex) $(wildcard data/*)
	latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex

clean:
	latexmk -c paper.tex
	rm -f build.log

.PHONY: clean
