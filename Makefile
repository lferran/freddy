venv:
	python3.8 -m venv venv

pre-checks-deps: venv
	venv/bin/pip install flake8
	venv/bin/pip install black
	venv/bin/pip install isort
	venv/bin/pip install mypy

pre-checks: pre-checks-deps
	venv/bin/flake8 freddy --config=setup.cfg
	venv/bin/flake8 tests --config=setup.cfg
	venv/bin/mypy freddy --ignore-missing-imports
	venv/bin/mypy tests --ignore-missing-imports
	venv/bin/isort -c -rc freddy
	venv/bin/isort -c -rc tests
	venv/bin/black --check --verbose freddy
	venv/bin/black --check --verbose tests

develop: venv
	venv/bin/pip install -e .[test]
	venv/bin/pip install pre-commit
	venv/bin/pre-commit install

tests: venv develop
	venv/bin/pytest -rfE -s --tb=native -v tests/

package: venv
	venv/bin/python setup.py sdist
	venv/bin/pip install twine
	venv/bin/twine upload dist/*

clean:
	rm -rf venv
	rm -rf dist
	rm -rf *.egg-info

snippets: develop
	venv/bin/pip install ipython
	venv/bin/pip install aiohttp
	venv/bin/pip install pdbpp
