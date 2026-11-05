import num2words
from .number_names import (
    LARGE,
    LETTERS,
    MASCULINE_BEFORE_LARGE,
    NUMBER_NAMES,
    TEENS,
)
import re

# "$50" is read "fifty dollars", so these symbols move after the number
CURRENCY_PREFIXES = {"$", "₪"}


def split_prefix(word: str) -> tuple[str, str]:
    """
    Split the Vav / He that num2words glues to a number word, eg. "ושלוש"
    """
    if word not in NUMBER_NAMES and word[:1] in LETTERS:
        return LETTERS[word[0]], word[1:]
    return "", word


def add_diacritics(words: str):
    tokens = words.split()
    new_words = []
    i = 0
    while i < len(tokens):
        prefix, word = split_prefix(tokens[i])
        next_word = tokens[i + 1] if i + 1 < len(tokens) else ""
        teen = TEENS.get(f"{word} {next_word}")
        if teen:
            new_words.append(prefix + teen)
            i += 2
            continue
        if word in MASCULINE_BEFORE_LARGE and next_word in LARGE:
            new_words.append(prefix + MASCULINE_BEFORE_LARGE[word])
        elif word in NUMBER_NAMES:
            new_words.append(prefix + NUMBER_NAMES[word])
        else:
            new_words.append(tokens[i])
        i += 1
    return " ".join(new_words)


def num_to_word(maybe_number: str) -> str:
    def replace_number(match):
        num: str = match.group()
        suffix, prefix = "", ""
        # prefix
        if not num.startswith("-") and not num[0].isdigit():
            prefix = num[0]
            num = num[1:]
        if not num[-1].isdigit():
            suffix = num[-1]
            num = num[:-1]
        if prefix in CURRENCY_PREFIXES:
            prefix, suffix = "", f"{prefix} {suffix}"
        words = num2words.num2words(num, lang="he", ordinal=False)
        words_with_diacritics = add_diacritics(words)
        return (
            f"{prefix.strip()} {words_with_diacritics.strip()} {suffix.strip()}".strip()
        )

    # Replace all whole numbers in the string
    result = re.sub(r"[^\d\-]?-?\d+(?:[\.,]\d+)?[^\d]?", replace_number, maybe_number)

    return result
