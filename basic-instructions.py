from openai import OpenAI

client = OpenAI()

response = client.responses.create(
  model="gpt-4o-mini",
  instructions="Answer in Spanish.",
  input="Tell me a bedtime story about a unicorn in three lines."

)

print(response.output_text)