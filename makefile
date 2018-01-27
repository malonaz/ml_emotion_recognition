




.PHONY: test clean

graph:
	dot graph.dot -Tpdf -o graph.pdf

test:
	python assignment1.py


clean:
	rm *.pyc *.pdf *.dot
