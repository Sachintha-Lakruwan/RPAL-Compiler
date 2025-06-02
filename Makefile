# runs the RPAL processor with the specified file
run:
	python3 myrpal.py $(file)

# print the AST
ast:
	python3 myrpal.py $(file) -ast

# print the standardized AST
sast:
	python3 myrpal.py $(file) -sast

# Remove virtual environment and cache files to start fresh
clean:
	rm -rf __pycache__ *.pyc

# avoid conflicts with files named 'run', 'ast', or 'sast'
.PHONY: run ast sast
