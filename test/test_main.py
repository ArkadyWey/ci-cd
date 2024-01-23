import pytest
from src.main import preprocess_text, vectorize_data

# Sample unit tests
def test_preprocess_text():
    text = "<p>This is a sample text with HTML tags.</p>"
    processed_text = preprocess_text(text)
    assert processed_text == "this is a sample text with html tags"

def test_vectorize_data():
    train_data = ["This is a sample sentence.", "Another sample sentence."]
    test_data = ["A new test sentence."]
    train_vectors, test_vectors = vectorize_data(train_data, test_data, max_features=10)
    assert train_vectors.shape[1] == test_vectors.shape[1] == 5


