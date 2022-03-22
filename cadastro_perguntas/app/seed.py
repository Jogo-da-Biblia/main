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
g_colaboradores.permissions.add(Permission.objects.get(codename='add_alternativa'))
g_colaboradores.permissions.add(Permission.objects.get(codename='add_referencia'))
g_colaboradores.permissions.add(Permission.objects.get(codename='view_pergunta'))
g_colaboradores.permissions.add(p_can_create_alternativa)
g_colaboradores.permissions.add(p_can_create_referencia)
# Associando usuários aos grupos
g_colaboradores.user_set.add(colaborador)

# Criando temas/grupos de perguntas
from app.perguntas.models import Tema
Tema(nome="Doutrina", cor="a163e8").save()
Tema(nome="Referencia", cor="f99e00").save()
Tema(nome="Personagens do Antigo Testamento", cor="5ade3c").save()
Tema(nome="Personagens do Novo Testamento", cor="2cd0de").save()
Tema(nome="Conhecimentos Gerais", cor="de5353").save()
Tema(nome="Especial", cor="ffffff").save()
Tema(nome="Números", cor="9e8e34").save()
Tema(nome="Perguntas Ouro", cor="e7d50f").save()