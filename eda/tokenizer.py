from abc import ABC, abstractmethod

class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> list:
        pass

    @staticmethod
    @abstractmethod
    def name(self) -> str:
        pass


class SudachiTokenizer(BaseTokenizer):
    def __init__(self):
        pass

    @staticmethod
    def name(self) -> str:
        return "sudachi"

    def tokenize(self, text: str) -> list:
        pass


class MeCabTokenizer(BaseTokenizer):
    def __init__(self):
        pass

    @staticmethod
    def name(self) -> str:
        return "mecab"

    def tokenize(self, text: str) -> list:
        pass
