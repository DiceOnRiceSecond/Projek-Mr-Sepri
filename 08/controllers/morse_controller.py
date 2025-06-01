from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User, Translation, db

morse_bp = Blueprint('morse', __name__)

MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.',  'F': '..-.', 'G': '--.',  'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-',  'L': '.-..',
    'M': '--', 'N': '-.',   'O': '---',  'P': '.--.',
    'Q': '--.-','R': '.-.', 'S': '...',  'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--','Z': '--..', '1': '.----', '2': '..---',
    '3': '...--','4': '....-','5': '.....', '6': '-....',
    '7': '--...','8': '---..','9': '----.','0': '-----'
}

REVERSE_MORSE = {v: k for k, v in MORSE_DICT.items()}

@morse_bp.route('/')
def home():
    user = None
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
    return render_template('index.html', user=user)

@morse_bp.route('/learn')
def learn():
    return render_template('learn.html', morse_dict=MORSE_DICT)

@morse_bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    result = None
    if request.method == "POST":
        text = request.form["text"].upper()
        morse = " ".join(MORSE_DICT.get(char, '?') for char in text if char != " ")
        result = morse

        if 'username' in session:
            user = User.query.filter_by(username=session['username']).first()
            if user:
                translation = Translation(
                    user_id=user.id,
                    input_text=text,
                    output_text=result,
                    mode='encode'
                )
                db.session.add(translation)
                db.session.commit()

    return render_template('quiz.html', result=result)

@morse_bp.route('/decode', methods=['GET', 'POST'])
def decode():
    result = None
    if request.method == 'POST':
        morse_input = request.form['morse'].strip()
        decoded_words = []
        words = morse_input.split(' / ')
        for word in words:
            letters = word.split()
            decoded_word = ''.join(REVERSE_MORSE.get(letter, '?') for letter in letters)
            decoded_words.append(decoded_word)
        result = ' '.join(decoded_words)

        if 'username' in session:
            user = User.query.filter_by(username=session['username']).first()
            if user:
                translation = Translation(
                    user_id=user.id,
                    input_text=morse_input,
                    output_text=result,
                    mode='decode'
                )
                db.session.add(translation)
                db.session.commit()

    return render_template('decode.html', result=result)

@morse_bp.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['username']).first()
    translations = Translation.query.filter_by(user_id=user.id).order_by(Translation.timestamp.desc()).all()
    return render_template('history.html', translations=translations)
