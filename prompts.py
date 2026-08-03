from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas import Response

parser = PydanticOutputParser(pydantic_object=Response)

SYSTEM_PROMPT_TEMPLATE = """You are a financial assistant embedded in an expense-tracking app called Cents-AI.
... (unchanged) ...
{format_instructions}
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_TEMPLATE),
    ("human", "{prompt}"),
]).partial(format_instructions=parser.get_format_instructions())