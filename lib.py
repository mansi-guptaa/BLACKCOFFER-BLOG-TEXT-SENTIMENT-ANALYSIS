"""
This is a secondary file, primary file is "main.py"
It's to improve code readability and modularity
"""

import re
import nltk
import string
import requests
import textstat
from bs4 import BeautifulSoup

nltk.download("punkt")
nltk.download("stopwords")


def scrape_webpage(url):
    try:
        response = requests.get(url)

        # raise an error for bad status codes
        response.raise_for_status()

        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # find title
        h1_tag = soup.find("h1", class_="entry-title") or soup.find(
            "h1", class_="tdb-title-text"
        )
        h1_text = h1_tag.get_text() if h1_tag else ""

        # find the text div
        target_div = soup.find("div", class_="td-post-content tagdiv-type")

        if not target_div:
            target_div_para = soup.find_all(
                "div",
                class_="td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type",
            )
            for i in target_div_para:
                target_div = i.find("div", class_="tdb-block-inner td-fix-index")

        # extract text from <p>, <ul> and <li> tags
        p_tags = target_div.find_all("p")
        ul_tags = target_div.find_all("ul")
        li_tags = target_div.find_all("li")

        # join the text from <p>, <ul> and <li> tags
        p_text = " ".join([p.get_text() for p in p_tags])
        ul_text = " ".join([ul.get_text() for ul in ul_tags])
        li_text = " ".join([li.get_text() for li in li_tags])

        # combine all the text
        return f"{h1_text}\n\n{p_text} {ul_text} {li_text}"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ''


def clean_text(text, stop_words):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])

    tokens = nltk.word_tokenize(text)
    cleaned_tokens = [word for word in tokens if word not in stop_words]

    return cleaned_tokens


def sentiment_scores(tokens, positive_words, negative_words):
    # positive score
    p_score = sum(1 for word in tokens if word in positive_words)
    # negative score
    n_score = sum(1 for word in tokens if word in negative_words)

    polarity_score = (p_score - n_score) / ((p_score + n_score) + 0.000001)
    subjectivity_score = (p_score + n_score) / (len(tokens) + 0.000001)

    return p_score, n_score, polarity_score, subjectivity_score


def average_words_per_sentence(text):
    sentences = nltk.sent_tokenize(text)
    total_words = len(nltk.word_tokenize(text))
    avg_words = total_words / (len(sentences) or 1)
    return avg_words


def average_word_length(cleaned_tokens):
    total_characters = sum(len(word) for word in cleaned_tokens)
    avg_word_length = total_characters / (len(cleaned_tokens) or 1)
    return avg_word_length


def is_complex_word(word):
    syllables = textstat.syllable_count(word)
    return syllables > 2


def count_personal_pronouns(text):
    pronouns = re.findall(r"\b(I|we|my|ours|us)\b", text, re.I)
    return len(pronouns)


def analyse_text(text, stop_words, positive_words, negative_words):
    cleaned_tokens = clean_text(text, stop_words)

    scores = sentiment_scores(cleaned_tokens, positive_words, negative_words)
    positive_score, negative_score, polarity_score, subjectivity_score = scores

    avg_words_per_sentence = average_words_per_sentence(text)
    avg_word_len = average_word_length(cleaned_tokens)
    average_sentence_length = avg_words_per_sentence * avg_word_len

    complex_words_count = sum(1 for word in cleaned_tokens if is_complex_word(word))
    complex_words_percentage = complex_words_count / (len(cleaned_tokens) or 1)

    fog_index = 0.4 * (average_sentence_length + complex_words_percentage)

    syllable_counts = sum(textstat.syllable_count(word) for word in cleaned_tokens)

    personal_pronouns_count = count_personal_pronouns(text)

    total_word_count = len(cleaned_tokens)

    return {
        "Positive Score": positive_score,
        "Negative Score": negative_score,
        "Polarity Score": polarity_score,
        "Subjectivity Score": subjectivity_score,
        "Average Sentence Length": average_sentence_length,
        "Percentage Complex Words": complex_words_percentage,
        "Fog Index": fog_index,
        "Average Words per Sentence": avg_words_per_sentence,
        "Complex Word Count": complex_words_count,
        "Total Word Count": total_word_count,
        "Syllable Counts": syllable_counts,
        "Personal Pronouns Count": personal_pronouns_count,
        "Average Word Length": avg_word_len,
    }


def read_text_file(path):
    with open(path, "r", encoding="iso-8859-1") as file:
        return file.read()
