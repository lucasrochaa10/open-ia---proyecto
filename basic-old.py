from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[{"role": "user", "content": "Cuéntame un haiku"}]
            )

print(response)
print(response.choices[0].message.content)