"""Synonym Extractor for Japanese"""
import csv
import os
from abc import ABC, abstractmethod
from urllib3.util import Retry
from typing import List, Dict, Optional, Set

import requests
from requests.adapters import HTTPAdapter

from .tokenizer import SudachiTokenizer


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
    """Sudachi synonym extractor.

    TODO: Use chikkar https://github.com/WorksApplications/chikkar/
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    synonym_path = os.path.join(current_dir, "resource/sudachi_synonyms.txt")
    def __init__(self, tokenizer: SudachiTokenizer):
        assert os.path.isfile(self.synonym_path), f"Not Found Synonym data at {self.synonym_path}."
        self.synonym_data = self._load_synonyms()
        self.tokenizer = tokenizer

    def _load_synonyms(self) -> Dict[int, Set[str]]:
        with open(self.synonym_path, "r") as f:
            reader = csv.reader(f)
            data = [row for row in reader]

        synonym_data: Dict[int, Set[str]] = {}
        synonym_set = set()  # 8th index
        synonym_group_id: Optional[int] = None  # 0th index
        for line in data:
            if not line:
                if synonym_group_id is not None:
                    synonym_data[synonym_group_id] = synonym_set
                synonym_set = set()
                synonym_group_id = None
            else:
                synonym_group_id = int(line[0])
                synonym_set.add(line[8])
        return synonym_data

    @property
    def name(self) -> str:
        return "sudachi"

    def get_synonyms(self, word: str) -> List[str]:
        synonym_group_ids = self.tokenizer.get_synonym_group_ids(word)
        synonyms = set()
        for synonym_group_id in synonym_group_ids:
            synonyms |= self.synonym_data.get(synonym_group_id, set())
        synonyms = synonyms - {word}  # Remove original word
        return list(synonyms)


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


def get_synonym_extractor(name: str, tokenizer: SudachiTokenizer) -> BaseSynonymExtractor:
    if name == "sudachi":
        return SudachiSynonymExtractor(tokenizer)
    elif name == "conceptnet":
        return ConceptNetSynonymExtractor()
    else:
        raise ValueError("Invalid synonym extractor.")
