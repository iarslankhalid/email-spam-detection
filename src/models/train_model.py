# -*- coding: utf-8 -*-
import logging
import joblib
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
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

def train_models(X_train, y_train, X_test, y_test):
    """Train multiple models and return the best performing model."""
    models = {
        "Naive Bayes": MultinomialNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(),
        "SVM": SVC()
    }
    
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    for model_name, model in models.items():
        logger.info(f"Training {model_name}...")
        model.fit(X_train, y_train)
        accuracy, report = evaluate_model(model, X_test, y_test)
        
        logger.info(f"Accuracy for {model_name}: {accuracy:.4f}")
        logger.info(f"Classification Report for {model_name}:\n{report}")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = model_name
    
    logger.info(f"Best model is {best_model_name} with accuracy: {best_accuracy:.4f}")
    return best_model, best_model_name, best_accuracy

def main(train_filepath, test_filepath, model_filepath):
    """Main function to load data, train models, and save the best performing model."""
    
    # Load the training and testing datasets from pkl files
    logger.info(f"Loading training data from {train_filepath}")
    X_train, y_train = joblib.load(train_filepath)

    logger.info(f"Loading testing data from {test_filepath}")
    X_test, y_test = joblib.load(test_filepath)

    # Train models and select the best one
    best_model, best_model_name, best_accuracy = train_models(X_train, y_train, X_test, y_test)

    # Save the best model to disk
    logger.info(f"Saving the best model ({best_model_name}) with accuracy {best_accuracy:.4f} to {model_filepath}")
    joblib.dump(best_model, model_filepath)

if __name__ == '__main__':
    load_dotenv(find_dotenv())

    # Define file paths
    train_filepath = os.getenv('TRAIN_FILE', 'data/processed/train_data.pkl')
    test_filepath = os.getenv('TEST_FILE', 'data/processed/test_data.pkl')
    model_filepath = os.getenv('MODEL_FILE', 'models/best_model.pkl')

    # Execute the main function
    main(train_filepath, test_filepath, model_filepath)
