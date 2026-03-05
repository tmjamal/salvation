#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Prophet, Companion, and Ruler models to the database
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from datetime import datetime

def add_prophet_models():
    """Add Prophet, Companion, and Ruler models to the existing database"""
    with app.app_context():
        # Add Prophet model
        db.engine.execute("""
        CREATE TABLE IF NOT EXISTS prophets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_arabic TEXT NOT NULL,
            name_ml TEXT NOT NULL,
            name_en TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            birthplace TEXT,
            period TEXT,
            description_ml TEXT,
            full_content_ml TEXT,
            order_num INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Add Companion model
        db.engine.execute("""
        CREATE TABLE IF NOT EXISTS companions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_arabic TEXT NOT NULL,
            name_ml TEXT NOT NULL,
            name_en TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            birth_year INTEGER,
            death_year INTEGER,
            birthplace TEXT,
            description_ml TEXT,
            full_content_ml TEXT,
            is_featured BOOLEAN DEFAULT 0,
            order_num INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Add Ruler model
        db.engine.execute("""
        CREATE TABLE IF NOT EXISTS rulers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_arabic TEXT NOT NULL,
            name_ml TEXT NOT NULL,
            name_en TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            dynasty TEXT,
            reign_start INTEGER,
            reign_end INTEGER,
            capital TEXT,
            description_ml TEXT,
            full_content_ml TEXT,
            order_num INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        print("Successfully added Prophet, Companion, and Ruler tables")

if __name__ == '__main__':
    add_prophet_models()
