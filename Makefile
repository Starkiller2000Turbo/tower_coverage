WORKDIR = scripts
PYTHON = python $(WORKDIR)

style:
	isort $(WORKDIR)
	black -S -l 79 $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)

pip:
	python -m pip install --upgrade pip

env:
	pip install isort
	pip install flake8
	pip install flake8-commas
	pip install flake8-quotes
	pip install flake8-docstrings
	pip install flake8-print
	pip install black
	pip install mypy

req_file:
	pip freeze -> requirements.txt

test:
	$(PYTHON)/tests.py

run:
	$(PYTHON)/main.py