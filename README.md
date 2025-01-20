# NLP Feedback Analysis

## 📌 Project Overview
This project is an **NLP-based Student Feedback Analysis System** that processes survey feedback using natural language processing (NLP) techniques. It analyzes text responses from student feedback surveys, classifies sentiments, and extracts key insights to help educators understand student experiences.

## 🚀 Features
- Preprocessing of student feedback text (tokenization, stopword removal, lemmatization, etc.)
- Sentiment analysis using **Bidirectional LSTM**
- Word embeddings with **GloVe** (Global Vectors for Word Representation)
- **K-Fold Cross-Validation** for model evaluation
- Visualization of results with **Confusion Matrix**

Tech Stack;
      Backend:Flask (Python-based web framework)
              TensorFlow & Keras (Deep learning framework)
              NLTK (Natural Language Toolkit for text preprocessing)
              Pandas & NumPy (Data processing)
     Frontend:HTML, CSS, JavaScript (for UI)
     Database:SQLite 


## 📂 Project Structure
```
NLP-Feedback-Analysis/
│── data/
│   ├── dataset.xlsx
│── models/
│   ├── sentiment_lstm_model.h5
│── src/
│   ├── preprocess.py
│   ├── train.py
│   ├── predict.py
│── app_new.py
│── requirements.txt
│── README.md
```

Usage
Upload student feedback data via the web interface.
View analysis results including sentiment classification.
Utilize visualization tools for better insights.
