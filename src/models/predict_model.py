# -*- coding: utf-8 -*-
import os
import sys
import joblib
import logging
from dotenv import load_dotenv, find_dotenv

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.features.preprocessing import preprocess_email_body

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def predict_email_class(email_body, vectorizer_filepath, model_filepath):
    """Preprocess, vectorize, and predict the class of a single email (spam or ham), including confidence score."""
    
    # Preprocess the email body
    logger.info("Preprocessing the input email body")
    processed_email_body = email_body.lower()  # Example preprocessing step

    # Load the trained vectorizer
    logger.info("Loading the trained vectorizer")
    vectorizer = joblib.load(vectorizer_filepath)
    
    # Vectorize the processed email body
    logger.info("Vectorizing the email")
    vectorized_email = vectorizer.transform([processed_email_body])
    
    # Load the trained model
    logger.info("Loading the trained model")
    model = joblib.load(model_filepath)
    
    # Make prediction and get the probabilities
    logger.info("Making prediction on the input email")
    prediction = model.predict(vectorized_email)
    prediction_proba = model.predict_proba(vectorized_email)

    # Extract the probability of the predicted class
    predicted_class = prediction[0]
    confidence = prediction_proba[0][predicted_class]  # Probability of the predicted class

    # Interpret prediction and return confidence
    label = "Spam" if predicted_class == 1 else "Ham"
    return label, confidence