# 🚀 Desplegar en EasyPanel

EasyPanel es perfecto para tu caso ya que ya tienes experiencia con él (mencionaste tu n8n ahí).

---

## 📋 PARTE 1: Preparar el proyecto

### 1. Crear archivo Dockerfile

Crea un archivo llamado `Dockerfile` en tu carpeta:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY script_pyrogram.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando de inicio
CMD ["python", "script_pyrogram.py"]
```

### 2. Subir a GitHub
Si aún no lo has hecho:
```bash
git add Dockerfile
git commit -m "Add Dockerfile for EasyPanel"
git push
```

---

## 📋 PARTE 2: Desplegar en EasyPanel

### 1. Acceder a tu EasyPanel
Ve a tu panel de EasyPanel (donde tienes n8n)

### 2. Crear nuevo servicio
1. Click en **"Create"** o **"New App"**
2. Selecciona **"From GitHub"** o **"Git Repository"**
3. Conecta tu repositorio de GitHub

### 3. Configurar el servicio

**Tipo de servicio:**
- Selecciona: **"App"** o **"Service"**

**Build settings:**
- **Build method**: Docker (detectará automáticamente tu Dockerfile)
- O si tiene la opción **"Nixpacks"**, también funcionará

**Resources:**
- CPU: 0.5 (mínimo)
- RAM: 512 MB (suficiente para el bot)

### 4. Variables de entorno (MUY IMPORTANTE)

Añade estas variables en la sección **"Environment Variables"**:

```
SESSION_STRING=BAG5gJ4ATkUghix_319Sqpd5L9bo3nUE0IHDUmyHFosZpmbqgxeixpvacVO1zz31pfjjCHFVZvAK_d9zoPlIc0CYU_IUUGR8gQDw9V21uIGCC7hfLNuBaFHkqccqC-VMbDO00I-1XSEH3jXqkP4uIUKndH_XGKGflprDpAoTBGQqr5JY9sLY3WoYVzVyO1at434IuaFy9aBMm6aXUiZbq4foG-l8gqJr0x4JvTDFGnrBqp8BnDtE9Sf68mTj2ZfGlJchKPut9vQwU9zExjHmhpAKRpMJdenlLZEyc9HIEk1p5CaK0HLmss4pJPUVONurImWTVQ-aKwt6R5xTFS8o3OqyXcCBgAAAAAAyiT0nAA
```

### 5. Deploy
Click en **"Deploy"** o **"Create"**

---

## 📋 PARTE 3: Modificar el script (IMPORTANTE)

Antes de desplegar, necesitas modificar `script_pyrogram.py` para usar el SESSION_STRING:

### Versión modificada del script:

```python
import asyncio
import sys
import os

# Configurar event loop para Python 3.14
if sys.version_info >= (3, 14):
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
import requests

# Obtener SESSION_STRING de variables de entorno
SESSION_STRING = os.getenv('SESSION_STRING')

if not SESSION_STRING:
    raise ValueError("❌ SESSION_STRING no está configurado en las variables de entorno")

# URL del webhook de n8n
N8N_WEBHOOK_URL = 'https://dani-n8n-n8n.yu6ww1.easypanel.host/webhook/f43f9869-cfdd-4e41-be6b-f7a361a581fd'

# IDs de los grupos/chats que quieres monitorizar
CHAT_ID_FILTERS = [-1003376832910, -1001872387914]

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
print("📨 Escuchando mensajes...\n")

# Iniciar el cliente
app.run()
```

---

## 📋 PARTE 4: Monitoreo en EasyPanel

### Ver logs:
1. En EasyPanel, ve a tu app
2. Click en **"Logs"** o **"Console"**
3. Verás los mensajes del bot en tiempo real

### Reiniciar el servicio:
1. Click en **"Restart"** si necesitas reiniciarlo

---

## ✅ Ventajas de EasyPanel

✅ Ya tienes experiencia con él (tu n8n está ahí)
✅ Interfaz simple y visual
✅ Logs fáciles de ver
✅ Mismo servidor que n8n (baja latencia)
✅ Deploy automático desde GitHub

---

## 📝 Checklist antes de desplegar:

- [ ] Archivo `Dockerfile` creado
- [ ] Script modificado para usar `SESSION_STRING`
- [ ] Todo subido a GitHub
- [ ] Variable `SESSION_STRING` añadida en EasyPanel
- [ ] Deploy iniciado

---

## 🆘 Solución de problemas

### Si el bot no inicia:
1. Ve a los **logs** en EasyPanel
2. Verifica que `SESSION_STRING` esté configurado correctamente
3. Asegúrate que el Dockerfile esté en la raíz del repo

### Si no recibe mensajes:
1. Verifica que los `CHAT_ID_FILTERS` sean correctos
2. Comprueba los logs para ver si hay errores de conexión

---

## 💰 Costo

Depende de tu plan de EasyPanel, pero como es self-hosted o en tu servidor:
- Si tienes servidor propio: **GRATIS**
- Si usas EasyPanel Cloud: Consulta sus precios

Es probable que ya tengas recursos si tienes n8n corriendo ahí.
