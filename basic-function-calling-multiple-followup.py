from openai import OpenAI
import json
from dotenv import load_dotenv
import requests

load_dotenv()

# Inicializar el cliente
client = OpenAI()

# Definir el mensaje inicial que requiere múltiples funciones
input_messages = [{
    "role": "user",
    "content": "What's the weather in Paris and Bogotá? Also send an email to bob@email.com with the results."
}]

# Definir múltiples herramientas
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude coordinate (e.g. 48.8566 for Paris)"
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude coordinate (e.g. 2.3522 for Paris)"
                }
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "send_email",
        "description": "Send an email to a recipient with weather information",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Email address of the recipient"
                },
                "subject": {
                    "type": "string",
                    "description": "Subject of the email"
                },
                "body": {
                    "type": "string",
                    "description": "Body of the email with weather information"
                }
            },
            "required": ["to", "subject", "body"],
            "additionalProperties": False
        }
    }
]

# Paso 1: Llamar al modelo con las funciones definidas
response = client.responses.create(
    model="gpt-4o-mini",
    input=input_messages,
    tools=tools
)

# Imprimir la salida inicial
print("Respuesta inicial del modelo:")
print(response.output)

# Función real para obtener el clima usando la API de Open-Meteo


def get_weather(latitude, longitude):
    """Obtiene la temperatura actual usando la API de Open-Meteo"""
    try:
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )
        data = response.json()
        temp_c = data['current']['temperature_2m']
        temp_f = (temp_c * 9/5) + 32
        return f"Temperature: {temp_c}°C ({temp_f:.1f}°F)"
    except Exception as e:
        return f"Error getting weather: {str(e)}"

# Función simulada para enviar email


def send_email(to, subject, body):
    """Simula el envío de un email"""
    # En una aplicación real, aquí se implementaría el envío real del email
    print(f"Email sent to {to}\nSubject: {subject}\nBody: {body}")
    return f"Email sent to {to}\nSubject: {subject}\nBody: {body}"

# Función para manejar las llamadas a funciones


def call_function(name, args):
    """Procesa una llamada a función y retorna su resultado"""
    if name == "get_weather":
        return get_weather(**args)
    elif name == "send_email":
        return send_email(**args)
    else:
        return f"Error: Function {name} not implemented"


# Paso 2: Procesar las llamadas a funciones y obtener respuesta final
while True:
    # Procesar las llamadas a funciones en la respuesta actual
    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue

        name = tool_call.name
        args = json.loads(tool_call.arguments)

        # Ejecutar la función y obtener el resultado
        result = call_function(name, args)

        # Agregar la llamada a función y su resultado a los mensajes
        input_messages.append(tool_call)
        input_messages.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(result)
        })

    # Obtener nueva respuesta del modelo
    response = client.responses.create(
        model="gpt-4o-mini",
        input=input_messages,
        tools=tools
    )

    # Si no hay más llamadas a funciones, salir del bucle
    if not response.output or all(call.type != "function_call" for call in response.output):
        break

# La última respuesta contiene el texto final del modelo
print("\nRespuesta final del modelo:")
print(response.output_text)

# Guardar el ID de la respuesta para mantener el contexto
previous_response_id = response.id

# Paso 5: Pregunta de seguimiento para probar la memoria del modelo
follow_up_message = [{
    "role": "user",
    "content": "Do you remember what was the current temperature in Paris?"
}]

print("\nPregunta de seguimiento:")
print(follow_up_message[0]["content"])

# Llamar al modelo con el contexto anterior
response_follow_up = client.responses.create(
    model="gpt-4o-mini",
    input=follow_up_message,
    tools=tools,
    previous_response_id=previous_response_id
)

print("\nRespuesta del modelo (con memoria):")
print(response_follow_up.output_text)
