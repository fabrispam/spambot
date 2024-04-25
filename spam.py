from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.errors import SessionPasswordNeededError
from datetime import datetime, timedelta
from time import sleep
from telethon.tl import types
from telethon.errors import FloodWaitError, ChatAdminRequiredError

api_id = '24780324'  
api_hash = '04b4e92dcbec796e5bb1145e65a43d54'  

grupo_origen_id = -1002013263674 #<----AQUI EL GRUPO  DE ORIGEN 

tu_numero_telefono = '+51934242950

def iniciar_sesion():
    client = TelegramClient('session_name', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        try:
            client.send_code_request(tu_numero_telefono)
            client.sign_in(tu_numero_telefono, input('Ingresa el código que has recibido: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Ingresa la contraseña de la cuenta: '))
    return client

def enviar_mensaje(client):
    try:
        print("\033[92m\u0062\u0079 \u0040\u0066\u0061\u006e\u0074\u0061\u0073\u006d\u0069\u006e\u0078\u0078\033[0m")
        sleep(3)  # Esperar 5 segundos
        print("\033[A                             \033[A")  
    except Exception as ex:
        print(f"ERROR AL REENVIAR EL MENSAJE {ex}")

def reenviar_mensajes(client):
    errores_impresos = set()  # Conjunto para almacenar errores ya impresos

    try:
        print("Obteniendo mensajes...")
        messages = client.iter_messages(grupo_origen_id)

        chats = client.get_dialogs()
        for message in messages:
            if isinstance(message, types.MessageService):
                continue
            for chat in chats:
                if chat.is_group and chat.id != grupo_origen_id:
                    try:
                        client.forward_messages(chat.id, messages=message)
                        print(f"Mensaje reenviado al grupo {chat.title}: {message.id}")
                    except Exception as e:
                        error_str = str(e)
                        if error_str not in errores_impresos:
                            print(f"Error al reenviar mensaje al grupo {chat.title}: {error_str}")
                            errores_impresos.add(error_str)
            sleep(1)  # Esperar 1 segundo después de enviar cada mensaje

    except Exception as ex:
        print(f"Error general: {ex}")

if __name__ == "__main__":
    client = iniciar_sesion()
    enviar_mensaje(client)
    
    while True:
        try:
            reenviar_mensajes(client)
            print("Esperar 10 minutos para reenviar mensajes nuevamente.")
            sleep(600)  # Esperar 15 minutos (900 segundos) antes de volver a reenviar mensajes
        except Exception as ex:
            print(f"Error general: {ex}")
