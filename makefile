# Python et venv
PYTHON := python3
VENV_NAME := .venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
PIP := $(VENV_NAME)/bin/pip

# Cible par défaut
all: fmt

# Créer l'environnement virtuel
venv:
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Virtual environment created. Activate it with: source $(VENV_ACTIVATE)"

# Installer les dépendances essentielles et pre-commit
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r py_packages.txt
	$(PIP) install pre-commit
	pre-commit install
	@echo "Dependencies installed and pre-commit hooks configured."

# Formater le code et appliquer les checks
fmt:
	pre-commit run --all-files
	@echo "Formatting and checks complete!"

# Lancer uniquement les checks sans modifier le code
check:
	pre-commit run --all-files --hook-stage manual
	@echo "Checks complete!"

# Nettoyer fichiers compilés et caches Python
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete
	rm -rf .mypy_cache .pytest_cache .coverage *.egg-info

# Aide
help:
	@echo "Available targets:"
	@echo "  all       : Format code and run checks (default)"
	@echo "  venv      : Create virtual environment"
	@echo "  install   : Install pre-commit hooks"
	@echo "  fmt       : Format code and run checks"
	@echo "  check     : Run checks without modifying files"
	@echo "  clean     : Remove Python artifacts"
	@echo "  help      : Show this help message"
