from google.cloud import storage, bigquery
from vertexai.language_models import TextEmbeddingModel
from unstructured.partition.auto import partition
from ..env import env


def get_clients():
    """Get Google Cloud clients."""
    return (
        storage.Client(),
        bigquery.Client(),
        TextEmbeddingModel.from_pretrained("textembedding-gecko")
    )


def document_processing() -> None:
    """Process documents and generate embeddings."""
    storage_client, bq_client, embedding_model = get_clients()
    
    # Usar variables de entorno
    project_id = env().project_id
    bucket_name = env().bucket_name
    dataset = env().dataset
    table = env().table
    
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix="documentos/")
    
    rows_to_insert = []

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        print(f"Procesando {blob.name}...")

        local_path = f"/tmp/{blob.name.split('/')[-1]}"
        blob.download_to_filename(local_path)

        # Extraer texto
        elements = partition(filename=local_path)
        texto = "\n".join([el.text for el in elements if el.text])

        # Dividir en fragmentos
        chunks = [texto[i:i+1000] for i in range(0, len(texto), 1000)]

        for chunk in chunks:
            embedding = embedding_model.get_embeddings([chunk])[0].values

            rows_to_insert.append({
                "doc_id": blob.name,
                "fragmento": chunk,
                "embedding": embedding
            })

    # Insertar en BigQuery
    errors = bq_client.insert_rows_json(f"{project_id}.{dataset}.{table}", rows_to_insert)
    if errors:
        print("Errores al insertar:", errors)
    else:
        print("Embeddings insertados correctamente en BigQuery.")