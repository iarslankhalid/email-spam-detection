# -*- coding: utf-8 -*-
import os
import joblib
import logging
from dotenv import load_dotenv, find_dotenv

from src.features.preprocessing import preprocess_email_body

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def predict_email_class(email_body, vectorizer_filepath, model_filepath):
    """Preprocess, vectorize, and predict the class of a single email (spam or ham)."""
    
    # Preprocess the email body
    logger.info("Preprocessing the input email body")
    processed_email_body = preprocess_email_body(email_body)
    
    # Load the trained vectorizer
    logger.info("Loading the trained vectorizer")
    vectorizer = joblib.load(vectorizer_filepath)
    
    # Vectorize the processed email body
    logger.info("Vectorizing the email")
    vectorized_email = vectorizer.transform([processed_email_body]) 
    
    # Load the trained model
    logger.info("Loading the trained model")
    model = joblib.load(model_filepath)
    
    # Make prediction
    logger.info("Making prediction on the input email")
    prediction = model.predict(vectorized_email)

    # Interpret prediction
    if prediction[0] == 1:
        return "Spam"
    else:
        return "Ham"

if __name__ == '__main__':
    # Load environment variables from .env
    load_dotenv(find_dotenv())

    # Example email for prediction (you can replace this with a user input in a real deployment)
    email_body = "Free money!!! Claim your reward now."

    # Get the vectorizer and model file paths from the .env file
    vectorizer_filepath = os.getenv('PREDICTION_VECTORIZER', 'models/tfidf_vectorizer.pkl')  # Path to the saved vectorizer from .env
    model_filepath = os.getenv('PREDICTION_MODEL', 'models/spam_classifier_model.pkl')  # Path to the saved trained model from .env

    # Call the prediction function
    result = predict_email_class(email_body, vectorizer_filepath, model_filepath)
    print(f"The email is classified as: {result}")
