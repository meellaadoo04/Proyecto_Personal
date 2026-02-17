import asyncio
import sys

# Configurar event loop para Python 3.14
if sys.version_info >= (3, 14):
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
import requests

# Tus credenciales de https://my.telegram.org
API_ID = '28934302'
API_HASH = '86672ce87514ee8a08f154d26bf99098'
PHONE_NUMBER = '+34608136144'

# URL del webhook de n8n
N8N_WEBHOOK_URL = 'https://dani-n8n-n8n.yu6ww1.easypanel.host/webhook/f43f9869-cfdd-4e41-be6b-f7a361a581fd'

# IDs de los grupos/chats que quieres monitorizar (añade todos los IDs que necesites)
CHAT_ID_FILTERS = [-1003376832910, -1001872387914]  # Lista de IDs de grupos a monitorizar

# Crear el cliente de Pyrogram
app = Client("mi_sesion", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

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
        texto = message.text if message.text else "[Multimedia/Sin texto]"
        
        # Preparar datos para enviar al webhook
        payload = {
            "source": chat_name,
            "user": sender_name,
            "message": texto,
            "chat_id": message.chat.id,
            "date": str(message.date)
        }
        
        # Enviar al webhook de n8n
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        print(f"✅ Mensaje enviado a n8n desde: {chat_name} - Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

print("🚀 Conectando a Telegram...")
print("📨 Mostrando todos los mensajes en tiempo real...\n")

# Iniciar el cliente
app.run()
