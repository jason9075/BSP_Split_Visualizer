DEFAULT_GOAL:=help


.PHONY: run
run:
	python main.py

.PHONY: dev
dev:
	@fd . | entr -r sh -c 'python main.py'


.PHONY: clean
clean:
	echo "Cleaning up..."

.PHONY: help
help:
	@echo "Makefile for local development"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
