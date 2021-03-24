"""Demonstrates how to make a simple call to the Natural Language API."""

import argparse

from google.cloud import language_v1

import os
import csv

# %matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set display row/column to show all data
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def write_result_to_csv(annotations, filename):
    """Create CSV filename to write results to"""
    csv_filename = os.path.splitext(filename)[0] + "_sentences_score.csv"
    print("CSV filename: " + csv_filename)

    """Create a new file if it does not exist"""
    with open(csv_filename, mode='w') as csv_file:
        fieldnames = ['SentenceIndex', 'SentenceText', 'SentenceSentiment']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for index, sentence in enumerate(annotations.sentences):
            sentence_sentiment = sentence.sentiment.score
            print(
                "Sentence {} has a sentiment score of {}".format(index, sentence_sentiment)
            )

            # print(sentence.text.content)

            writer.writerow({'SentenceIndex': index, 'SentenceText': sentence.text.content, 'SentenceSentiment': sentence_sentiment})

    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    print(
        "Overall Sentiment: score of {} with magnitude of {}".format(score, magnitude)
    )
    # return 0

    return csv_filename


def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print(
            "Sentence {} has a sentiment score of {}".format(index, sentence_sentiment)
        )

    print(
        "Overall Sentiment: score of {} with magnitude of {}".format(score, magnitude)
    )
    return 0


def analyze(filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language_v1.LanguageServiceClient()

    with open(filename, "r") as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request={'document': document})

    # Print the results
    # print_result(annotations)

    # Write sentence scores to csv
    csv_filename = write_result_to_csv(annotations, filename)

    # text = document.content

    # read csv data into dataframe
    sentence_scores = pd.read_csv(csv_filename)
    print(sentence_scores)

    # describe the sentence sentiments
    sentence_sentiments = sentence_scores.SentenceSentiment.describe()
    print(sentence_sentiments)

    # plot max temp. vs month
    sentence_scores.plot(kind='line', y='SentenceSentiment', x='SentenceIndex')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "filename",
        help="The filename of the article you'd like to analyze.",
    )
    args = parser.parse_args()

    analyze(args.filename)
