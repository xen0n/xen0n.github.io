all: pybble-build

pybble-build:
	@./pybblew build

templates:
	@rm -rf _templates static
	@cd _src && gulp

.PHONY: pybble-build templates
