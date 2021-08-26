build: 
	@echo 'Buinding container...'
	@docker build -t $(APP_NAME) .

run: 
	@echo 'Run container...'
	@docker run --detach -p 5000:5000 --env-file=$(ENV_FILE) $(APP_NAME)

start:
	@echo 'Starting container...'
	@docker ps -a | grep $(APP_NAME) | awk '{print $$1}' | xargs docker start

stop:
	@echo 'Stopping container...'
	@docker ps | grep $(APP_NAME) | awk '{print $$1}' | xargs docker stop

kill:
	@echo 'Killing container...'
	@docker ps | grep $(APP_NAME) | awk '{print $$1}' | xargs docker rm -f

clean:
	@echo 'Killing (eventually) dead container(s)...'
	@docker ps -a | grep $(APP_NAME) | awk '{print $$1}' | xargs -r docker rm -f
	@echo 'Removing container image...'
	@docker images | grep $(APP_NAME) | awk '{print $$3}' | xargs docker rmi
