def markdown_to_blocks(markdown: str) -> list[str]:
    rows = markdown.split("\n\n")
    return [row.strip() for row in rows if row.strip()]
