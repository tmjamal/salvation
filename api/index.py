#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import your Flask app
from app import app

# Set environment variables for Vercel
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///islamic_site.db')

# Export the app for Vercel
application = app

if __name__ == "__main__":
    app.run()
