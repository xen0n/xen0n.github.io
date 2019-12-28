all: pybble-build

pybble-build:
	@./_generator/venv/bin/python3 ./pybblew build

templates:
	@rm -rf _templates static/css
	@cd _src && ./node_modules/.bin/gulp

.PHONY: pybble-build templates
