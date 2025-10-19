# Docker Compose configuration
COMPOSE_FILE=docker-compose.yml
COMPOSE=docker compose

# Image names (defined in docker-compose.yml)
IMAGE=netserf/rabbitmq:latest
PRODUCER_IMAGE=netserf/mqtt-producer:latest
CONSUMER_IMAGE=netserf/mqtt-consumer:latest

# Container names (defined in docker-compose.yml)
SERVER=rabbitmq-server
PRODUCER=mqtt-producer
CONSUMER=mqtt-consumer

.PHONY: help
help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

.PHONY: build
build: ## Build all container images
	$(COMPOSE) -f $(COMPOSE_FILE) build

.PHONY: up
up: ## Start all containers in detached mode
	$(COMPOSE) -f $(COMPOSE_FILE) up -d
	@echo "RabbitMQ MQTT environment is running"
	@echo "Management UI: http://localhost:15672 (admin/YodaSaysUseStrongPwd9!)"

.PHONY: down
down: ## Stop and remove all containers and networks
	$(COMPOSE) -f $(COMPOSE_FILE) down

.PHONY: ps
ps: ## List running containers
	$(COMPOSE) -f $(COMPOSE_FILE) ps

.PHONY: logs
logs: ## Show logs from all containers (follow mode)
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f

.PHONY: logs-server
logs-server: ## Show logs from RabbitMQ server
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f $(SERVER)

.PHONY: logs-producer
logs-producer: ## Show logs from MQTT producer
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f $(PRODUCER)

.PHONY: logs-consumer
logs-consumer: ## Show logs from MQTT consumer
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f $(CONSUMER)

.PHONY: exec-server
exec-server: ## Open shell in RabbitMQ server container
	$(COMPOSE) -f $(COMPOSE_FILE) exec $(SERVER) /bin/bash

.PHONY: exec-producer
exec-producer: ## Open shell in producer container
	$(COMPOSE) -f $(COMPOSE_FILE) exec $(PRODUCER) /bin/bash

.PHONY: exec-consumer
exec-consumer: ## Open shell in consumer container
	$(COMPOSE) -f $(COMPOSE_FILE) exec $(CONSUMER) /bin/bash

.PHONY: restart
restart: ## Restart all containers
	$(COMPOSE) -f $(COMPOSE_FILE) restart

.PHONY: restart-server
restart-server: ## Restart RabbitMQ server only
	$(COMPOSE) -f $(COMPOSE_FILE) restart $(SERVER)

.PHONY: restart-producer
restart-producer: ## Restart producer only
	$(COMPOSE) -f $(COMPOSE_FILE) restart $(PRODUCER)

.PHONY: restart-consumer
restart-consumer: ## Restart consumer only
	$(COMPOSE) -f $(COMPOSE_FILE) restart $(CONSUMER)

.PHONY: ui
ui: ## Open RabbitMQ Management UI in browser
	@echo "Opening RabbitMQ Management UI..."
	@echo "URL: http://localhost:15672"
	@echo "Username: admin"
	@echo "Password: YodaSaysUseStrongPwd9!"
	xdg-open http://localhost:15672 2>/dev/null || open http://localhost:15672 2>/dev/null || echo "Please open http://localhost:15672 in your browser"

.PHONY: clean
clean: down ## Stop containers and remove images
	-docker rmi $(IMAGE) 2>/dev/null || true
	-docker rmi $(PRODUCER_IMAGE) 2>/dev/null || true
	-docker rmi $(CONSUMER_IMAGE) 2>/dev/null || true
