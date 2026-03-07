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

print("Testing database connection...")

# Test database connection first
from app import app, db

with app.app_context():
    try:
        # Test if we can query verses
        verse_count = db.session.execute('SELECT COUNT(*) FROM verses').scalar()
        print(f"Database connected! Found {verse_count} verses")
        
        # Test daily verse logic
        from datetime import datetime
        day_of_year = datetime.now().timetuple().tm_yday
        verse_index = day_of_year % verse_count if verse_count > 0 else 0
        print(f"Today is day {day_of_year}, verse index {verse_index}")
        
        # Test verse query
        from app import Verse
        daily_verse = Verse.query.offset(verse_index).first()
        if daily_verse:
            print(f"Daily verse found: {daily_verse.verse_number}")
            print(f"Content: {daily_verse.translation_ml[:50]}...")
        else:
            print("No verse found")
            
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()

print("Starting Flask app...")

# Import your Flask app
from app import app

# Export for gunicorn
application = app

if __name__ == "__main__":
    app.run(debug=True, port=5000)
