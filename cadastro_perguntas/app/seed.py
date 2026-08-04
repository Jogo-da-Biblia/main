# Adicionando usuários de teste
from app.perguntas.models import Tema
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


User = get_user_model()

def get_or_create_user(username, password, **defaults):
    user, _ = User.objects.update_or_create(username=username, defaults=defaults)
    user.set_password(password)
    user.save()
    return user


def get_permissions(*codenames):
    return list(Permission.objects.filter(codename__in=codenames))


def upsert_tema(nome, cor):
    tema = Tema.objects.filter(nome=nome).first()
    if tema is None:
        Tema.objects.create(nome=nome, cor=cor)
        return

    tema.cor = cor
    tema.save(update_fields=["cor"])


print("Criando usuários...")
try:
    print("Adicionado colaborador de teste...")
    colaborador = get_or_create_user(
        username="colaborador",
        password="passw@rd",
        defaults={
            "name": "Colaborador de Teste",
            "email": "colaborador@jogodabiblia.com.br",
            "phone": "71992540736",
            "is_whatsapp": True,
        },
    )
except Exception as e:
    print(e)

try:
    print("Adicionado revisor de teste...")
    revisor = get_or_create_user(
        username="revisor",
        password="passw@rd",
        defaults={
            "name": "Revisor de Teste",
            "email": "revisor@teste.com",
            "phone": "71992540737",
            "is_whatsapp": True,
        },
    )
except Exception as e:
    print(e)

print("Adicionado publicador de teste...")
try:
    publicador = get_or_create_user(
        username="publicador",
        password="passw@rd",
        defaults={
            "name": "Publicador de Teste",
            "email": "publicador@teste.com",
            "phone": "71992540738",
            "is_whatsapp": True,
        },
    )
except Exception as e:
    print(e)

print("Adicionado supervisor de teste...")
try:
    supervisor = get_or_create_user(
        username="supervisor",
        password="passw@rd",
        defaults={
            "name": "Supervisor de Teste",
            "email": "supervisor@teste.com",
            "phone": "71992540739",
            "is_whatsapp": True,
        },
    )
except Exception as e:
    print(e)

print("Adicionado administrador de teste...")
try:
    administrador = get_or_create_user(
        username="administrador",
        password="passw@rd",
        defaults={
            "name": "Administrador de Teste",
            "email": "administrador@teste.com",
            "phone": "71992540740",
            "is_whatsapp": True,
        },
    )
except Exception as e:
    print(e)

print("Adicionando grupos...")
try:
    g_colaboradores, created = Group.objects.get_or_create(name='colaboradores')
    g_revisores, created = Group.objects.get_or_create(name='revisores')
    g_publicadores, created = Group.objects.get_or_create(name='publicadores')
    g_supervisores, created = Group.objects.get_or_create(name='supervisores')
    g_administradores, created = Group.objects.get_or_create(name='administradores')
except Exception as e:
    print(e)

print("Adicionando permissões...")
try:
    perguntas_perms = get_permissions(
        'add_pergunta',
        'view_pergunta',
        'change_pergunta',
        'delete_pergunta',
    )

    comentarios_perms = get_permissions(
        'add_comentario',
        'view_comentario',
        'change_comentario',
        'delete_comentario',
    )

    alternativas_perms = get_permissions(
        'add_alternativa',
        'view_alternativa',
        'change_alternativa',
        'delete_alternativa',
    )

    all_perms = Permission.objects.all()
except Exception as e:
    print(e)

print("Adicionando usuários aos grupos de permissões...")
try:
    # Colaboradores
    g_colaboradores.permissions.add(
        *comentarios_perms,
        *perguntas_perms,
        *alternativas_perms
    )

    # Revisores
    g_revisores.permissions.add(
        *comentarios_perms,
        *perguntas_perms,
        *alternativas_perms
    )

    # Publicadores
    g_publicadores.permissions.add(
        *comentarios_perms,
        *perguntas_perms,
        *alternativas_perms
    )

    # Supervisores
    g_supervisores.permissions.add(*all_perms)

    # Administradores
    g_administradores.permissions.add(*all_perms)

    # Associando usuários aos grupos
    g_colaboradores.user_set.add(colaborador)
    g_revisores.user_set.add(revisor)
    g_publicadores.user_set.add(publicador)
    g_supervisores.user_set.add(supervisor)
    g_administradores.user_set.add(administrador)
except Exception as e:
    print(e)

print("Adicionando temas de perguntas...")
try:
    upsert_tema(nome="Doutrina", cor="a163e8")
    upsert_tema(nome="Referencia", cor="f99e00")
    upsert_tema(nome="Personagens do Antigo Testamento", cor="5ade3c")
    upsert_tema(nome="Personagens do Novo Testamento", cor="2cd0de")
    upsert_tema(nome="Conhecimentos Gerais", cor="de5353")
    upsert_tema(nome="Especial", cor="ffffff")
    upsert_tema(nome="Números", cor="9e8e34")
    upsert_tema(nome="Perguntas Ouro", cor="e7d50f")
except Exception as e:
    print(e)
