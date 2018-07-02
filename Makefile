
define msg
    @printf "\033[36m# %s\033[0m\n" $(1)
endef

test:  ## Run tests
	$(call msg,"Running tests")
	py.test src/

lint:  ## Run PyLint
	$(call msg,"Running PyLint")
	find src -iname "*.py" | xargs pylint
