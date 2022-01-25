import pytest
from app import hello, extract_sentiment, text_contain_word, bubblesort


def test_hello():
    got = hello("Aleksandra")
    want = "Hello Aleksandra"

    assert got == want


def test_extract_sentiment():

    text = "I think today will be a great day"

    sentiment = extract_sentiment(text)

    assert sentiment > 0


def test_extract_sentiment_positive():

    text = "I think today will be a great day"

    sentiment = extract_sentiment(text)

    assert sentiment > 0


def test_extract_sentiment_negative():

    text = "I do not think this will turn out well"

    sentiment = extract_sentiment(text)

    assert sentiment < 0


testdata = ["I think today will be a great day", "I do not think this will turn out well"]


@pytest.mark.parametrize('sample', testdata)
def test_extract_sentiment(sample):

    sentiment = extract_sentiment(sample)

    assert sentiment > 0


testdata = [
    ('There is a duck in this text', 'duck', True),
    ('There is nothing here', 'duck', False)
    ]


@pytest.mark.parametrize('sample, word, expected_output', testdata)
def test_text_contain_word(sample, word, expected_output):

    assert text_contain_word(word, sample) == expected_output


testdata = [
    ([4, 2, 6, 3, 1, 5], [1, 2, 3, 4, 5, 6]),
    ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]),
    ([90, 50, 22, 8, 37, 26, 41, 77, 94, 6, 48, 91, 2, 65, 88, 59, 84, 92, 7, 74, 61, 16],
     [2, 6, 7, 8, 16, 22, 26, 37, 41, 48, 50, 59, 61, 65, 74, 77, 84, 88, 90, 91, 92, 94]),
    ([79, 21, 1, 89, 67, 2, 7, 29, 97, 20], [1, 2, 7, 20, 21, 29, 67, 79, 89, 97]),
    ([0, 22, 41, 1, 22, 1, 41, 0, 1, 41, 54, 22], [0, 0, 1, 1, 1, 22, 22, 22, 41, 41, 41, 54])
    ]


@pytest.mark.parametrize('sample, expected', testdata)
def test_bubblesort(sample, expected):
    assert bubblesort(sample) == expected
