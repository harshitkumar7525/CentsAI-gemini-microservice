import requests
from langchain.tools import tool


@tool
def get_exchange_rate(src: str) -> str:
    """
    Find the exchange rate between two currencies.
    LLM can use this tool to convert the source currency to Indian currency (INR).
    :param src: ISO 4217 currency code
    :return: exchange rate between source currency and indian currency
    """
    resp = requests.get(f"https://open.er-api.com/v6/latest/{src}")
    data = resp.json()
    return data["rates"]["INR"]