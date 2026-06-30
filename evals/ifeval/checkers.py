import re
import json


def compare_count(value: int, relation: str | None, target: int) -> bool:
    relation = relation or 'exactly'

    if relation == 'exactly':
        return value == target
    if relation == 'at least':
        return value >= target
    if relation == 'at most':
        return value <= target
    if relation == 'less than':
        return value < target
    if relation == 'more than':
        return value > target

    raise ValueError(f'Unsupported relation: "{relation}"')

def check_no_comma(response: str, **kwargs) -> bool:
    return ',' not in response

PLACEHOLDER_RE = re.compile(r"\[[^\[\]\n]+\]")
def check_number_placeholders(response: str, *, num_placeholders: int, relation: str | None = None, **kwargs) -> bool:
    placeholders = PLACEHOLDER_RE.findall(response)
    return compare_count(value=len(placeholders), relation=relation or 'at least', target=num_placeholders)

BULLET_RE = re.compile(r"(?m)^\s*\* .+")
def check_number_bullet_lists(response: str, *, num_bullets: int, relation: str | None = None, **kwargs) -> bool:
    bullets = BULLET_RE.findall(response)
    return compare_count(value=len(bullets), relation=relation or 'exactly', target=num_bullets)

TITLE_RE = re.compile(r"<<[^<>\n]+>>")
def check_title(response: str, **kwargs) -> bool:
    return bool(TITLE_RE.search(response))

def check_repeat_prompt(response: str, *, prompt_to_repeat: str, **kwargs) -> bool:
    return response.startswith(prompt_to_repeat)

def check_english_lowercase(response: str, **kwargs) -> bool:
    letters = [char for char in response if char.isalpha()]
    return bool(letters) and all(char.islower() for char in letters)

def check_keywords_existence(response: str, *, keywords: list[str], **kwargs) -> bool:
    return all(keyword.lower() in response.lower() for keyword in keywords)

def check_forbidden_words(response: str, *, forbidden_words: list[str] | None = None, keywords: list[str] | None = None, **kwargs) -> bool:
    words = forbidden_words or keywords or []
    return all(word.lower() not in response.lower() for word in words)

def check_end_checker(response: str, *, end_phrase: str, **kwargs) -> bool:
    return response.strip().endswith(end_phrase)

def check_quotation(response: str, **kwargs) -> bool:
    text = response.strip()
    return len(text) >= 2 and text[0] == '"' and text[-1] == '"'

WORD_RE = re.compile(r"\b[\w'-]+\b")
def check_number_words(response: str, *, num_words: int, relation: str | None = None, **kwargs) -> bool:
    word_count = len(WORD_RE.findall(response))
    return compare_count(value=word_count, relation=relation or 'exactly', target=num_words)

IS_JSON_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", flags=re.DOTALL | re.IGNORECASE)
def check_json_format(response: str, **kwargs) -> bool:
    response = response.strip()
    match = IS_JSON_RE.fullmatch(response)
    text = match.group(1).strip() if match else response
    try:
        json.loads(text)
        return True
    except Exception:
        return False

def check_two_responses(response: str, **kwargs) -> bool:
    parts = [part.strip() for part in response.split('******')]
    return len(parts) == 2 and all(parts)

def check_english_capital(response: str, **kwargs) -> bool:
    letters = [char for char in response if char.isalpha()]
    return bool(letters) and all(char.isupper() for char in letters)

def check_postscript(response: str, *, postscript_marker: str | None = None, **kwargs) -> bool:
    marker = postscript_marker or 'P.S.'
    return marker.lower() in response.lower()

HIGHLIGHT_RE = re.compile(r"(?<!\*)\*[^*\n]+\*(?!\*)|\*\*[^*\n]+\*\*")
def check_number_highlighted_sections(response: str, *, num_highlights: int, relation: str | None = None, **kwargs) -> bool:
    highlights = HIGHLIGHT_RE.findall(response)
    return compare_count(value=len(highlights), relation=relation or 'at least', target=num_highlights)

KEYWORK_OCCURENCE_RE = re.compile(r"[A-Za-z0-9_]+")
def count_keyword_occurrences(response: str, keyword: str) -> int:
    if re.fullmatch(KEYWORK_OCCURENCE_RE, keyword):
        pattern = rf"\b{re.escape(keyword)}\b"
    else:
        pattern = re.escape(keyword)
    return len(re.findall(pattern, response, flags=re.IGNORECASE))

def check_keyword_frequency(response: str, *, keyword: str | None = None, keywords: list[str] | None = None, frequency: int, relation: str | None = None, **kwargs) -> bool:
    if keyword is None:
        if not keywords:
            raise ValueError('Missing keyword/keywords')
        keyword = keywords[0]

    count = count_keyword_occurrences(response, keyword)
    return compare_count(value=count, relation=relation or 'exactly', target=frequency)

def check_letter_frequency(response: str, *, letter: str, let_frequency: int, let_relation: str | None = None, **kwargs) -> bool:
    if len(letter) != 1:
        raise ValueError(f'Expected a single character letter, got {letter!r}')

    if letter.isalpha():
        count = response.lower().count(letter.lower())
    else:
        count = response.count(letter)

    return compare_count(value=count, relation=let_relation or 'exactly', target=let_frequency)

def check_number_paragraphs(response: str, *, num_paragraphs: int, relation: str | None = None, section_spliter: str | None = None, **kwargs) -> bool:
    response = response.strip()
    if response:
        parts = response.split(section_spliter) if section_spliter else re.split(r'\n\s*\n', response)
    else:
        parts = []
    paragraphs = [part.strip() for part in parts if part.strip()]
    return compare_count(value=len(paragraphs), relation=relation or 'exactly', target=num_paragraphs)

CHECKERS = {
    'punctuation:no_comma': check_no_comma,
    'detectable_content:number_placeholders': check_number_placeholders,
    'detectable_format:number_bullet_lists': check_number_bullet_lists,
    'detectable_format:title': check_title,
    'combination:repeat_prompt': check_repeat_prompt,
    'change_case:english_lowercase': check_english_lowercase,
    'keywords:existence': check_keywords_existence,
    'keywords:forbidden_words': check_forbidden_words,
    'startend:end_checker': check_end_checker,
    'startend:quotation': check_quotation,
    'length_constraints:number_words': check_number_words,
    'detectable_format:json_format': check_json_format,
    'combination:two_responses': check_two_responses,
    'change_case:english_capital': check_english_capital,
    'detectable_content:postscript': check_postscript,
    'detectable_format:number_highlighted_sections': check_number_highlighted_sections,
    'keywords:frequency': check_keyword_frequency,
    'keywords:letter_frequency': check_letter_frequency,
    'length_constraints:number_paragraphs': check_number_paragraphs
}
