# Hugging Face LlamaIndex Agent

A small LlamaIndex agent that uses Hugging Face Inference API and exposes a
`multiply` tool.

## Requirements

- Python 3.10 or newer
- A Hugging Face access token with permission to use the configured model

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your token:

```env
HF_TOKEN=your_huggingface_token
```

## Run

```powershell
python app.py
```

The agent sends a multiplication question to the configured Hugging Face
model and prints the response.