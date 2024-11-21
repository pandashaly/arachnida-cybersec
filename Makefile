PY = python3
RECS = requirements.txt
SPIDER = spider.py
SCORPION = scorpion.py
VENV = source env/bin/activate

all: install make_exec

venv:
	@echo "Setting up virtual environment..."
	$(PY) -m venv env

install: venv
	@echo "Installing python packages..."
	env/bin/pip install --upgrade pip
	. env/bin/activate && pip install -r $(RECS)

make_exec:
	@echo "Making Executables..."
	chmod +x $(SPIDER)
	chmod +x $(SCORPION)

clean:
	@echo "Cleaning up previous python virtual environment"
	rm -rf env
