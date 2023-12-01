import re
import random
import unicodedata
from typing import List

from spacy.lang import ja

from .eda import random_swap, random_deletion
from .tokenizer import BaseTokenizer
from .synonym_extractor import BaseSynonymExtractor


stop_words = ja.STOP_WORDS  # Set


def get_only_chars(line: str) -> str:
    """"Clean up text.

    - Replace hyphens with spaces
    - Replace tabs with spaces
    - Replace newlines with spaces
    - Lowercase all characters
    - Delete extra spaces
    - Delete leading spaces
    - Unicode normalization
    """
    clean_line = ""

    line = line.replace("’", "")
    line = line.replace("'", "")
    line = line.replace("-", " ") #replace hyphens with spaces
    line = line.replace("\t", " ")
    line = line.replace("\n", " ")
    line = line.lower()
    line = unicodedata.normalize("NFKC", line)

    clean_line = re.sub(' +',' ',line) #delete extra spaces
    if clean_line[0] == ' ':
        clean_line = clean_line[1:]

    return clean_line


def synonym_replacement(words: List[str], n: int, synonym_extractor: BaseSynonymExtractor) -> List[str]:
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = synonym_extractor.get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break

    # followed original eda.py
    # > this is stupid but we need it, trust me
    sentence = " ".join(new_words)
    new_words = sentence.split(" ")
    return new_words


def random_insertion(words: List[str], n: int, synonym_extractor: BaseSynonymExtractor) -> List[str]:
    def add_word(new_words: List[str]) -> None:
        synonyms = []
        counter = 0
        while len(synonyms) < 1:
            random_word = words[random.randint(0, len(words) - 1)]
            synonyms = synonym_extractor.get_synonyms(random_word)
            counter += 1
            if counter >= 10:
                return
        random_synonym = synonyms[0]
        random_idx = random.randint(0, len(new_words) - 1)
        new_words.insert(random_idx, random_synonym)

    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words


def eda_ja(
    sentence: str,
    tokenizer: BaseTokenizer,
    synonym_extractor: BaseSynonymExtractor,
    alpha_sr: float = 0.1,
    alpha_ri: float = 0.1,
    alpha_rs: float = 0.1,
    p_rd: float = 0.1,
    num_aug: int = 9,
    is_append_original: bool = False,
) -> List[str]:
    """Perform EDA for Japanese."""
    if synonym_extractor.name == "sudachi":
        assert tokenizer.name == "sudachi"

    sentence = get_only_chars(sentence)
    words = tokenizer.tokenize(sentence)
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug / 4) + 1

    if alpha_sr > 0:
        n_sr = max(1, int(alpha_sr * num_words))
        for _ in range(num_new_per_technique):
            a_words = synonym_replacement(words, n_sr, synonym_extractor)
            augmented_sentences.append("".join(a_words))

    if alpha_ri > 0:
        n_ri = max(1, int(alpha_ri * num_words))
        for _ in range(num_new_per_technique):
            a_words = random_insertion(words, n_ri, synonym_extractor)
            augmented_sentences.append("".join(a_words))

    if alpha_rs > 0:
        n_rs = max(1, int(alpha_rs * num_words))
        for _ in range(num_new_per_technique):
            a_words = random_swap(words, n_rs)
            augmented_sentences.append("".join(a_words))

    if p_rd > 0:
        for _ in range(num_new_per_technique):
            a_words = random_deletion(words, p_rd)
            augmented_sentences.append("".join(a_words))

    augmented_sentences = [get_only_chars(sentence) for sentence in augmented_sentences]
    random.shuffle(augmented_sentences)

    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    if is_append_original:
        augmented_sentences.append(sentence)

    return augmented_sentences
