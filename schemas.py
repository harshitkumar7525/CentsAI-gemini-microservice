from typing import Literal
from datetime import date
from pydantic import BaseModel, Field


class Response(BaseModel):
    amount: float = Field(ge=0, description="The expense extracted from the prompt in Indian rupees")
    transactionDate: date = Field(description="The date the transaction was made", default_factory=date.today)
    category: Literal[
        "food", "entertainment", "bills", "shopping", "travel", "health", "education", "others"
    ] = Field(description="The category of the transaction")