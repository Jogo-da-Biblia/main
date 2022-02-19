### Rodando a aplicação pela primeira vez

Execute:
```sh
# Se você quiser restaurar as configurações iniciais do projeto para rodar novamente como se fosse a primeira vez
make reset
# É bom aguardar depois de executar `make_run` para dar tempo de o banco de dados subir
make run
# Instale as aplicações e migrations, se der erro da primeira vez ([Errno 111] Connection refused)"), execute novamente
make migrate
# Popule o banco de dados
docker exec -it jogodabiblia_db bash
cat /initial_data/*.sql | mysql -u root -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE}
# Crie um superusuário
make superuser
# Depois de popular o banco ele pode cair
make run
```

### Inicializando migrações

```sh
docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations"
docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate"
```
### Criando superusuário

```sh
docker exec -it jogodabiblia_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py createsuperuser"
```

### Backup and Restore some table
```sh
# Backup
DB_TABLE=biblia_livro sh dump_table.sh
# Restore
cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE
```

## Known Issues

- "Can't connect to MySQL server on 'db' ([Errno 111] Connection refused)") | Execute novamente `make run`

## To watch/compile sass

```sh
python manage.py sass app/perguntas/static/scss/ app/perguntas/static/css/ --watch
python manage.py sass app/perguntas/static/scss/ app/perguntas/static/css/ -t compressed
```