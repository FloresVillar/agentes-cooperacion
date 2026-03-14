import os
from openai import OpenAI

cliente = OpenAI(api_key = "ollama",
                 base_url = os.getenv("OLLAMA_HOST","http://localhost:11434") + "/v1")


def llamada_a_modelo(historial,prompt_sistema):
    mensajes = [{"role": "system", "content": prompt_sistema}] + historial
    respuesta = cliente.chat.completions.create(
        model=""
    )