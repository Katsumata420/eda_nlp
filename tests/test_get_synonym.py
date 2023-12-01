import pytest
from eda.synonym_extractor import EXTRACTOR
from eda.tokenizer import SudachiTokenizer


@pytest.mark.parametrize("extractor", ["sudachi", "conceptnet"])
def test_synonym_extractor(extractor: str) -> None:
    """Test synonym extractor."""
    original_word = "日本"
    # original_word = "日産ネットワークホールディングス"

    if extractor == "sudachi":
        tokenizer = SudachiTokenizer()
        extractor = EXTRACTOR[extractor](tokenizer)
    elif extractor == "conceptnet":
        extractor = EXTRACTOR[extractor]()
    else:
        raise ValueError(f"Invalid extractor name: {extractor}")
    synonym_words = extractor.get_synonyms(original_word)

    assert type(synonym_words) == list
    print(synonym_words)
