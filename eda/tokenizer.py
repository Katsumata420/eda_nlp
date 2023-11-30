import functools
import os
from abc import ABC, abstractmethod
from typing import List

import fugashi
from sudachipy import tokenizer as sudachi_tokenizer
from sudachipy import dictionary


class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class SudachiTokenizer(BaseTokenizer):
    def __init__(self):
        self.tokenizer = dictionary.Dictionary().create()
        mode = sudachi_tokenizer.Tokenizer.SplitMode.C
        self.tokenizer = functools.partial(self.tokenizer.tokenize, mode=mode)

    @property
    def name(self) -> str:
        return "sudachi"

    def tokenize(self, text: str) -> List[str]:
        return [m.surface() for m in self.tokenizer(text)]

    def get_synonym_group_ids(self, word: str) -> List[int]:
        token = self.tokenizer(word)[0]
        return token.synonym_group_ids()


class MeCabTokenizer(BaseTokenizer):
    supported_dictionaries = ["unidic", "unidic_lite", "ipadic"]
    def __init__(self, dictionary: str = "ipadic"):
        assert dictionary in self.supported_dictionaries
        dic_dir: str
        if dictionary == "ipadic":
            import ipadic
            dic_dir = ipadic.DICDIR
        elif dictionary == "unidic":
            import unidic
            dic_dir = unidic.DICDIR
        elif dictionary == "unidic_lite":
            import unidic_lite
            dic_dir = unidic_lite.DICDIR

        mecabrc = os.path.join(dic_dir, "mecabrc")
        mecab_option = f'-d "{dic_dir}" -r "{mecabrc}" -Owakati'

        self.tokenizer = fugashi.GenericTagger(mecab_option)

    @property
    def name(self) -> str:
        return "mecab"

    def tokenize(self, text: str) -> List[str]:
        return self.tokenizer.parse(text).split()
