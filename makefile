run:
	docker compose up --build api tempo grafana dcgm prometheus --remove-orphans

run-debug:
	docker compose up --build api-debug tempo grafana dcgm prometheus --remove-orphans

test:
	docker compose run --rm --build test

test-debug:
	docker compose up --build test-debug

test-cicd:
	@docker build -t knowitall-cicd-test -f docker/Dockerfile . && \
	docker run --rm -e DISABLE_TELEMETRY=True knowitall-cicd-test python -m unittest discover -s tests

clean:
	@docker system prune -a --force

setup:
	@echo "Setting up model download environment..."
	@mkdir -p models
	@chmod -R 777 models

	@echo "Building Docker image..."
	@docker build --build-arg UID=$$(id -u) --build-arg GID=$$(id -g) -t model-downloader -f docker/Dockerfile.setup . || \
		(echo "Error: Docker build failed"; exit 1)

	@echo "Running model download container..."
	@docker run --rm \
		-v $$(pwd)/models:/workspace/models \
		model-downloader python download_model.py || \
		(echo "Error: Model download failed"; exit 1)

	@echo "Setup complete. Check the 'models' directory for downloaded files."

# Run precommit on any staged files
precommit:
	@docker build --build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) -f docker/Dockerfile.precommit -t precommit . && \
	docker run --rm -v $(shell pwd):/workspace precommit bash -c "pre-commit run"

# Run precommit on the entire repository
precommit-all:
	@docker build --build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) -f docker/Dockerfile.precommit -t precommit-all . && \
	docker run --rm -v $(shell pwd):/workspace precommit-all bash -c "pre-commit run --all-files"

request:
	curl -X GET "http://localhost:8000/predict/?message=This%20is%20a%20test%20message"
