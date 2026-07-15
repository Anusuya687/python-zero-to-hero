import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Anthropic Config
claude_model = os.getenv("ANTHROPIC_DEFAULT_SONNET_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
anthropic_url = os.getenv("ANTHROPIC_BASE_URL", "")

client = Anthropic()
model = claude_model

assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
)
assert anthropic_url, "Error: ANTHROPIC_BASE_URL cannot be empty. Update .env"

message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What is quantum computing? Answer in one sentence"
        }
    ]
)

print(message.content[0].text)