# Makefile

PYTHON := python3
MAIN := game.py
TEST := player/player_demo.py

.PHONY: run test clean

run:
	$(PYTHON) $(MAIN)

test:
	$(PYTHON) $(TEST)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
