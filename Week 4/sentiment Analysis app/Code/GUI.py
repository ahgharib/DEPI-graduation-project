import tkinter as tk
from tkinter import messagebox
import spacy
import os
import sys
from joblib import load
import string
from spacy.lang.en.stop_words import STOP_WORDS

# Set model path (account for PyInstaller packed model)
if getattr(sys, 'frozen', False):  # If running from the executable
    model_path = os.path.join(sys._MEIPASS, "en_core_web_sm")
    print("Running in frozen mode, model path:", model_path)
else:
    model_path = "en_core_web_sm"  # For development or regular Python environment
    print("Running in development mode, model path:", model_path)

# Load the spaCy model
nlp = spacy.load(model_path)


if getattr(sys, 'frozen', False):  # If running from an .exe
    model_path1 = os.path.join(sys._MEIPASS, 'trained_model.joblib')
else:  # For development or normal execution
    model_path1 = os.path.join(os.path.dirname(__file__), 'trained_model.joblib')

model = load(model_path1)

#Preprocessing from ML code
punc = string.punctuation
stopwords = list(STOP_WORDS)

def data_cleaning(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower().strip() if token.lemma_ != "-PRON-" else token.lower_ for token in doc]
    cleaned_tokens = [token for token in tokens if token not in stopwords and token not in punc]
    return " ".join(cleaned_tokens)

#prediction
def predict_sentiment(text):
    cleaned_text = data_cleaning(text)
    prediction = model.predict([cleaned_text])[0]
    return prediction

# Function for button click
def classify_text():
    user_input = text_entry.get("1.0", "end-1c")  # To Get text from input field
    if not user_input.strip():
        messagebox.showwarning("Input Error", "Please enter some text.")
        return
    
    sentiment_score = predict_sentiment(user_input)
    
    sentiment_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    result_label.config(text=f"Sentiment: {sentiment_map.get(sentiment_score, 'Unknown')}", fg="blue")

# Create the GUI
root = tk.Tk()
root.title("Sentiment Analysis App")
text_label = tk.Label(root, text="Enter your text:")
text_label.pack(pady=10)
text_entry = tk.Text(root, height=5, width=50)
text_entry.pack(pady=10)
classify_button = tk.Button(root, text="Classify", command=classify_text)
classify_button.pack(pady=10)
result_label = tk.Label(root, text="Sentiment: ", font=("Arial", 12))
result_label.pack(pady=10)
root.mainloop()
