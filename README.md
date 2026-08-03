# Cents-AI Microservice

A **FastAPI**-based microservice that uses a LangChain agent powered by **Google Gemini** to intelligently extract and categorize financial expenses from natural language input.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Endpoints](#endpoints)
  - [GET /](#1-get-)
  - [GET /health](#2-get-health)
  - [POST /generate](#3-post-generate)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the Service](#running-the-service)
- [Configuration](#configuration)
- [CORS Policy](#cors-policy)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## Overview

This microservice accepts a natural-language prompt describing one or more expenses (e.g. *"I spent 500 rupees on pizza yesterday and 200 today on a movie"*) and returns structured, categorized transaction data as JSON. It's meant to sit behind a main backend that handles the core business/app logic.

## How It Works

1. A prompt hits `POST /generate`.
2. A system prompt (with today's date and formatting instructions baked in) is built via `prompts.py`.
3. A LangChain agent (`agent.py`), backed by `gemini-3.6-flash`, processes the message. The agent has access to a `get_exchange_rate` tool (`tools.py`) so it can convert non-INR amounts to INR using live exchange rates from [open.er-api.com](https://open.er-api.com/).
4. The agent's raw text output is extracted (`extraction.py`) and parsed into a strict Pydantic schema (`schemas.py`) using a `PydanticOutputParser`.
5. The parsed list of transactions is returned to the client.

If the LLM call fails, or its output can't be parsed as valid structured data, the API responds with an `HTTP 502` and a descriptive error message.

---

## Endpoints

### 1. `GET` `/`

**Description:** Welcome / root endpoint

**Purpose:** Confirms the service is reachable

**Request Example:**

```bash
curl -X GET http://localhost:8000/
```

**Response Example:**

```json
{
  "message": "Welcome to Cents-Ai-Microservice"
}
```

---

### 2. `GET` `/health`

**Description:** Health-check endpoint

**Purpose:** Used for uptime/health monitoring

**Request Example:**

```bash
curl -X GET http://localhost:8000/health
```

**Response Example:**

```json
{
  "status": "ok"
}
```

---

### 3. `POST` `/generate`

**Description:** Extract and categorize financial expenses from natural language input

**Required Input:**

| Field    | Type   | Description                                               |
| -------- | ------ | ----------------------------------------------------------|
| `prompt` | string | Natural language description of the expense(s) to extract |

**Request Body Schema:**

```json
{
  "prompt": "string"
}
```

**Request Example:**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I spent 500 rupees on pizza yesterday and 200 today on a movie"}'
```

**Response Format:**

Returns a JSON array of expense objects:

```json
[
  {
    "amount": 0,
    "transactionDate": "YYYY-MM-DD",
    "category": "food | entertainment | bills | shopping | travel | health | education | others"
  }
]
```

**Response Example:**

```json
[
  {
    "amount": 500,
    "transactionDate": "2025-12-04",
    "category": "food"
  },
  {
    "amount": 200,
    "transactionDate": "2025-12-05",
    "category": "entertainment"
  }
]
```

**Supported Categories:**

- `food`
- `entertainment`
- `bills`
- `shopping`
- `travel`
- `health`
- `education`
- `others`

**Processing Rules:**

- **Multiple transactions:** Every distinct purchase mentioned in a single prompt is extracted as its own entry — the agent never merges or splits purchases incorrectly.
- **Date handling:** Relative references like "today," "yesterday," "kal," and "aaj" are resolved against the current date. If no date is mentioned, today's date is used, and different transactions in the same prompt can resolve to different dates.
- **Missing amount:** Defaults to `0` if not stated.
- **Currency conversion:** Non-INR amounts are converted to INR using the `get_exchange_rate` tool, which fetches live rates.
- **Unknown categories:** Assigned to `"others"` if nothing else fits.
- **No expense detected:** Returns a single entry — `amount: 0`, `transactionDate: today`, `category: "others"`.
- **Response format:** The LLM is instructed to return only valid JSON — no prose, no markdown fences.

**Natural Language Examples:**

1. Simple expense
   ```json
   {"prompt": "I spent 100 rupees on coffee"}
   ```

2. Multiple expenses
   ```json
   {"prompt": "Yesterday I paid 5000 for electricity bill and today spent 300 on groceries"}
   ```

3. With date references (Hinglish supported)
   ```json
   {"prompt": "Kal rupees 1500 ka taxi, aaj 200 movie ticket"}
   ```

4. With foreign currency
   ```json
   {"prompt": "Spent 50 dollars on shopping"}
   ```

---

## Project Structure

```
.
├── main.py           # FastAPI app, routes, CORS setup
├── agent.py           # LangChain agent definition (Gemini + tools)
├── tools.py           # Currency exchange-rate tool for the agent
├── prompts.py         # System prompt template + output parser
├── schemas.py         # Pydantic response models
├── extraction.py      # Helper to pull plain text out of an agent message
├── config.py          # Environment variable loading
├── requirements.txt   # Python dependencies
├── .env.example       # Sample environment file
└── test.py            # (placeholder for tests)
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- A Google Gemini API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/harshitkumar7525/CentsAI-gemini-microservice.git
   cd CentsAI-gemini-microservice
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (use `.env.example` as a reference):
   ```bash
   cp .env.example .env
   ```

5. Add your Gemini API key and backend URL to `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   BACKEND_URL=your_main_backend_url
   ```

   > **Note:** `.env.example` currently lists `CENTS_AI_BACKEND`, but `config.py` reads `BACKEND_URL` for the CORS origin. Make sure the variable name in your `.env` matches what `config.py` expects (`BACKEND_URL`), or update `config.py` if you'd rather keep `CENTS_AI_BACKEND`.

### Running the Service

**Development (with auto-reload):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Directly via Python:**
```bash
python main.py
```

The service will be available at `http://0.0.0.0:8000` (or your configured `PORT`). Interactive API docs are automatically available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

---

## Configuration

### Environment Variables

| Variable         | Required | Description                                          |
| ----------------- | -------- | ----------------------------------------------------- |
| `GEMINI_API_KEY`  | Yes      | Your Google Gemini API key                            |
| `BACKEND_URL`     | Yes      | URL of your main backend, used as the allowed CORS origin |
| `PORT`            | No       | Server port when running `python main.py` (default: `8000`) |

---

## CORS Policy

The service is configured with CORS middleware to accept requests only from the configured backend:

- **Allowed Origins:** `BACKEND_URL`
- **Allowed Methods:** All
- **Allowed Headers:** All
- **Allow Credentials:** Yes

---

## Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** — Web framework
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server
- **[LangChain](https://www.langchain.com/)** — Agent orchestration
- **[langchain-google-genai](https://python.langchain.com/docs/integrations/chat/google_generative_ai/)** — Gemini integration for LangChain
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation and structured output parsing
- **[Google Gemini](https://ai.google.dev/)** (`gemini-3.6-flash`) — Natural language understanding and expense extraction

---

## License

This project is maintained by [harshitkumar7525](https://github.com/harshitkumar7525).