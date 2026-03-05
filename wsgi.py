#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Add your project directory to the Python path
project_home = '/home/LightOfLord/DAWA'  # Your PythonAnywhere project path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Change to the project directory
os.chdir(project_home)

# Import your Flask app
from app import app as application

# Make sure app is in production mode
application.config['DEBUG'] = False
application.config['ENV'] = 'production'

# Set secret key for production
application.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
