reset:
	docker-compose down --volumes --remove-orphans
	sudo rm -rf data
run: 
	docker-compose down
	docker-compose up -d 
migrate:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate"		
superuser:
	docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py createsuperuser"