# Stateful Chatbots with OpenAI API

This project contains two minimal Python chatbot scripts:

- **statefulchat.py**: Uses the new OpenAI Responses API for stateful conversation.
- **statefulchat-old.py**: Uses the traditional OpenAI Completions (Chat) API for stateful conversation.

## Setup

### 1. Create and activate a virtual environment
```bash
uv venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
uv pip install -r requirements.txt
# or if using pyproject.toml
uv pip install .
```

### 3. Set your OpenAI API key
Create a `.env` file in this directory:
```env
OPENAI_API_KEY=your-api-key-here
```
(Your `.env` is already in `.gitignore`.)

### 4. Run the chatbot
```bash
python statefulchat.py
```

## Usage

### Responses API (Recommended)
Run:
```bash
python statefulchat.py
```

### Completions API (Legacy)
Run:
```bash
python statefulchat-old.py
```

Both scripts will prompt you for input in the terminal and maintain conversation state within the session.

---

- `statefulchat.py` uses the latest OpenAI Responses API and is recommended for new projects.
- `statefulchat-old.py` uses the classic chat/completions API for backwards compatibility.

## Tips

- Use `uv sync` to ensure your environment matches the lockfile.
- Use `deactivate` to leave the virtual environment.
