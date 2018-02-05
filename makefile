

#### FOR GRAPHS 

GRAPHS_DIR = graphs/
GRAPHS_OBJECTS = graphs/emotion1.dot graphs/emotion2.dot graphs/emotion3.dot graphs/emotion4.dot graphs/emotion5.dot graphs/emotion6.dot


$(GRAPHS_OBJECTS):
	mkdir -p graphs
	mkdir -p output
	python src/main.py

$(GRAPHS_OBJECTS:.dot=.pdf): %.pdf : %.dot
	dot $< -Tpdf -o $@

graphs:  $(GRAPHS_OBJECTS:.dot=.pdf)


#### REPORT

report:
	mkdir -p report
	make report/report.pdf
	clear

report/report.pdf: src/report.tex
	pdflatex $<
	mv report.pdf report/report.pdf
	rm -rf report.*

### PHONY

.PHONY: graphs test clean report


clean:
	rm -rf src/*.pyc graphs/* output/*.txt report/*

