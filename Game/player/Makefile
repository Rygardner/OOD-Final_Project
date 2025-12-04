INTERPRETER = python
TYPE = mypy
STYLE = flake8
FIX_STYLE = autopep8
TEST = pytest
DOCS = docs
ASSIGNMENTS = 

.PHONY: all
all: check-type fix-style check-style run-test run-kat-test clean
	@echo "All done..."

.PHONY: check-type
check-type:
	@echo "Checking type using mypy..."
	$(TYPE) --strict --allow-untyped-decorators --ignore-missing-imports .

.PHONY: check-style
check-style:
	@echo "Checking style..."
	$(STYLE) .

.PHONY: fix-style
fix-style:
	@echo "Fixing style..."
	$(FIX_STYLE) -r --in-place --aggressive .

.PHONY: clean
clean:
	rm -rf 'find . -type d -name __pycache__'

.PHONY: create-doc-folder
create-doc-folder:
	@mkdir -p $(DOCS) 

.PHONY: run-test
run-test:
	@echo "Running $(TEST)..."
	$(TEST) --verbose --color=yes tests/

.PHONY: run-kat-test
run-kat-test:
	@echo "Running kattis test..."
	kattis test

.PHONY: run-all-tests
run-all-tests: run-test run-kat-test
	@echo "Running pytest, coverage test, and Kattis tests"
	
.PHONY: run-test-coverage
run-test-coverage:
	pytest --verbose --cov=. --cov-report=term-missing tests/
	@echo "Running pytest coverage...."

.PHONY: create-pdoc
create-pdoc:
	pdoc $(ASSIGNMENTS) -o docs