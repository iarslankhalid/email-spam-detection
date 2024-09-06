from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

vectorizer = TfidfVectorizer(max_features=5000)

def vectorize_text(email_bodies: list, labels: list, vectorizer: TfidfVectorizer = vectorizer):
    vectorized_emails = vectorizer.fit_transform(email_bodies).toarray()
    y = np.array(labels)
    
    return vectorized_emails, y, vectorizer