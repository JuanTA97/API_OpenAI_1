import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar .env
load_dotenv()


# Leer claves de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

if not openai_api_key:
    raise RuntimeError(
        "Falta OPENAI_API_KEY. Asegúrate de tenerla en tu .env y haber llamado load_dotenv()."
    )

# Crear cliente
client = OpenAI(api_key=openai_api_key)

def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente de IA útil y conciso."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
        )

        # Validar estructura
        if not response.choices:
            raise RuntimeError("La respuesta no trae 'choices'. Reintenta la petición.")

        msg = response.choices[0].message
        content = getattr(msg, "content", None)
        if not content:
            raise RuntimeError("La respuesta llegó sin 'content'.")

        return content

    except Exception as e:
        raise RuntimeError(f"Fallo al consultar el modelo '{MODEL}': {e}") from e

# Prueba
if __name__ == "__main__":
    try:
        texto = get_llm_response("""Actúa como un community manager especializado en marketing musical y redes sociales.
                                    Genera 3 ideas creativas de publicaciones para Instagram enfocadas en una banda/solista de rock.
                                    Cada idea debe incluir:

                                    Formato sugerido (ejemplo: reel, carrusel, foto, historia).

                                    Concepto principal.

                                    Texto breve o copy atractivo.

                                    Hashtags recomendados.
                                    Sé concreto, profesional y enfocado en captar la atención de un público amante del rock."""
                                 )
        
        print("\n=== Respuesta del modelo ===\n")
        print(texto)
    except Exception as err:
        print(f"ERROR: {err}")