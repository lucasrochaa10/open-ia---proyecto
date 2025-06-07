from openai import OpenAI
import json
from dotenv import load_dotenv
import requests

load_dotenv()

# Inicializar el cliente
client = OpenAI()

# Definir el mensaje inicial
input_messages = [
    {"role": "user", "content": "What is the weather like in Paris today?"}]

# Definir la herramienta/función get_weather
tools = [{
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
}]

# Paso 1: Llamar al modelo con la función definida
response = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools
)

# Imprimir la salida inicial
print("Respuesta inicial del modelo:")
print(response.output)

# Función real para obtener el tiempo en una localidad usando la API de Open-Meteo


def get_weather(latitude, longitude):
    """Obtiene la temperatura actual usando la API de Open-Meteo"""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    temp_c = data['current']['temperature_2m']
    temp_f = (temp_c * 9/5) + 32
    return f"The current temperature is {temp_c}°C ({temp_f:.1f}°F)"


# Paso 3: Ejecutar el código de la función
# Procesar las llamadas a funciones en la respuesta
for tool_call in response.output:
    if tool_call.type == "function_call":
        # Parsear los argumentos
        args = json.loads(tool_call.arguments)

        # Ejecutar la función
        result = get_weather(args["latitude"], args["longitude"])

        # Agregar la llamada a función a los mensajes
        input_messages.append(tool_call)

        # Agregar el resultado de la función
        input_messages.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(result)
        })

# Paso 4: Enviar los resultados de vuelta al modelo
response_2 = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools
)

# Paso 5: El modelo responde incorporando el resultado
print("\nRespuesta final del modelo:")
print(response_2.output_text)
