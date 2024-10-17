reset_all:
	sudo find . -path "./cadastro_perguntas/app/app/*/migrations/*.py" -not -name "__init__.py" -delete
	sudo find . -path "./cadastro_perguntas/app/app/*/migrations/*.pyc" -delete	
	echo "Criando migrations core..."
	docker-compose down --volumes --remove-orphans
	sudo rm -rf data
	docker-compose build --no-cache
	docker-compose up -d 
reset:
	docker-compose down --volumes --remove-orphans
	sudo rm -rf data
	docker-compose build
run: 
	docker-compose down
	docker-compose up -d
build:
	docker-compose build --no-cache
	make run
migrate:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate"
makemigrations:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations"		
seed:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py shell < seed.py"		
	echo "Restaurando banco com sqls da pasta initial_data"
	docker compose exec -it app bash -c "psql -U postgres -d jogodabiblia -f /initial_data/biblia_psql.sql"
superuser:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py createsuperuser"
logs:
	docker-compose logs -f
db_terminal:
	docker exec -it jogodabiblia_db bash
sass:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py sass /usr/src/app/app/static/scss/ /usr/src/app/app/static/css/ --watch"
test:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && pytest -vv ./app/tests/"