env:
	python3 -m venv env
	source env/bin/activate
deps:
	python3 -m pip install --upgrade pip setuptools wheel
dev:
	pip install -r dev-requirements.txt 
get_credentials:
	python3 get_creds.py 
setup:
	python3 setup.py install
precommit:
	pre-commit run --all-files
