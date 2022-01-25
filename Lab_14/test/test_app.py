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
    ([1, 5, 4, 2, 6, 41, 11, 67, 12, 22, 45], [1, 2, 4, 5, 6, 11, 12, 22, 41, 45, 67]),
    ([9, 5, 3, 2, 1, 0, 11, 34, 55, 16, 80], [0, 1, 2, 3, 5, 9, 11, 16, 34, 55, 80]),
    ([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([0, 0, 0, 6, 9, 6, 3, 3, 3], [0, 0, 0, 3, 3, 3, 6, 6, 9])
    ]


@pytest.mark.parametrize('sample, expected', testdata)
def test_bubblesort(sample, expected):
    assert bubblesort(sample) == expected
