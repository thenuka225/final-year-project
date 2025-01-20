from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import tensorflow as tf
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import nltk
from nltk.corpus import stopwords


# Load model and tokenizer
model = tf.keras.models.load_model('sentiment_lstm_model_old.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey')

# Database setup
DATABASE = 'reviews.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    with app.app_context():
        db = get_db()
        db.executescript('''
            CREATE TABLE IF NOT EXISTS lecturers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lecturer_id INTEGER NOT NULL,
                review TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                FOREIGN KEY (lecturer_id) REFERENCES lecturers(id)
            );
        ''')
        db.commit()

nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

def analyze_sentiment(review):
    review = preprocess_text(review)
    if not review.strip():
        return "Error: Review input is empty."

    review_sequence = tokenizer.texts_to_sequences([review])
    if not review_sequence or len(review_sequence[0]) == 0:
        return "Error: Review could not be tokenized."

    review_padded = pad_sequences(review_sequence, maxlen=model.input_shape[1], padding='post')

    try:
        sentiment_score = model.predict(review_padded)[0]
        confidence = max(sentiment_score)
        predicted_class = sentiment_score.argmax()
        sentiment = {0: 'negative', 1: 'neutral', 2: 'positive'}.get(predicted_class, 'unknown')
        return f"{sentiment} ({confidence * 100:.2f}%)"
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return "Error: An error occurred during prediction."

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student', methods=['GET', 'POST'])
def student():
    db = get_db()
    lecturers = db.execute('SELECT id, username FROM lecturers').fetchall()

    if request.method == 'POST':
        review = request.form.get('review')
        lecturer_id = request.form.get('lecturer_id')
        if not review.strip():
            return "Error: Review input is empty.", 400
        if not lecturer_id:
            return "Error: No lecturer selected.", 400

        sentiment = analyze_sentiment(review)
        try:
            db.execute('INSERT INTO reviews (lecturer_id, review, sentiment) VALUES (?, ?, ?)', 
                       (lecturer_id, review, sentiment))
            db.commit()
        except sqlite3.Error as e:
            print(f"Database insert error: {e}")
            return "Error: Unable to store review.", 500

        return render_template('result.html', sentiment=sentiment)

    return render_template('student_review_form.html', lecturers=lecturers)

@app.route('/lecturer', methods=['GET', 'POST'])
def lecturer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        lecturer = db.execute('SELECT * FROM lecturers WHERE username = ?', (username,)).fetchone()
        if lecturer and check_password_hash(lecturer['password'], password):
            session['lecturer_id'] = lecturer['id']
            flash('Login successful!', 'success')
            return redirect(url_for('lecturer_dashboard'))
        flash('Invalid login', 'error')
    return render_template('lecturer_login.html')

@app.route('/lecturer/dashboard')
def lecturer_dashboard():
    if 'lecturer_id' not in session:
        return redirect(url_for('lecturer_login'))

    lecturer_id = session['lecturer_id']
    db = get_db()
    lecturer = db.execute('SELECT username FROM lecturers WHERE id = ?', (lecturer_id,)).fetchone()
    reviews = db.execute('SELECT sentiment, COUNT(*) AS count FROM reviews WHERE lecturer_id = ? GROUP BY sentiment',
                         (lecturer_id,)).fetchall()
    
    sentiment_counts = {row['sentiment']: row['count'] for row in reviews}
    total_reviews = sum(sentiment_counts.values())
    sentiment_percentages = {sentiment: (count / total_reviews) * 100 if total_reviews else 0 
                             for sentiment, count in sentiment_counts.items()}

    return render_template('lecturer_dashboard.html', 
                           lecturer_username=lecturer['username'] if lecturer else None,
                           sentiment_percentages=sentiment_percentages,
                           sentiment_counts=sentiment_counts,
                           total_reviews=total_reviews)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        db = get_db()
        try:
            db.execute('INSERT INTO lecturers (username, password) VALUES (?, ?)', (username, hashed_password))
            db.commit()
            flash('Account created successfully!')
            return redirect(url_for('lecturer_login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('lecturer_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
