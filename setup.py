import os
import subprocess

# Define the file paths
model_file_path = 'models/spam_classifier_model.pkl'
vectorizer_file_path = 'models/tfidf_vectorizer.pkl'
train_data_file_path = 'data/processed/train_data.pkl'
test_data_file_path = 'data/processed/test_data.pkl'
train_model_script = 'src/models/train_model.py'
build_features_script = 'src/features/build_features.py'

def check_file_exists(file_path):
    """Check if a file exists at the specified path."""
    exists = os.path.exists(file_path)
    print(f"Checking if {file_path} exists: {exists}")
    return exists

def run_script(script_path):
    """Run a Python script using subprocess."""
    try:
        print(f"Running script: {script_path}")
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e}")
        exit(1)

if __name__ == "__main__":
    print("Starting setup...")

    # Step 1: Check if model and vectorizer files exist
    model_exists = check_file_exists(model_file_path)
    vectorizer_exists = check_file_exists(vectorizer_file_path)

    if model_exists and vectorizer_exists:
        print("Model and vectorizer already exist. No need to retrain.")
    else:
        # Step 2: Check if train and test data files exist
        train_data_exists = check_file_exists(train_data_file_path)
        test_data_exists = check_file_exists(test_data_file_path)

        if train_data_exists and test_data_exists:
            print("Train and test data found. Training the model...")
            run_script(train_model_script)
        else:
            # Step 3: Run the feature-building script
            print("Train and test data not found. Building features first...")
            run_script(build_features_script)

            # After building features, train the model
            print("Now training the model...")
            run_script(train_model_script)

    print("Setup completed.")
