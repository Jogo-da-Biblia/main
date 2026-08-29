from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import transaction

from app.perguntas.models import Tema


User = get_user_model()

USERS = (
    ("colaborador", "Colaborador de Teste", "colaborador@jogodabiblia.com.br", "71992540736", "colaboradores"),
    ("revisor", "Revisor de Teste", "revisor@teste.com", "71992540737", "revisores"),
    ("publicador", "Publicador de Teste", "publicador@teste.com", "71992540738", "publicadores"),
    ("supervisor", "Supervisor de Teste", "supervisor@teste.com", "71992540739", "supervisores"),
    ("administrador", "Administrador de Teste", "administrador@teste.com", "71992540740", "administradores"),
)

EDITOR_PERMISSION_CODENAMES = (
    "add_pergunta",
    "view_pergunta",
    "change_pergunta",
    "delete_pergunta",
    "add_comentario",
    "view_comentario",
    "change_comentario",
    "delete_comentario",
    "add_alternativa",
    "view_alternativa",
    "change_alternativa",
    "delete_alternativa",
)

TEMAS = (
    ("Doutrina", "a163e8"),
    ("Referencia", "f99e00"),
    ("Personagens do Antigo Testamento", "5ade3c"),
    ("Personagens do Novo Testamento", "2cd0de"),
    ("Conhecimentos Gerais", "de5353"),
    ("Especial", "ffffff"),
    ("Números", "9e8e34"),
    ("Perguntas Ouro", "e7d50f"),
)


with transaction.atomic():
    groups = {
        name: Group.objects.get_or_create(name=name)[0]
        for name in (
            "colaboradores",
            "revisores",
            "publicadores",
            "supervisores",
            "administradores",
        )
    }

    editor_permissions = Permission.objects.filter(
        codename__in=EDITOR_PERMISSION_CODENAMES
    )
    all_permissions = Permission.objects.all()

    for group_name in ("colaboradores", "revisores", "publicadores"):
        groups[group_name].permissions.set(editor_permissions)
    for group_name in ("supervisores", "administradores"):
        groups[group_name].permissions.set(all_permissions)

    for username, name, email, phone, group_name in USERS:
        user, _ = User.objects.update_or_create(
            username=username,
            defaults={
                "name": name,
                "email": email,
                "phone": phone,
                "is_whatsapp": True,
            },
        )
        user.set_password("passw@rd")
        user.save(update_fields=["password"])
        user.groups.set([groups[group_name]])

    for nome, cor in TEMAS:
        Tema.objects.update_or_create(nome=nome, defaults={"cor": cor})

print(f"Seed concluído: {len(USERS)} usuários e {len(TEMAS)} temas.")
