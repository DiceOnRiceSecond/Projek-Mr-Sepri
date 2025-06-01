from flask import Flask
from models import db
from controllers.auth_controller import auth_bp
from controllers.morse_controller import morse_bp
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



app.register_blueprint(auth_bp)
app.register_blueprint(morse_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

