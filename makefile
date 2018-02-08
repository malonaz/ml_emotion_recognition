

#### FOR GRAPHS 

GRAPHS_DIR = graphs/
GRAPHS_OBJECTS = graphs/clean_dataset/emotion1.dot graphs/clean_dataset/emotion2.dot graphs/clean_dataset/emotion3.dot \
		 graphs/clean_dataset/emotion4.dot graphs/clean_dataset/emotion5.dot graphs/clean_dataset/emotion6.dot \
		 graphs/noisy_dataset/emotion1.dot graphs/noisy_dataset/emotion2.dot graphs/noisy_dataset/emotion3.dot \
		 graphs/noisy_dataset/emotion4.dot graphs/noisy_dataset/emotion5.dot graphs/noisy_dataset/emotion6.dot


$(GRAPHS_OBJECTS):
	mkdir -p graphs/clean_dataset
	mkdir -p graphs/noisy_dataset
	mkdir -p output/clean_dataset
	mkdir -p output/noisy_dataset
	python src/main.py

$(GRAPHS_OBJECTS:.dot=.pdf): %.pdf : %.dot
	dot $< -Tpdf -o $@

graphs:  $(GRAPHS_OBJECTS:.dot=.pdf)

### REPORT

REPORT_OBJECTS = report.aux report.log report.out
REPORT_SRC = report/implementation.tex report/ambiguity.tex report/evaluation.tex

report: report/report.pdf


report/report.pdf: $(GRAPHS_OBJECTS:.dot=.pdf) report/report.tex $(REPORT_SRC)
	pdflatex report/report.tex
	rm -rf $(REPORT_OBJECTS)
	mv report.pdf report



### PHONY

.PHONY: graphs test clean report


clean:
	rm -rf src/*.pyc graphs/* output/* $(REPORT_OBJECTS)

