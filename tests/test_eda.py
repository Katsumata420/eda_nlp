import pytest
from eda import eda_english, eda_japanese
from eda.tokenizer import SudachiTokenizer, MeCabTokenizer
from eda.synonym_extractor import EXTRACTOR


def test_eda():
    """Test eda_english function."""
    original_sentence = "It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire."
    edit_sentences = eda_english(original_sentence)

    print(original_sentence)
    print(edit_sentences)
    assert type(edit_sentences) == list

    for sentence in edit_sentences:
        assert type(sentence) == str
        assert sentence != original_sentence


@pytest.mark.parametrize("synonym", ["sudachi", "conceptnet"])
def test_japanese_eda(synonym: str):
    """Test eda_ja function."""
    original_sentence = "日本語の文章をテストします。"

    if synonym == "sudachi":
        tokenizer = SudachiTokenizer()
        synonym_extractor = EXTRACTOR["sudachi"](tokenizer)
    elif synonym == "conceptnet":
        tokenizer = MeCabTokenizer()
        synonym_extractor = EXTRACTOR["conceptnet"]()
    else:
        raise ValueError("Invalid synonym.")

    edit_sentences = eda_japanese(
        original_sentence,
        tokenizer,
        synonym_extractor,
        alpha_sr=0.1,
        alpha_ri=0.1,
        alpha_rs=0.1,
        p_rd=0.1,
    )

    print(original_sentence)
    print(edit_sentences)
    assert type(edit_sentences) == list

    for sentence in edit_sentences:
        assert type(sentence) == str
        # If the probability of random deletion is low, the sentence may be the same as the original sentence.
        # assert sentence != original_sentence
