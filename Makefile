.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 djangocms_installer

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source djangocms-installer setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/djangocms_installer.*.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ djangocms_installer
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

release: clean
	python setup.py clean --all sdist bdist_wheel
	twine upload dist/*

sdist: clean
	python setup.py sdist
	ls -l dist
