
build:
	docker-compose -f local.yml build

start:
	docker-compose -f local.yml up

runserver:
	docker-compose -f local.yml run --service-ports django

migrations:
	docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate

superuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

shell:
	docker-compose -f local.yml run --rm django python manage.py shell_plus

test:
	docker-compose -f local.yml run --rm django py.test --ds=config.settings.test -s -v -x --ff $${TEST_ARGS}

black:
	docker-compose -f local.yml run --rm django black .

lint:
	docker-compose -f local.yml run --rm django flake8 .

isort:
	docker-compose -f local.yml run --rm django isort -y

drop-db:
	docker-compose -f local.yml down --volumes


wakeup-database:
	docker-compose -f local.yml up -d postgres
	@echo "==="
	@echo "Sleeping for a few seconds to make sure the database wakes up!"
	@echo "==="
	sleep 3s

docker-clean-containers: ## Remove all docker containers
	@echo Removing all containers
	-docker ps -aq | xargs docker rm -f

docker-clean-images: ## Remove all docker images
	@echo Removing old images
	-docker images -q -f="dangling=true" | xargs docker rmi

docker-clean: docker-clean-containers docker-clean-images

docker-clean-all-images: ## Remove all docker images
	@echo Removing old images
	-docker images -q | xargs docker rmi --force