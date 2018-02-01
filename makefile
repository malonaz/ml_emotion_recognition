

#### FOR GRAPHS 

GRAPHS_DIR = graphs/
GRAPHS_OBJECTS = graphs/emotion1.dot graphs/emotion2.dot graphs/emotion3.dot graphs/emotion4.dot graphs/emotion5.dot graphs/emotion6.dot


$(GRAPHS_OBJECTS):
	mkdir -p graphs
	python src/main.py

$(GRAPHS_OBJECTS:.dot=.pdf): %.pdf : %.dot
	dot $< -Tpdf -o $@

graphs:  $(GRAPHS_OBJECTS:.dot=.pdf)



### PHONY

.PHONY: graphs test clean 


clean:
	rm -rf src/*.pyc graphs/*

