from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search_preview"}],
    input="¿Qué canciones ha estrenado Matt Berninger recientemente?"
)

print(response.output_text)