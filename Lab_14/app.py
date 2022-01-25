from textblob import TextBlob


def hello(name):
    output = f'Hello {name}'
    return output


def extract_sentiment(text):
    text = TextBlob(text)

    return text.sentiment.polarity


def text_contain_word(word: str, text: str):
    return word in text


def bubblesort(sample):
    is_sorted = False

    while not is_sorted:
        is_sorted = True
        for i in range(len(sample) - 1):
            if sample[i] > sample[i + 1]:
                sample[i], sample[i + 1] = sample[i + 1], sample[i]
                is_sorted = False

    return sample
