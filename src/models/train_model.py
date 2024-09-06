# -*- coding: utf-8 -*-
import logging
import joblib
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from dotenv import load_dotenv, find_dotenv

# Configure logging
log_file = "logs/model_training.log"  # Log file to store logs
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

logger = logging.getLogger(__name__)

def evaluate_model(model, X_test, y_test):
    """Evaluate the model and return accuracy and classification report."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report

def train_naive_bayes(X_train, y_train, X_test, y_test):
    """Train a Naive Bayes model and evaluate its performance."""
    logger.info(f"Training Naive Bayes...")
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    accuracy, report = evaluate_model(model, X_test, y_test)
    
    logger.info(f"Accuracy for Naive Bayes: {accuracy:.4f}")
    logger.info(f"Classification Report for Naive Bayes:\n{report}")
    
    return model, accuracy

def main(train_filepath, test_filepath, model_filepath):
    """Main function to load data, train Naive Bayes model, and save the model."""
    
    # Load the training and testing datasets from pkl files
    logger.info(f"Loading training data from {train_filepath}")
    X_train, y_train = joblib.load(train_filepath)

    logger.info(f"Loading testing data from {test_filepath}")
    X_test, y_test = joblib.load(test_filepath)

    # Train Naive Bayes model
    model, accuracy = train_naive_bayes(X_train, y_train, X_test, y_test)

    # Save the trained model to disk
    logger.info(f"Saving the Naive Bayes model with accuracy {accuracy:.4f} to {model_filepath}")
    joblib.dump(model, model_filepath)

if __name__ == '__main__':
    load_dotenv(find_dotenv())

    # Define file paths
    train_filepath = os.getenv('TRAIN_FILE', 'data/processed/train_data.pkl')
    test_filepath = os.getenv('TEST_FILE', 'data/processed/test_data.pkl')
    model_filepath = os.getenv('MODEL_FILE', 'models/spam_classifier_model.pkl')

    # Execute the main function
    main(train_filepath, test_filepath, model_filepath)
