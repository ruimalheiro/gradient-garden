import re
import string

from difflib import SequenceMatcher


def normalize_text(text: str, normalize: list[str] | None = None) -> str:
    normalize = normalize or []
    for step in normalize:
        if step == 'strip':
            text = text.strip()
        elif step == 'lower':
            text = text.lower()
        elif step == 'strip_punct':
            text = text.strip(string.punctuation + ' \t\n\r')
        else:
            raise ValueError(f'Unsupported normalization step: {step}')
    return text

def check_exact_match(response: str, targets: list[str], normalize: list[str] | None = None, **kwargs):
    normalized_response = normalize_text(response, normalize)
    normalized_targets = {
        normalize_text(target, normalize)
        for target in targets
    }
    return normalized_response in normalized_targets

def check_non_empty(response: str, **kwargs):
    return bool(response.strip())

def check_no_role_leak(response: str, **kwargs):
    forbidden = [
        'System:',
        'User:',
        'Assistant:',
        '<|system|>',
        '<|user|>',
        '<|assistant|>',
    ]
    return all(item.lower() not in response.lower() for item in forbidden)

def check_comma_list_count(response: str, n: int, **kwargs):
    if (
        '\n' in response or
        ':' in response
    ):
        return False
    items = [item.strip() for item in response.strip().split(',')]
    if any(not item for item in items):
        return False
    return len(items) == n

NUMBERED_LIST_RE = re.compile(r"^\s*\d+\s*(?:[.)]|-)\s+\S+")
def check_numbered_list_count(response: str, n: int, **kwargs):
    lines = [line.strip() for line in response.strip().splitlines() if line.strip()]
    if len(lines) != n:
        return False
    return all(NUMBERED_LIST_RE.match(line) for line in lines)

def check_contains_all(response: str, must_contain: list[str], case_sensitive: bool = False, **kwargs):
    text = response if case_sensitive else response.lower()
    for item in must_contain:
        target = item if case_sensitive else item.lower()
        if target not in text:
            return False
    return True

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*")
def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))

def check_max_words(response: str, max_words: int, **kwargs) -> bool:
    return count_words(response) <= max_words

WHITESPACE_RE = re.compile(r"\s+")
def normalize_for_similarity(text: str) -> str:
    text = text.strip().lower()
    text = WHITESPACE_RE.sub(' ', text)
    return text

def similarity_ratio(a: str, b: str) -> float:
    a = normalize_for_similarity(a)
    b = normalize_for_similarity(b)

    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def check_not_near_copy(response: str, source: str, max_similarity: float = 0.85, min_words: int = 3, **kwargs) -> bool:
    if not response.strip():
        return False

    if count_words(response) < min_words:
        return False

    return similarity_ratio(response, source) < max_similarity


CHECKERS = {
    'exact_match': check_exact_match,
    'non_empty': check_non_empty,
    'no_role_leak': check_no_role_leak,
    'comma_list_count': check_comma_list_count,
    'numbered_list_count': check_numbered_list_count,
    'contains_all': check_contains_all,
    'max_words': check_max_words,
    'not_near_copy': check_not_near_copy
}
