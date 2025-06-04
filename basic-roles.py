from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-nano",
    input=[
        {
            "role": "developer",
            "content": "Habla como un pirata."
        },
        {
            "role": "user",
            "content": "¿Son los puntos y comas opcionales en JavaScript?"
        }
    ]
)

print(response.output_text)
