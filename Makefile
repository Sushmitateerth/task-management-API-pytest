build:
	docker build -t task-management-pytest .

run: build
	docker run task-management-pytest

.PHONY: build run