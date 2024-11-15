# Blackcoffer Blog Sentiment Analysis

## Objective

The objective of this document is to explain the methodology adopted to perform text analysis to derive sentimental opinions, sentiment scores, readability, passive words, personal pronouns, and other related metrics.

## Table of Contents

1. [Sentimental Analysis](#sentimental-analysis)
   - [Cleaning using Stop Words Lists](#cleaning-using-stop-words-lists)
   - [Creating Dictionary of Positive and Negative Words](#creating-dictionary-of-positive-and-negative-words)
   - [Extracting Derived Variables](#extracting-derived-variables)
2. [Analysis of Readability](#analysis-of-readability)
3. [Average Number of Words Per Sentence](#average-number-of-words-per-sentence)
4. [Complex Word Count](#complex-word-count)
5. [Word Count](#word-count)
6. [Syllable Count Per Word](#syllable-count-per-word)
7. [Personal Pronouns](#personal-pronouns)
8. [Average Word Length](#average-word-length)

## Sentimental Analysis

Sentimental analysis involves determining whether a piece of writing is positive, negative, or neutral. The methodology below is designed for use in financial texts and includes:

### Cleaning using Stop Words Lists

The Stop Words Lists (found in the folder `StopWords`) are used to clean the text by excluding words found in the stop words list. This helps in focusing on meaningful words for sentiment analysis.

### Creating Dictionary of Positive and Negative Words

The Master Dictionary (found in the folder `MasterDictionary`) is used to create dictionaries of positive and negative words. Only words not found in the stop words lists are added to these dictionaries.

### Extracting Derived Variables

Text is converted into a list of tokens using the `nltk` tokenize module. The following variables are calculated:

- **Positive Score**: The total count of words found in the Positive Dictionary, each assigned a value of +1.
- **Negative Score**: The total count of words found in the Negative Dictionary, each assigned a value of -1. The score is then multiplied by -1 to ensure a positive number.
- **Polarity Score**: Calculated using the formula:
  \[
  \text{Polarity Score} = \frac{\text{Positive Score} - \text{Negative Score}}{\text{Positive Score} + \text{Negative Score} + 0.000001}
  \]
  Range: -1 to +1
- **Subjectivity Score**: Calculated using the formula:
  \[
  \text{Subjectivity Score} = \frac{\text{Positive Score} + \text{Negative Score}}{\text{Total Words after cleaning} + 0.000001}
  \]
  Range: 0 to +1

## Analysis of Readability

Readability is calculated using the Gunning Fog Index with the following formulas:

- **Average Sentence Length** = Number of words / Number of sentences
- **Percentage of Complex Words** = Number of complex words / Number of words
- **Fog Index** = 0.4 * (Average Sentence Length + Percentage of Complex Words)

## Average Number of Words Per Sentence

Calculated using the formula:
\[
\text{Average Number of Words Per Sentence} = \frac{\text{Total Number of Words}}{\text{Total Number of Sentences}}
\]

## Complex Word Count

Complex words are defined as words with more than two syllables.

## Word Count

Total cleaned words are counted by:
1. Removing stop words (using `stopwords` class from `nltk` package).
2. Removing punctuations (e.g., `?`, `!`, `,`, `.`).

## Syllable Count Per Word

The number of syllables in each word is counted based on vowels. Exceptions, such as words ending in "es" or "ed," are handled appropriately.

## Personal Pronouns

Personal pronouns are identified using regex to count occurrences of "I," "we," "my," "ours," and "us," while excluding the country name "US."

## Average Word Length

Calculated using the formula:
\[
\text{Average Word Length} = \frac{\text{Sum of Total Number of Characters in Each Word}}{\text{Total Number of Words}}
\]

## Data Extraction and NLP

[Website](https://blackcoffer.com)

#### Objective

Extracted textual data from articles at given URLs and perform text analysis to compute the variables described below.

#### Data Extraction

- **Input File**: `Input.xlsx`
- Extracted text from articles, saving each in a text file named `URL_ID.txt`.
- Ensuring only the article title and text are extracted, excluding website headers, footers, etc.


#### Data Analysis

- Analyzed each extracted text according to the variables specified in `Output Data Structure.xlsx`.
- Output saved in `Output Data Structure.xlsx`.



