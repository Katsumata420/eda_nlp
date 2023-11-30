import functools
from abc import ABC, abstractmethod
from typing import List

from sudachipy import tokenizer as sudachi_tokenizer
from sudachipy import dictionary


class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def name(self) -> str:
        pass


class SudachiTokenizer(BaseTokenizer):
    def __init__(self):
        self.tokenizer = dictionary.Dictionary().create()
        mode = sudachi_tokenizer.Tokenizer.SplitMode.C
        self.tokenizer = functools.partial(self.tokenizer.tokenize, mode=mode)

    @staticmethod
    def name(self) -> str:
        return "sudachi"

    def tokenize(self, text: str) -> List[str]:
        return [m.surface() for m in self.tokenizer(text)]

    def get_synonym_group_ids(self, word: str) -> List[int]:
        token = self.tokenizer(word)[0]
        return token.synonym_group_ids()


class MeCabTokenizer(BaseTokenizer):
    def __init__(self):
        pass

    @staticmethod
    def name(self) -> str:
        return "mecab"

    def tokenize(self, text: str) -> list:
        pass
