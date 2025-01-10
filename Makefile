.PHONY: install test lint format generate-proto clean-proto

install:
	pip install -e ".[dev]"

test:
	pytest

test-quiet:
	pytest --disable-warnings -q

lint:
	mypy epistemic_me tests
	black --check epistemic_me tests
	isort --check-only epistemic_me tests

format:
	black epistemic_me tests
	isort epistemic_me tests

clean-proto:
	rm -rf epistemic_me/generated/proto

generate-proto: clean-proto
	pip install grpcio-tools
	cd $(CURDIR) && python generate_proto.py

all: generate-proto install test
