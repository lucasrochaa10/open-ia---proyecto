from openai import OpenAI
import json
from dotenv import load_dotenv

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
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country e.g. Bogotá, Colombia"
            }
        },
        "required": ["location"],
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

# Output esperado:
# [{
#     "type": "function_call",
#     "id": "fc_12345xyz",
#     "call_id": "call_12345xyz",
#     "name": "get_weather",
#     "arguments": "{\"location\":\"Paris, France\"}"
# }]


def get_weather(location):
    """Función simulada para obtener el clima de una ubicación"""
    # En una aplicación real, aquí harías una llamada a una API del clima
    weather_data = {
        "Paris, France": {"temperature": 14, "conditions": "cloudy"},
        "Bogotá, Colombia": {"temperature": 18, "conditions": "rainy"},
        "Tokyo, Japan": {"temperature": 10, "conditions": "sunny"}
    }

    if location in weather_data:
        temp = weather_data[location]["temperature"]
        temp_f = (temp * 9/5) + 32
        return f"The current temperature is {temp}°C ({temp_f:.1f}°F)"
    else:
        return f"Weather data not available for {location}"


# Paso 3: Ejecutar el código de la función
# Procesar las llamadas a funciones en la respuesta
for tool_call in response.output:
    if tool_call.type == "function_call":
        # Parsear los argumentos
        args = json.loads(tool_call.arguments)

        # Ejecutar la función
        result = get_weather(args["location"])

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
