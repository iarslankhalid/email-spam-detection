# -*- coding: utf-8 -*-
import logging
import pandas as pd
import os
import joblib
from dotenv import load_dotenv, find_dotenv

from preprocessing import preprocess_email_body
from over_sampling import oversampling_data
from train_test_split import train_data_split
from vectorizing import vectorize_text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(input_filepath, output_processed_filepath, train_filepath, test_filepath, vectorizer_filepath):
    """ Preprocess, vectorize, oversample, and split the data for model training/testing. """
    
    logger.info(f"Reading parsed emails from {input_filepath}")
    df = pd.read_csv(input_filepath)

    df['Body'] = df['Body'].fillna('')

    logger.info(f"Preprocessing email bodies")
    df['Processed_Body'] = df['Body'].apply(preprocess_email_body)

    logger.info(f"Saving preprocessed email bodies to {output_processed_filepath}")
    df[['Filename', 'Processed_Body']].to_csv(output_processed_filepath, index=False)

    email_bodies = df['Processed_Body'].tolist()
    labels = df['Label'].tolist()

    X, y, vectorizer = vectorize_text(email_bodies, labels)

    logger.info(f"Oversampling the data...")
    X_resampled, y_resampled = oversampling_data(X, y)

    logger.info(f"Splitting data into training and testing sets")
    X_train, X_test, y_train, y_test = train_data_split(X_resampled, y_resampled)

    logger.info(f"Saving training data to {train_filepath}")
    joblib.dump((X_train, y_train), train_filepath)

    logger.info(f"Saving testing data to {test_filepath}")
    joblib.dump((X_test, y_test), test_filepath)

    logger.info(f"Saving vectorizer to {vectorizer_filepath}")
    joblib.dump(vectorizer, vectorizer_filepath)


if __name__ == '__main__':
    load_dotenv(find_dotenv())

    # Define file paths (these can be passed as arguments or via .env)
    input_filepath = os.getenv('INPUT_FILE', 'data/interim/parsed_emails.csv')
    output_processed_filepath = os.getenv('OUTPUT_PROCESSED_FILE', 'data/processed/processed_email.csv')
    train_filepath = os.getenv('TRAIN_FILE', 'data/processed/train_data.pkl')
    test_filepath = os.getenv('TEST_FILE', 'data/processed/test_data.pkl')
    vectorizer_filepath = os.getenv('VECTORIZER_FILE', 'models/tfidf_vectorizer.pkl')

    # Execute the main function
    main(input_filepath, output_processed_filepath, train_filepath, test_filepath, vectorizer_filepath)
