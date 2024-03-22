# Define the default target
.DEFAULT_GOAL := help
docker-build
	docker-compose -f local.yml build

docker-prod-build:
	docker-compose -f prod.yml build

docker-local:
	docker-compose -f local.yml up -d

docker-prod:
	docker-compose -f prod.yml up -d

# Show help message
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo "  run          Run the Django development server"
	@echo "  run-asgi     Run the Django application with Uvicorn ASGI server"
	@echo "  help         Show this help message"
