# Import necessary libraries
import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# Load and preprocess the data
def load_data(data_dir):
    data = []
    labels = []
    for category in ['pos', 'neg']:
        category_dir = os.path.join(data_dir, category)
        for filename in os.listdir(category_dir):
            with open(os.path.join(category_dir, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                data.append(preprocess_text(text))
                labels.append(1 if category == 'pos' else 0)
    return data, labels

# Preprocess text data
def preprocess_text(text):
    text = text.lower()
    text = re.sub('<[^<]+?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)  # Remove punctuation and special characters
    text = ' '.join(text.split())  # Remove extra whitespace
    return text

# Split the dataset into training and testing sets
def split_data(data, labels, test_size=0.2, random_state=42):
    return train_test_split(data, labels, test_size=test_size, random_state=random_state)

# TF-IDF Vectorization
def vectorize_data(train_data, test_data, max_features=5000):
    vectorizer = TfidfVectorizer(max_features=max_features)
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)
    return train_vectors, test_vectors

# Train a LinearSVC classifier
def train_classifier(train_vectors, labels):
    clf = LinearSVC()
    clf.fit(train_vectors, labels)
    return clf

# Evaluate the model
def evaluate_classifier(clf, test_vectors, test_labels):
    predictions = clf.predict(test_vectors)
    accuracy = accuracy_score(test_labels, predictions)
    precision = precision_score(test_labels, predictions)
    recall = recall_score(test_labels, predictions)
    f1 = f1_score(test_labels, predictions)
    return accuracy, precision, recall, f1

if __name__ == "__main__":
    data_dir = "aclImdb/train"  # Replace with the path to your dataset directory
    data, labels = load_data(data_dir)
    train_data, test_data, train_labels, test_labels = split_data(data, labels)
    train_vectors, test_vectors = vectorize_data(train_data, test_data)

    classifier = train_classifier(train_vectors, train_labels)
    accuracy, precision, recall, f1 = evaluate_classifier(classifier, test_vectors, test_labels)

    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")