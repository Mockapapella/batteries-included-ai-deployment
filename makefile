run:
	docker compose up --build api tempo grafana dcgm prometheus --remove-orphans

run-debug:
	docker compose up --build api-debug tempo grafana dcgm prometheus --remove-orphans

test:
	docker compose run --rm --build test

test-debug:
	docker compose up --build test-debug

test-cicd:
	docker compose run --rm --build test-cicd

# Cleans up all unused images
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
	curl -X GET "http://localhost:8000/generate/?prompt=Once%20upon%20a%20time%20in%20a%20galaxy%20far,%20far%20away&max_length=100"
