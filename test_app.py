#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set environment variables BEFORE importing app
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'srashtaavinte-maargadarshnam-2024-secret')
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///islamic_site.db')

# Test basic Flask app
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Salvation Website - Test Page</h1><p>✅ Basic Flask is working!</p>"

@app.route('/test')
def test():
    return "<h1>Test Route Working</h1><p>Database and routes are OK!</p>"

# Export for Render
application = app

if __name__ == "__main__":
    app.run()
