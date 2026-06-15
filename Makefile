PYTHON ?= python3
VENV   := .venv
PY     := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip pytest

.PHONY: validate
validate: ## Lint every SKILL.md (frontmatter, size, paths)
	$(PYTHON) scripts/validate_skill.py skills/*

.PHONY: build
build: $(VENV) ## Install each skill's requirements.txt
	@for req in skills/*/requirements.txt; do \
		[ -f "$$req" ] && echo "Installing $$req" && $(PIP) install -r "$$req"; \
	done; true

.PHONY: test
test: validate build ## Run all tests
	$(PY) -m pytest tests/ skills/*/tests/ -q

.PHONY: new
new: ## Scaffold a new skill: make new name=my-skill kind=text|template|script
	$(PYTHON) scripts/new_skill.py $(name) --kind $(or $(kind),text)

.PHONY: install
install: ## Symlink skills/* into ./.cursor/skills/
	$(PYTHON) scripts/sync_skills.py

.PHONY: clean
clean: ## Remove venv and caches
	rm -rf $(VENV) .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
