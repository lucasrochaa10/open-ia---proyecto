from openai import OpenAI
client = OpenAI()

stream = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": "Termina este trabalenguas: el cielo está enladrillado...",
        },
    ],
    stream=True,
)

# ResponseTextDeltaEvent(content_index=0, delta='l', item_id='msg_684050b7307481a0a1ba1f55c1c13f8004cda34fc0f79bab', output_index=0, sequence_number=25, type='response.output_text.delta')
# ResponseTextDeltaEvent(content_index=0, delta='adr', item_id='msg_684050b7307481a0a1ba1f55c1c13f8004cda34fc0f79bab', output_index=0, sequence_number=26, type='response.output_text.delta')
# ResponseTextDeltaEvent(content_index=0, delta='ill', item_id='msg_684050b7307481a0a1ba1f55c1c13f8004cda34fc0f79bab', output_index=0, sequence_number=27, type='response.output_text.delta')
# ResponseTextDeltaEvent(content_index=0, delta='ador', item_id='msg_684050b7307481a0a1ba1f55c1c13f8004cda34fc0f79bab', output_index=0, sequence_number=28, type='response.output_text.delta')
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)