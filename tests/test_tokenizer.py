import pytest
from eda.tokenizer import SudachiTokenizer, MeCabTokenizer


@pytest.mark.parametrize("tokenizer", ["sudachi", "mecab"])
def test_tokenizer(tokenizer: str) -> None:
    """Test tokenizer."""
    original_sentence = "日本語の文章をテストします。"
    if tokenizer == "sudachi":
        tokenizer = SudachiTokenizer()
    elif tokenizer == "mecab":
        tokenizer = MeCabTokenizer()
    else:
        raise ValueError(f"Invalid tokenizer name: {tokenizer}")
    words = tokenizer.tokenize(original_sentence)

    assert type(words) == list
    print(words)
