import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    print("Stateful Chatbot (Completions API, type 'exit' to quit)")
    model = "gpt-4o-mini"
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        conversation.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model=model,
                messages=conversation
            )
            text = response.choices[0].message.content.strip()
            print(f"Bot: {text}")
            conversation.append({"role": "assistant", "content": text})
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
