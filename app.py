from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from werkzeug.utils import secure_filename
import os
from urllib.parse import unquote
from dotenv import load_dotenv, dotenv_values
import random, string
from functools import wraps

# Load .env
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

# Generate a new random password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Read env or create .env if missing
env_data = dotenv_values(ENV_FILE)
new_password = generate_password()
PASSWORD = new_password

# Update .env with new password
if not env_data or env_data.get("ADMIN_PASSWORD") != PASSWORD:
    with open(ENV_FILE, "a") as f:
        f.write(f"\nADMIN_PASSWORD={PASSWORD}\n")

print(f"New admin password generated: {PASSWORD}")

# Config
ROOT_DIR = os.environ.get("ROOT_DIR", "C:\\")  # Root directory to serve
# Use a dedicated uploads folder for writable files to avoid PermissionError
UPLOAD_FOLDER = os.path.join(ROOT_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = None  # None = allow all
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200MB max
SECRET_KEY = os.environ.get("FLASK_SECRET", "dev-secret-change-me")

# Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Helpers
def allowed_file(filename):
    if ALLOWED_EXT is None:
        return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# Auth decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('browse', req_path=''))
        flash('Wrong password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
@login_required
def browse(req_path):
    req_path = unquote(req_path)
    abs_path = os.path.abspath(os.path.join(ROOT_DIR, req_path))

    if not abs_path.startswith(os.path.abspath(ROOT_DIR)):
        return "Access denied", 403

    if os.path.isdir(abs_path):
        dirs = []
        files = []
        for f in sorted(os.listdir(abs_path)):
            if os.path.isdir(os.path.join(abs_path, f)):
                dirs.append(f)
            else:
                files.append(f)
        parent_path = os.path.relpath(os.path.join(abs_path, '..'), ROOT_DIR)
        if parent_path == '.':
            parent_path = ''
        return render_template('index.html', dirs=dirs, files=files, current_path=req_path, parent_path=parent_path)
    else:
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=True)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    req_path = request.form.get('current_path', '')
    # Force uploads to the dedicated UPLOAD_FOLDER to avoid permission issues
    abs_path = os.path.join(UPLOAD_FOLDER, req_path)
    os.makedirs(abs_path, exist_ok=True)

    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('browse', req_path=req_path))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('browse', req_path=req_path))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        target = os.path.join(abs_path, filename)
        file.save(target)
        flash(f'Uploaded {filename} to uploads folder')

    return redirect(url_for('browse', req_path=req_path))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)