def extract_text(message) -> str:
    """Pull just the plain-text block(s) out of an AIMessage.content."""
    content = message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = [
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "".join(parts)

    return str(content)