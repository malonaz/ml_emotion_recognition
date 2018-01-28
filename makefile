.PHONY: graphs test clean


graphs:
	dot graphs/emotion1.dot -Tpdf -o graphs/emotion1.pdf
	dot graphs/emotion2.dot -Tpdf -o graphs/emotion2.pdf
	dot graphs/emotion3.dot -Tpdf -o graphs/emotion3.pdf
	dot graphs/emotion4.dot -Tpdf -o graphs/emotion4.pdf
	dot graphs/emotion5.dot -Tpdf -o graphs/emotion5.pdf
	dot graphs/emotion6.dot -Tpdf -o graphs/emotion6.pdf

test:
	python src/learning.py


clean:
	rm -rf src/*.pyc graphs/*
