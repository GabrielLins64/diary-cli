# Makefile for Diary-CLI

PYTHON = python3
PIP = python3 -m pip
PYINSTALLER = pyinstaller
INSTALL_DIR = /usr/local/bin
EXECUTABLE = dist/main

VENV_DIR = venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate

.PHONY: install build clean

# Buildando e instalando globalmente o executável
install: $(VENV_ACTIVATE) build
	@echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	@echo Atenção!
	@echo O instalador irá precisar de permissão de administrador
	@echo Para tornar o programa executável de qualquer localização.
	@sudo cp $(EXECUTABLE) $(INSTALL_DIR)/diarycli
	@echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	@echo "Diary-CLI foi instalado com sucesso."

# Criando o executável
build: $(VENV_ACTIVATE)
	@. $(VENV_ACTIVATE) && $(PIP) install -r requirements.txt
	@. $(VENV_ACTIVATE) && $(PYINSTALLER) --onefile main.py

# Limpeza de diretórios de builds e cache
clean:
	@rm -rf build dist venv __pycache__

# Criar um ambiente virtual
$(VENV_ACTIVATE):
	@$(PYTHON) -m venv $(VENV_DIR)
