import uuid
import json
from datetime import datetime
from google.cloud import bigquery
from pydantic import BaseModel
from typing import Dict, Any, List, Literal, Optional
import io

from conversation import ConversationRepository
from message import MessageRepository
from user import UserRepository
from pathlib import Path
from chat.memory import MessageContent, MessagesContentTypeAdapter


# Asegúrate de que todas tus clases de repositorio y modelos (UserModel, ConversationModel, etc.)
# estén definidas o importadas aquí.

# --- Inicio del script de pruebas ---

if __name__ == "__main__":
    # Reemplaza estos valores con la información de tu proyecto de Google Cloud
    PROJECT_ID = "adept-storm-467519-j4"
    DATASET_ID = "reto_winter_equipo1"

    # Inicializa el cliente y los repositorios
    try:
        client = bigquery.Client(project=PROJECT_ID)
        user_repo = UserRepository(client, PROJECT_ID, DATASET_ID)
        conv_repo = ConversationRepository(client, PROJECT_ID, DATASET_ID)
        msg_repo = MessageRepository(client, PROJECT_ID, DATASET_ID)
    except Exception as e:
        print(f"❌ Error al inicializar los repositorios: {e}")
        exit()

    # Variables para almacenar los IDs generados
    test_user_id = None
    test_conversation_id = None
    test_message_id = None

    print("--- 🧪 Iniciando pruebas simples de creación y lectura 🧪 ---")

    # 1. Prueba de usuario
    """print("\n[INFO] Creando un nuevo usuario...")
    test_user_id = user_repo.create()
    if test_user_id:
        print(f"✅ Usuario creado con ID: {test_user_id}")
        user = user_repo.read(test_user_id)
        print(f"✅ Usuario leído: {user}")"""


    # 2. Prueba de conversación
    #if test_user_id:
        #print("\n[INFO] Creando una nueva conversación...")
    ##test_conversation_id = conv_repo.create('462637fb-5735-4d75-a5f5-86f1c3205cbe')
    ##if test_conversation_id:
        ##print(f"✅ Conversación creada con ID: {test_conversation_id}")
    conversation = conv_repo.read('70ad1e70-7c51-4fcb-9adb-6cfcf2f3ed48')
    print(f"✅ Conversación leída: {conversation}")


    """ path = Path(__file__).parent / "../../test_values/values.json"
    read_json = path.read_text()
    print(read_json)



   # 3. Prueba de mensaje
    if test_conversation_id:
        print("\n[INFO] Creando un nuevo mensaje...")
        message_content = MessagesContentTypeAdapter.validate_json(read_json)
        test_message_id = msg_repo.create(test_conversation_id,'user', message_content)
        if test_message_id:
            print(f"✅ Mensaje creado con ID: {test_message_id}")
            message = msg_repo.read(test_message_id)
            print(f"✅ Mensaje leído: {message}")

    print("\n--- ✅ Pruebas completadas. ---")"""