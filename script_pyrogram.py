import asyncio
import sys
import os

# Configurar event loop para Python 3.14
if sys.version_info >= (3, 14):
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
import requests

# Session string hardcodeado
SESSION_STRING = "BAG5gJ4ATkUghix_319Sqpd5L9bo3nUE0IHDUmyHFosZpmbqgxeixpvacVO1zz31pfjjCHFVZvAK_d9zoPlIc0CYU_IUUGR8gQDw9V21uIGCC7hfLNuBaFHkqccqC-VMbDO00I-1XSEH3jXqkP4uIUKndH_XGKGflprDpAoTBGQqr5JY9sLY3WoYVzVyO1at434IuaFy9aBMm6aXUiZbq4foG-l8gqJr0x4JvTDFGnrBqp8BnDtE9Sf68mTj2ZfGlJchKPut9vQwU9zExjHmhpAKRpMJdenlLZEyc9HIEk1p5CaK0HLmss4pJPUVONurImWTVQ-aKwt6R5xTFS8o3OqyXcCBgAAAAAAyiT0nAA"

# URL del webhook de n8n
N8N_WEBHOOK_URL = 'https://dani-n8n-n8n.yu6ww1.easypanel.host/webhook/f43f9869-cfdd-4e41-be6b-f7a361a581fd'

# IDs de los grupos/chats que quieres monitorizar (añade todos los IDs que necesites)
CHAT_ID_FILTERS = [-1003376832910, -1001872387914,1687976608 ]  # Lista de IDs de grupos a monitorizar

# Crear el cliente usando SESSION_STRING
app = Client("mi_sesion", session_string=SESSION_STRING)

@app.on_message()
async def handler(client, message):
    try:
        # Filtrar solo mensajes de los chats específicos
        if message.chat.id not in CHAT_ID_FILTERS:
            return  # Ignorar mensajes de otros chats
        
        # Obtener información del chat
        chat_name = "Desconocido"
        if message.chat.title:
            chat_name = message.chat.title
        elif message.chat.first_name:
            chat_name = message.chat.first_name
        
        # Obtener nombre del remitente
        sender_name = "Desconocido"
        if message.from_user:
            if message.from_user.username:
                sender_name = f"@{message.from_user.username}"
            elif message.from_user.first_name:
                sender_name = message.from_user.first_name
        
        # Obtener texto del mensaje
        texto = message.text if message.text else (message.caption if message.caption else "[Multimedia/Sin texto]")
        
        # Preparar datos para enviar al webhook
        payload = {
            "source": chat_name,
            "user": sender_name,
            "message": texto,
            "chat_id": message.chat.id,
            "date": str(message.date),
            "has_photo": False,
            "photo_file_id": None
        }
        
        # Si el mensaje tiene foto, añadir información
        if message.photo:
            payload["has_photo"] = True
            payload["photo_file_id"] = message.photo.file_id
            payload["photo_width"] = message.photo.width
            payload["photo_height"] = message.photo.height
            print(f"📸 Foto detectada: {message.photo.file_id}")
        
        # Enviar al webhook de n8n
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        print(f"✅ Mensaje enviado a n8n desde: {chat_name} - Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

print("🚀 Conectando a Telegram...")
print("📨 Mostrando todos los mensajes en tiempo real...\n")

# Iniciar el cliente
app.run()
