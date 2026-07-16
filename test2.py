import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# Anthropic Config
claude_model = os.getenv("ANTHROPIC_DEFAULT_SONNET_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
anthropic_url = os.getenv("ANTHROPIC_BASE_URL", "")

client = Anthropic(
    api_key=anthropic_api_key,
    base_url=anthropic_url,
    timeout=60.0,
)
model = claude_model

assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
)
assert anthropic_url, "Error: ANTHROPIC_BASE_URL cannot be empty. Update .env"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    return response.content[0].text

messages = []
add_user_message(messages, 'What is quantum computing in one senetnce')
answer = chat(messages)

print(answer)

add_assistant_message(messages,answer)
add_user_message(messages, 'write another line')
answer= chat(messages)
print(answer)