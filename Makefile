PACKAGE_PATH=medium_crosspost

define msg
    @printf "\033[36m# %s\033[0m\n" $(1)
endef

test:
	$(call msg,"Running tests")
	py.test $(PACKAGE_PATH)/

lint:
	$(call msg,"Running PyLint")
	find $(PACKAGE_PATH) -iname "*.py" | xargs pylint

code-coverage:
	$(call msg,"Running coverage.py")
	py.test --cov=$(PACKAGE_PATH) $(PACKAGE_PATH)/

travis-coverage:
	$(call msg,"Running coverage.py formatted for build")
	py.test --cov-report xml --cov=$(PACKAGE_PATH) $(PACKAGE_PATH)/ && cat coverage.xml

create-venv:
	$(call msg,"Creating a virtualenv for this project")
	virtualenv --python=/usr/bin/python3.7 venv
	venv/bin/pip3.7 install -r requirements.txt
	echo "$(shell pwd)/$(PACKAGE_PATH)" > venv/lib/python3.7/site-packages/$(PACKAGE_PATH).pth

publish:
	$(call msg,"Publishing to PyPI")
	rm dist/*.whl | true
	rm dist/*.tar.gz | true
	python setup.py sdist bdist_wheel
	twine upload dist/*
