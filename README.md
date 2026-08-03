# Cents-AI Microservice

A FastAPI-based microservice that uses Google's Gemini AI to intelligently extract and categorize financial expenses from natural language input.

## Overview

This microservice processes financial expense data by accepting user prompts and using the Gemini 2.5 Flash model to extract structured expense information in JSON format.

## Endpoints

### 1. **GET** `/`

**Description:** Welcome/Health check endpoint

**Purpose:** Returns a welcome message to confirm the service is running

**Required Input:** None

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

### 2. **POST** `/generate`

**Description:** Generate and extract financial expenses from user input

**Purpose:** Processes natural language input to extract expense information and categorize them using AI

**Required Input:**

| Field | Type | Description |
|-------|------|-------------|
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

Returns a JSON array of expense objects with the following structure:

```json
[
  {
    "amount": number,
    "transactionDate": "YYYY-MM-DD",
    "category": "string"
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

- **Date Handling:** The system uses relative dates like "kal" (yesterday) or "today". If no date is mentioned, today's date is used.
- **Missing Amount:** If the amount is not specified, it defaults to `0`.
- **Currency Conversion:** Non-INR amounts are automatically converted using last known currency rates.
- **Unknown Categories:** Expenses that don't fit predefined categories are assigned to `"others"`.
- **No Expense Scenario:** If no expenses are detected in the input, returns `[{"amount":0,"transactionDate":"TODAY","category":"others"}]`.
- **Response Format:** Always returns valid JSON only.

**Natural Language Examples:**

1. Simple expense:
   ```
   {"prompt": "I spent 100 rupees on coffee"}
   ```

2. Multiple expenses:
   ```
   {"prompt": "Yesterday I paid 5000 for electricity bill and today spent 300 on groceries"}
   ```

3. With date references:
   ```
   {"prompt": "Kal rupees 1500 ka taxi, aaj 200 movie ticket"}
   ```

4. With foreign currency:
   ```
   {"prompt": "Spent 50 dollars on shopping"}
   ```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/harshitkumar7525/CentsAI-gemini-microservice.git
cd cents-ai-microservice
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (use `.env.example` as reference):
```bash
cp .env.example .env
```

4. Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

### Running the Service

**Development:**
```bash
python main.py
```

**Production (with custom port):**
```bash
PORT=8080 python main.py
```

The service will be available at `http://0.0.0.0:8000` (or your specified port)

---

## API Documentation

Once the service is running, you can access interactive API documentation at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |
| `CENTS_AI_BACKEND` | Yes | Your main backend handling all the business logic |
| `PORT` | No | Server port (default: 8000) |

---

## CORS Policy

The service allows requests from all origins with CORS middleware enabled:
- Allow Origins: `YOUR MAIN BACKEND_URL`
- Allow Methods: All
- Allow Headers: All

---

## Technologies Used

- **FastAPI:** Web framework
- **Pydantic:** Data validation
- **Google Gemini AI:** Natural language processing and expense extraction
- **Uvicorn:** ASGI server
- **python-dotenv:** Environment variable management

---

## License

This project is maintained by [harshitkumar7525](https://github.com/harshitkumar7525)
