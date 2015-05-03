all: pybble-build

pybble-build:
	@./pybblew

templates:
	@rm -rf _templates static
	@cd _src && gulp

.PHONY: pybble-buildd templates
