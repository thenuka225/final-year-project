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

Usage:
Upload student feedback data via the web interface.
View analysis results including sentiment classification.
Utilize visualization tools for better insights.

![Home - NLP Feedback Analysis - Google Chrome 20_01_2025 20_45_30](https://github.com/user-attachments/assets/6f22840e-4850-461a-b0ea-f41b3f5a9826)

![Home - NLP Feedback Analysis - Google Chrome 20_01_2025 20_46_10](https://github.com/user-attachments/assets/e7cb757c-6416-41a5-a816-feff3aab4e7e)

![Home - NLP Feedback Analysis - Google Chrome 20_01_2025 20_45_51](https://github.com/user-attachments/assets/1aa83fd5-2a43-4174-9abf-65fd8e5acde2)

![Home - NLP Feedback Analysis - Google Chrome 20_01_2025 20_45_38](https://github.com/user-attachments/assets/c55f5676-2769-4dab-b23d-4ea17155bea6)

![Sentiment Analysis Result - Google Chrome 06_01_2025 23_59_50](https://github.com/user-attachments/assets/6dbecd22-0661-40ad-a40c-f7a6b458abd3)

![Sentiment Analysis Result - Google Chrome 06_01_2025 23_49_59](https://github.com/user-attachments/assets/de7a20d2-969a-4fbe-8340-314d11499526)

![Sentiment Analysis Result - Google Chrome 06_01_2025 23_48_15](https://github.com/user-attachments/assets/9f498994-4494-489e-9e96-5853ee207955)


