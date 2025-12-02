from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import date
from google import genai
import os

# Load env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(prompt: Prompt):
    today = str(date.today())

    optimized_prompt = f"""
    You are a financial expense extractor. Return ONLY a JSON array.

    Categories: food, entertainment, bills, shopping, travel, health, education, others
    Today: {today}

    Rules:
    - Use mentioned date or 'kal/yesterday'. Else Today.
    - Missing amount → 0.
    - Non-INR → convert using last known currency rate.
    - Each object: amount, transactionDate, category.
    - Unknown category → "others".
    - JS Date compatible.
    - If no expense → return [{{"amount":0,"transactionDate":Today,"category":"others"}}].
    - Output MUST be valid JSON ONLY.

    User Input: "{prompt.prompt}"
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=optimized_prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return response.text
