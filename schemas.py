from typing import Literal, List
from datetime import date
from pydantic import BaseModel, Field


class Response(BaseModel):
    amount: float = Field(ge=0, description="The expense extracted from the prompt in Indian rupees")
    transactionDate: date = Field(description="The date the transaction was made", default_factory=date.today)
    category: Literal[
        "food", "entertainment", "bills", "shopping", "travel", "health", "education", "others"
    ] = Field(description="The category of the transaction")


class ResponseList(BaseModel):
    """Wrapper so PydanticOutputParser has a single root object to parse the LLM's
    JSON into. Only `transactions` is what actually gets returned to the client —
    /generate unwraps this before responding."""
    transactions: List[Response] = Field(
        description="Every individual expense/transaction mentioned in the prompt, "
        "one entry per distinct purchase. Must contain at least one entry."
    )