# Sistema de Cadastro de Perguntas - Jogo da Bíblia

Jogo da Bíblia é um jogo híbrido, ou seja, é um jogo físico de tabuleiro de perguntas e respostas onde o usuário anda certo número de casas de acordo com o acerto da resposta obtida de cada, porém as cartas do jogo são digitais, então funciona assim:

1. Tem um tabuleiro com casas coloridas e um QR code
2. Ao scanear o QR code o usuário tem acesso à tela do sistema onde é possível selecionar uma cor de cartas que apresentará a carta da pergunta a ser respondida

O cadastro de perguntas será colaborativo e pessoas interessadas em produzir perguntas poderão fazê-lo e serão avaliadas pela equipe revisora, por isso os colaboradores só poderão ter acesso à página estilizada de cadastro de perguntas enquanto os revisores poderão fazer alteração nas perguntas e os publicadores, tanto editar quanto publicar as perguntas, tornando-as públicas para uso final dos jogadores.

## Inicializando

Você precisa ter o `docker` e o `docker-compose` instalado em sua máquina. para isso verifique os links de documentação prorietária: [Docker](https://docs.docker.com/engine/install/) e [Docker-compose](https://docs.docker.com/compose/install/), nessa ordem.

Primeiramente leia a [seção de arquivos .env](env) para setar as variáveis de ambiente como senhas de banco de dados. Para instalar todos os pacotes e dependências rode:

```
make build
```

Ou, se estiver usando o windows abra o arquivo `Makefile` e execute linha por linha do bloco `build`. Para saber mais [leia](makefile).

Acesse http://localhost:A_PORTA_QUE_VOCE_COLOCOU_EM_ENV e verá seu serviço rodando. Mágica? Não. Docker. 😉

**Atenção** Se não aparecer o site pode ser porque, a primeira vez que é gerado o banco de dados ele demora para inicializar, dessa forma o django tenta conectar com o banco e não consegue, gerando erro. Verifique o `log` no terminal para ter certeza, mas se for esse o caso, execute:

```bash
make run
```

## Arquivos

<a id="env"></a>

### .env e .env.example

São arquivos que guardam variáveis de ambiente, são geralmente dados que precisam de uma segurança maior e não podem ficar expostos no github, por isso sempre o `.env` fica no `.gitignore` e uma versão sem os dados fica disponível em `.env.example`. Você deve então copiar os dados de `.env.example` para `.env` e colocar os dados. Para isso use o comando abaixo:

```bash
cp .env.example .env
```

<a id="makefile"></a>

### Makefile

Só funciona em linux, é útil para executar blocos de códigos juntos, sem precisar digitar um por um na linhas de comandos, então colocamos grupos de comandos que são utilizados comumente juntos, para usar digite `make` e o nome do bloco, por exemplo:

```bash
make init
```

### Para ambiente de testes

Execute para resetar sem formatar o banco de dados:

```sh
# Se você quiser restaurar as configurações iniciais do projeto para rodar novamente como se fosse a primeira vez
make reset
# É bom aguardar depois de executar `make_run` para dar tempo de o banco de dados subir
make run
# Instale as aplicações e migrations, se der erro da primeira vez ([Errno 111] Connection refused)"), execute novamente
make migrate
# Popule o banco de dados
make seed
# Crie um superusuário
make superuser
# Depois de popular o banco ele pode cair
make run
```

Formatando o banco de dados e reiniciando o sistema para fins de produção em ambiente de desenvolvimento:

```sh
make reset_all
make makemigrations
make run
make seed
make superuser
make run
```

### Inicializando migrações

```sh
docker exec -it catekel_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py makemigrations"
docker exec -it catekel_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py migrate"
```

### Criando superusuário

```sh
docker exec -it catekel_cadastro_perguntas bash -c "cd /usr/src/app/app && python manage.py createsuperuser"
```

### Restaurando tabela postgres

```sh
psql -U postgres -f /initial_data/biblia_psql.sql
```

### Backup and Restore some table

**!! Deprecated !!**
```sh
# Backup
DB_TABLE=biblia_livro sh dump_table.sh
# Restore
cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE
```

## Run Tests
```sh
docker exec -it catekel_cadastro_perguntas bash -c "cd /usr/src/app/app && pytest app/graphql/tests.py"
```
or just
```
make test
```

## Known Issues

- "Can't connect to MySQL server on 'db' ([Errno 111] Connection refused)") | Execute novamente `make run`

## To watch/compile sass

```sh
make sass
python manage.py sass app/perguntas/static/scss/ app/perguntas/static/css/ -t compressed
```

## Automatizando criação de perfis/grupos e permissões

Os comando automatizados estão listados em `app/seed.py` e são executados junto com o bloco de comandos `make seed`

## Criando tradução para português do painel administrativo

```bash
docker exec -it catekel_cadastro_perguntas bash -c "django-admin makemessages --locale=pt_BR"
```
