import pytest
from eda.synonym_extractor import EXTRACTOR


@pytest.mark.parametrize("extractor", ["sudachi", "conceptnet"])
def test_synonym_extractor(extractor: str) -> None:
    """Test synonym extractor."""
    original_word = "日本"

    extractor = EXTRACTOR[extractor]()
    synonym_words = extractor.get_synonyms(original_word)

    assert type(synonym_words) == list
    print(synonym_words)
