
import uuid
import json
from datetime import datetime, date
from google.cloud import bigquery
from pydantic import BaseModel
from typing import Dict, Any, List, Literal, Optional
import io

from conversation import ConversationRepository
from message import MessageRepository
from form import FormRepository
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

    try:
        # Inicializa el cliente y el repositorio
        client = bigquery.Client(project=PROJECT_ID)
        ithaka_repo = FormRepository(client, PROJECT_ID, DATASET_ID)
    except Exception as e:
        print(f"❌ Error al inicializar el cliente de BigQuery: {e}")
        exit()

    print("--- 🧪 Iniciando prueba de creación y lectura de formulario 🧪 ---")

    # Define los datos de un formulario de prueba
    test_form_data = {
        "message_id": str(uuid.uuid4()),
        "name": "Prueba de Integración 3",
        "first_question": "Comité de evaluación",
        "date_of_completion": date.today(),
        "evaluators": ("José Alonso", "Martín Abreu"),
        "idea": "Plataforma de IA para el análisis de mercado",
        "sponsor": "Florencia Clemente",
        "ucu_community_members": ("Egresado/a", "Docente"),
        "linked_faculty": ("FIT", "UCU BUSINESS"),
        "stage": ("Ideación", "NULL"),
        "profile_type": ["ANII (Disrupción y escala)", "Impacto Social"],
        "potential_support": ["Mentoria/Tutoría (elegir de la lista a continuación)", "Club de beneficios"],
        "specific_mentor": ["Luis Silveira"],
        "follow_up_personnel": ("José Alonso",  "NULL"),
        "internal_comments": "Excelente potencial para el mercado uruguayo.",
        "message_for_applicant": "Felicidades, tu idea ha sido seleccionada para la siguiente etapa.",
    }

    # 1. Prueba de creación
    print("\n[INFO] Creando un nuevo formulario de evaluación...")
    try:
        form_id = ithaka_repo.create(**test_form_data)
        print(f"✅ Formulario creado con éxito. ID: {form_id}")
    except Exception as e:
        print(f"❌ Error al crear el formulario: {e}")
        form_id = None

    # 2. Prueba de lectura
    if form_id:
        print("\n[INFO] Leyendo el formulario recién creado...")
        try:
            read_form = ithaka_repo.read("Prueba de Integración 3")
            if read_form:
                print(f"✅ Formulario leído con éxito.")
                print(f"  - Nombre del formulario: {read_form.name}")
                print(f"  - Idea: {read_form.idea}")
                print(f"  - Mensaje para el postulante: {read_form.message_for_applicant}")
            else:
                print(f"❌ Error: No se encontró el formulario con ID {form_id}")
        except Exception as e:
            print(f"❌ Error al leer el formulario: {e}")
    else:
        print("\n[INFO] Se saltó la prueba de lectura debido a un fallo en la creación.")

    print("\n--- ✅ Pruebas completadas. ---")
