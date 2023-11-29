from eda import eda_english


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
