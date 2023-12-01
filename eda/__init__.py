from .eda import eda as eda_english
from .eda_japanese import eda_ja as eda_japanese
from .tokenizer import get_tokenizer
from .synonym_extractor import get_synonym_extractor

version = "1.1.1"

__all__ = ["eda_english", "eda_japanese", "get_tokenizer", "get_synonym_extractor"]
