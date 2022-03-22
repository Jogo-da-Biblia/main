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
# Crie um superusuário
make seed
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

## Códigos temporários para criação de usuários com permissões predefinidas de exemplo

```bash
docker exec -it jogodabiblia_cadastro_perguntas bash
cd app && python manage.py shell
```

```python
# Adicionando usuários de teste
from django.contrib.auth import get_user_model
User = get_user_model()
User(username="colaborador", name="Colaborador de Teste", email="colaborador@jogodabiblia.com.br", phone="71992540736", is_whatsapp=True, is_staff=True).save()
colaborador = User.objects.get(username="colaborador")
colaborador.set_password("passw@rd")
# Criando grupos e permissões
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.perguntas.models import Pergunta, Alternativa, Referencia
# Criando os grupos
g_colaboradores, created = Group.objects.get_or_create(name='colaboradores')
g_revisores, created = Group.objects.get_or_create(name='revisores')
g_publicadores, created = Group.objects.get_or_create(name='publicadores')
# Capturando o conteúdo dos models para associar às permissões
ct_pergunta = ContentType.objects.get_for_model(Pergunta)
ct_alternativa = ContentType.objects.get_for_model(Alternativa)
ct_referencia = ContentType.objects.get_for_model(Referencia)
# Criando as permissões
p_can_create_pergunta = Permission.objects.create(codename='can_create_pergunta', name='Pode criar uma pergunta', content_type=ct_pergunta)
p_can_create_alternativa = Permission.objects.create(codename='can_create_alternativa', name='Pode criar uma alternativa',content_type=ct_alternativa)
p_can_create_referencia = Permission.objects.create(codename='can_create_referencia', name='Pode criar uma referência', content_type=ct_referencia)
# Associando grupos às permissões
g_colaboradores.permissions.add(p_can_create_pergunta)
g_colaboradores.permissions.add(Permission.objects.get(codename='add_pergunta'))
g_colaboradores.permissions.add(p_can_create_alternativa)
g_colaboradores.permissions.add(p_can_create_referencia)
# Associando usuários aos grupos
g_colaboradores.user_set.add(colaborador)
# ... agora em seed.py
```

```python
# Checando permissões
all_permissions = Permission.objects.all()
for permission in all_permissions:
    print(permission.__dict__)
```

## Criando tradução para português do painel administrativo

```bash
docker exec -it jogodabiblia_cadastro_perguntas bash -c "django-admin makemessages --locale=pt_BR"
```