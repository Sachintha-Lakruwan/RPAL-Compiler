# runs the RPAL processor with the specified file
run:
	python myrpal.py $(file)

# print tokens
tokens:
	python myrpal.py $(file) -tokens

# print the AST
ast:
	python myrpal.py $(file) -ast

# print the standardized AST
sast:
	python myrpal.py $(file) -sast

# print control structures
cs:
	python myrpal.py $(file) -cs

# Remove virtual environment and cache files to start fresh
clean:
	rm -rf __pycache__ *.pyc

# avoid conflicts with files named 'run', 'ast', or 'sast'
.PHONY: run ast sast cs tokens
