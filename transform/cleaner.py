def clean_text(text):
    if not isinstance(text, str):
        return text
    return text.strip().lower()
