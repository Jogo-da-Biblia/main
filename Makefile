reset_all:
	sudo find . -path “*/migrations/*.py” -not -name “__init__.py” -delete
	sudo find . -path “*/migrations/*.pyc” -delete	
	echo "Removendo histórico de migrations"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py showmigrations"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate --fake core zero"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate --fake biblia zero"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate --fake perguntas zero"
	echo "Criando migrations core..."
	docker-compose down --volumes --remove-orphans
	sudo rm -rf data
	docker-compose build --no-cache
	docker-compose up -d 
	echo "Esperando subir banco de dados..."
	sleep 30
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations core"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations biblia"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations perguntas"
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate --fake-initial"
reset:
	docker-compose down --volumes --remove-orphans
	sudo rm -rf data
	docker-compose build
run: 
	docker-compose down
	docker-compose up -d 
migrate:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate"		
superuser:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py createsuperuser"