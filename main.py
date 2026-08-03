from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import BACKEND_URL
from schemas import Response
from prompts import prompt_template, parser
from agent import finance_agent
from extraction import extract_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[BACKEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Cents-Ai-Microservice"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate", response_model=Response)
async def generate(prompt: str):
    today = str(date.today())
    formatted_messages = prompt_template.format_messages(today=today, prompt=prompt)

    try:
        result = finance_agent.invoke({"messages": formatted_messages})
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent invocation failed: {exc}")

    final_message = result["messages"][-1]
    output_text = extract_text(final_message)

    if not output_text.strip():
        raise HTTPException(status_code=502, detail="LLM response contained no text content to parse.")

    try:
        parsed_response = parser.parse(output_text)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to parse LLM response as structured expense data: {exc}",
        )

    return parsed_response