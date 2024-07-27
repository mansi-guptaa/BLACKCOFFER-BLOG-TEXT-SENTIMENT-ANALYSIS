"""
Before running this program please ensure that required packages are installed
To install all required packages, run "pip install -r requirements.txt"
To run the program, run "python main.py".
"""

import os
import pandas as pd

from lib import analyse_text, read_text_file, scrape_webpage


INPUT_EXCEL_FILE = "Input.xlsx"
OUTPUT_EXCEL_FILE = "Output.xlsx"

OUTPUT_TEXT_DIR = "ScrapedTextFiles"
MASTER_DICT_DIR = "MasterDictionary"
STOP_WORDS_DIR = "StopWords"


# load input file
df = pd.read_excel(INPUT_EXCEL_FILE)

# create output directory if not exists
os.makedirs(OUTPUT_TEXT_DIR, exist_ok=True)

# scrape webpages & save scraped text to files
for _, df_row in df.iterrows():
    url = df_row.get("URL")
    text = scrape_webpage(url)

    url_id = df_row.get("URL_ID")
    path = os.path.join(OUTPUT_TEXT_DIR, url_id)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


# load stop words
stop_words = set()
for filename in os.listdir(STOP_WORDS_DIR):
    path = os.path.join(STOP_WORDS_DIR, filename)
    stop_words.update(read_text_file(path).splitlines())

# load postive words
positive_words_file = os.path.join(MASTER_DICT_DIR, "positive-words.txt")
positive_words = set(read_text_file(positive_words_file).splitlines())

# load negative words
negative_words_file = os.path.join(MASTER_DICT_DIR, "negative-words.txt")
negative_words = set(read_text_file(negative_words_file).splitlines())


# analyse text files
for filename in os.listdir(OUTPUT_TEXT_DIR):
    path = os.path.join(OUTPUT_TEXT_DIR, filename)
    text = read_text_file(path)

    analysis = analyse_text(text, stop_words, positive_words, negative_words)

    # update corresponding dataframe row with analysis data
    row_index = df["URL_ID"] == filename
    for column, value in analysis.items():
        df.loc[row_index, column] = value


# save to output file
df.to_excel(OUTPUT_EXCEL_FILE)
