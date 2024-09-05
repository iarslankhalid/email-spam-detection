# -*- coding: utf-8 -*-
import logging
import pandas as pd
import os
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv, find_dotenv

from preprocessing import preprocess_email_body

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Function to vectorize text using TF-IDF
def vectorize_text(texts):
    """Vectorizes the input texts using TF-IDF."""
    logging.info("Vectorizing the email bodies using TF-IDF")

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)

    logging.info(f"Vectorization complete with {X.shape[1]} features")

    return X, vectorizer


def main(input_filepath, output_processed_filepath, output_vectorized_filepath):
    """ Preprocess and vectorize the email body from the parsed email CSV. """
    logger = logging.getLogger(__name__)

    # Load the CSV file with parsed emails
    logger.info(f"Reading parsed emails from {input_filepath}")
    df = pd.read_csv(input_filepath)

    # Preprocess the 'Body' column
    logger.info(f"Preprocessing email bodies")
    df['Processed_Body'] = df['Body'].apply(preprocess_email_body)

    # Save the preprocessed email bodies to a new CSV
    logger.info(f"Saving preprocessed email bodies to {output_processed_filepath}")
    df[['Filename', 'Processed_Body']].to_csv(output_processed_filepath, index=False)

    # Vectorize the preprocessed email bodies
    email_bodies = df['Processed_Body'].tolist()
    X, vectorizer = vectorize_text(email_bodies)

    # Save the vectorized features as a CSV (optional: you can also save as a sparse matrix)
    logger.info(f"Saving vectorized email bodies to {output_vectorized_filepath}")
    pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out()).to_csv(output_vectorized_filepath,
                                                                                 index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    # Define file paths (these can be passed in the future as arguments via click or from .env)
    input_filepath = os.getenv('INPUT_PARSED_EMAILS_CSV', 'data/processed/parsed_emails.csv')
    output_processed_filepath = os.getenv('OUTPUT_PROCESSED_EMAILS_CSV', 'data/interim/processed_emails.csv')
    output_vectorized_filepath = os.getenv('OUTPUT_VECTORIZED_EMAILS_CSV', 'data/interim/vectorized_emails.csv')

    # Execute the main function
    main(input_filepath, output_processed_filepath, output_vectorized_filepath)
