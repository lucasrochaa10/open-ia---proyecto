from openai import OpenAI

client = OpenAI()

response = client.responses.create(
  model="gpt-4o-mini",
  input="Cuéntame en tres líneas un cuento de un unicornio."

)

print(response.output_text)