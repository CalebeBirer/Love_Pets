from rolepermissions.roles import AbstractUserRole

class Owner(AbstractUserRole):
    available_permissions = {
        'cadastrar_pet': True,
        'liberar_descontos': True,
        'cadastrar_vendedor': True,
    }

class Client(AbstractUserRole):
    available_permissions = {
        'realizar_venda': True,
    }