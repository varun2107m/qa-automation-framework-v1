# =========================
# QA Automation Framework
# =========================

.PHONY: test report clean install

# Run tests
test:
	pytest -v --alluredir=reports/allure-results

test-smoke:
	pytest -v -m smoke --alluredir=reports/allure-results	

# Serve Allure report
report:
	allure serve reports/allure-results

# Clean reports
clean:
	rm -rf reports/allure-results

# Install dependencies
install:
	pip install -r requirements.txt
