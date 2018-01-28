.PHONY: test clean


graph:
	dot graphs/graph.dot -Tpdf -o graphs/graph.pdf

test:
	python src/learning.py


clean:
	rm -rf src/*.pyc graphs/*
