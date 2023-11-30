"""Synonym Extractor for Japanese"""
import json
from abc import ABC, abstractmethod
from urllib3.util import Retry
from typing import List

import requests
from requests.adapters import HTTPAdapter

class BaseSynonymExtractor(ABC):
    @abstractmethod
    def get_synonyms(self, word: str) -> List[str]:
        """Get synonyms of word.

        Returns:
            List[str]: List of synonyms
            If there is no synonym, return empty list.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class SudachiSynonymExtractor(BaseSynonymExtractor):
    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return "sudachi"

    def get_synonyms(self, word: str) -> List[str]:
        pass


class ConceptNetSynonymExtractor(BaseSynonymExtractor):
    n_retry = 5
    url = "http://api.conceptnet.io/query?node=/c/ja/{}&rel=/r/Synonym&limit=1000"
    connect_timeout = 10.0
    read_timeout = 30.0
    def __init__(self):
        self.retry = Retry(total=self.n_retry, backoff_factor=1, status_forcelist=[502, 503, 504])

    @property
    def name(self) -> str:
        return "conceptnet"

    def get_synonyms(self, word: str) -> List[str]:
        session = requests.Session()
        session.mount("http://", HTTPAdapter(max_retries=self.retry))
        response = session.get(
            url=self.url.format(word),
            timeout=(self.connect_timeout, self.read_timeout),
        )
        response = response.json()

        synonyms = set()
        for edge in response["edges"]:
            # Get link of synonym
            # Only Japanese term
            # allow bi-directional
            link: str
            language: str
            if edge["start"]["term"] == f"/c/ja/{word}":
                # right word is synonym
                link = edge["end"]["term"]
                language = edge["end"]["language"]
            else:
                # left word is synonym
                link = edge["start"]["term"]
                language = edge["start"]["language"]
            if language == "ja":
                synonyms.add(link.split("/")[-1])  # Remove prefix
        synonyms = synonyms - {word}  # Remove original word
        return list(synonyms)


EXTRACTOR = {
    "sudachi": SudachiSynonymExtractor,
    "conceptnet": ConceptNetSynonymExtractor,
}
