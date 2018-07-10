PACKAGE_PATH=medium_crosspost

define msg
    @printf "\033[36m# %s\033[0m\n" $(1)
endef

test:  ## Run tests
	$(call msg,"Running tests")
	py.test $(PACKAGE_PATH)/

lint:  ## Run PyLint
	$(call msg,"Running PyLint")
	find $(PACKAGE_PATH) -iname "*.py" | xargs pylint

code-coverage: ## Run coverage.py
	$(call msg,"Running coverage.py")
	py.test --cov=$(PACKAGE_PATH) $(PACKAGE_PATH)/

travis-coverage: ## Run coverage.py formatted for build
	$(call msg,"Running coverage.py formatted for build")
	py.test --cov-report xml --cov=$(PACKAGE_PATH) $(PACKAGE_PATH)/ && cat coverage.xml

create-venv: ## Create a virtualenv for this project
	$(call msg,"Creating a virtualenv for this project")
	virtualenv --python=/usr/bin/python2.7 venv
	venv/bin/pip install -r requirements.txt
	echo "$(shell pwd)/$(PACKAGE_PATH)" > venv/lib/python2.7/site-packages/$(PACKAGE_PATH).pth
