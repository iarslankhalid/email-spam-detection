import sys
import os
import joblib
import random
import tkinter as tk
from tkinter import messagebox

# Add the root directory to sys.path so that Python can find the src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models.predict_model import predict_email_class  # Now this import will work

# Load the trained vectorizer and model
vectorizer_filepath = 'models/tfidf_vectorizer.pkl'  # Path to the saved vectorizer file
model_filepath = 'models/spam_classifier_model.pkl'  # Updated model file path

def clear_prediction(event):
    """Clear the prediction label when the email body is changed."""
    prediction_label.config(text="")

def predict_spam():
    """Predict whether the email is spam or not, and show the confidence score."""
    email_body = email_entry.get("1.0", 'end-1c').strip()
    if not email_body:
        messagebox.showwarning("Input Error", "Please enter an email body!")
        return

    # Call the prediction function with the file paths, not loaded objects
    try:
        label, confidence = predict_email_class(email_body, vectorizer_filepath, model_filepath)
        prediction_label.config(text=f"Prediction: {label} (Confidence: {confidence:.2f})")
        update_example_texts()  # Change examples after each prediction
    except Exception as e:
        prediction_label.config(text=f"Error: {str(e)}")

def load_random_example(file_path):
    """Load a random email example from the provided file."""
    with open(file_path, 'r') as f:
        emails = f.read().strip().split("\n\n")
    
    return random.choice(emails)  # Return a random email from the file

def update_example_texts():
    """Update the examples in the spam and ham text boxes with new random examples."""
    spam_example = load_random_example('data/example-emails/spam_emails.txt')
    ham_example = load_random_example('data/example-emails/ham_emails.txt')

    # Update spam example text
    spam_text.config(state=tk.NORMAL)  # Enable editing temporarily
    spam_text.delete(1.0, tk.END)  # Clear existing content
    spam_text.insert(tk.END, spam_example)  # Insert new random example
    spam_text.config(state=tk.DISABLED)  # Disable editing

    # Update ham example text
    ham_text.config(state=tk.NORMAL)
    ham_text.delete(1.0, tk.END)
    ham_text.insert(tk.END, ham_example)
    ham_text.config(state=tk.DISABLED)

# Create the GUI
root = tk.Tk()
root.title("Email Spam Prediction")

# Configure layout
root.geometry('900x500')  # Set the window size
root.configure(bg="#f4f4f9")

# Font settings
header_font = ("Arial", 16, "bold")
subheader_font = ("Arial", 12, "bold")
normal_font = ("Arial", 12)

# Create a grid-based layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Email body input area in the center
input_frame = tk.Frame(root, bg="#f4f4f9", padx=20, pady=20)
input_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(input_frame, text="Enter the email body:", font=header_font, bg="#f4f4f9").pack(pady=10)
email_entry = tk.Text(input_frame, height=10, width=50, font=normal_font, bg="#ffffff", bd=0, relief="flat")
email_entry.pack(pady=10)

# Add a listener to clear the prediction when the email body is modified
email_entry.bind("<Key>", clear_prediction)

# Predict button at the bottom center
predict_button = tk.Button(input_frame, text="Predict Spam", font=subheader_font, bg="#4caf50", fg="white", padx=10, pady=5, relief="flat", command=predict_spam)
predict_button.pack(pady=10)

# Label to display the prediction result
prediction_label = tk.Label(input_frame, text="", font=normal_font, bg="#f4f4f9")
prediction_label.pack(pady=20)

# Right panel for examples of spam and ham
example_frame = tk.Frame(root, bg="#f4f4f9", padx=20, pady=20)
example_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

tk.Label(example_frame, text="Examples of Spam and Ham", font=header_font, bg="#f4f4f9").pack(pady=10)

# Spam example panel
spam_example_frame = tk.Frame(example_frame, bg="#f9f9f9", padx=10, pady=10, bd=2, relief="groove")
spam_example_frame.pack(fill="both", pady=10)

tk.Label(spam_example_frame, text="Spam Example:", font=subheader_font, bg="#f9f9f9").pack(anchor="w")
spam_text = tk.Text(spam_example_frame, height=5, width=40, wrap='word', font=normal_font, bg="#ffffff", bd=0, relief="flat")
spam_text.pack(pady=5)

# Ham example panel
ham_example_frame = tk.Frame(example_frame, bg="#f9f9f9", padx=10, pady=10, bd=2, relief="groove")
ham_example_frame.pack(fill="both", pady=10)

tk.Label(ham_example_frame, text="Ham Example:", font=subheader_font, bg="#f9f9f9").pack(anchor="w")
ham_text = tk.Text(ham_example_frame, height=5, width=40, wrap='word', font=normal_font, bg="#ffffff", bd=0, relief="flat")
ham_text.pack(pady=5)

# Update the text boxes with random examples when the app starts
update_example_texts()

# Run the GUI loop
root.mainloop()
