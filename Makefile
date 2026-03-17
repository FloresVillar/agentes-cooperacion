COMPOSE=docker-compose
APP_CONTAINER=agentes-python
OLLAMA_CONTAINER=ollama-sever
MODELO=llama3.2:1b
SERVICE?=app
.PHONY: build run down logs shell-app limpieza ayuda
DOCKER:=docker

ayuda:
	@echo ""
	@echo "comandos"
	@echo "make build -- construccion de imagenes"
	@echo "make run   -- levanta sistema instala modelo"
	@echo "make down  --apaga contenedores"
	@echo "make logs  --muestra logs"
	@echo "make shell-app  -- terminal de app"
	@echo "make limpieza  --borra imagenes"

build-service:
	docker compose up -d --build $(SERVICE)
limpieza-service:
	docker compose stop $(SERVICE)
	docker compose rm -f $(SERVICE) 
	docker rmi agentes-cooperacion-app
shell-app:
	docker exec -it $(APP_CONTAINER) /bin/bash
logs:
	$(COMPOSE) logs -f
logs-service:
	docker logs $(SERVICE)
