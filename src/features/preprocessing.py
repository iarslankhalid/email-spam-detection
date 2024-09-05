import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stemmer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))

def preprocess_email_body(body, l=stemmer, stop_words=stopwords):
    # 1. Lowercasing
    body = body.lower()

    # 2. Remove punctuation
    body = re.sub(r'[^\w\s]', '', body)

    # 3. Tokenization
    tokens = word_tokenize(body)

    # 4. Remove stop words and perform stemming
    processed_tokens = [l.lemmatize(word) for word in tokens if word not in stop_words]

    # Join tokens back into a string
    output = ' '.join(processed_tokens)
    return output