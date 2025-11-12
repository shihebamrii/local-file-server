# run_waitress.py
from waitress import serve
import app

if __name__ == '__main__':
    serve(app.app, host='0.0.0.0', port=int(__import__('os').environ.get('PORT', 8000)))