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
migrate:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate"		
makemigrations:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations core"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations biblia"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations perguntas"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate"		
seed:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py shell < seed.py"		
superuser:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py createsuperuser"