import regex as re

def count_words(text):
    """Accurate word count for localization (supports Arabic/English)"""
    if not text:
        return 0
    # Match words with Arabic/Unicode characters
    return len(re.findall(r'\b\p{Arabic}+\b|\b\w+\b', text, re.UNICODE))

def count_segments(text):
    """Count translatable segments (paragraphs)"""
    if not text:
        return 0
    # Split by two or more newlines
    return len(re.split(r'\n{2,}', text.strip()))
