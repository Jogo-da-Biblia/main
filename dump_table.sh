if [ -f .env ]
then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

docker exec jogodabiblia_db /usr/bin/mysqldump -u root --password=${DB_ROOT_PASSWORD} django_cadastro_perguntas ${DB_TABLE} > "initial_data/${DB_TABLE}.sql"