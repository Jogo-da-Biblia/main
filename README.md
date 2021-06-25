### Realizando dump de banco de dados

```sh
# backup sqlite3
sqlite3 db.sqlite3 > dump.sql
# restore sqlite3
mv db.sqlite3 _db.sqlite3
sqlite3 db.sqlite3 < dump.sql
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
docker exec CONTAINER /usr/bin/mysqldump -u root --password=${DB_PASSWORD} django_cadastro_perguntas biblia_livro > biblia_livro.sql
# Restore
cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE
```
