GRAPHS_DIR = graphs/
GRAPHS_OBJECTS = $(wildcard $(GRAPHS_DIR)*.dot)



.PHONY: graphs test clean $(GRAPHS_OBJECTS)


$(GRAPHS_OBJECTS:.dot=.pdf): %.pdf : %.dot
	dot $< -Tpdf -o $@

graphs: $(GRAPHS_OBJECTS:.dot=.pdf)


test: 
	python src/learning.py

clean:
	rm -rf src/*.pyc graphs/*

$(patsubst %.c,%.o,$(wildcard *.c))
