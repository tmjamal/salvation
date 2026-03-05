#!/usr/bin/env python
import os
import sys

# Add project to path
project_home = '/home/LightOfLord/DAWA'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

# Import your Flask app
from app import app as application

# Production settings
application.config['DEBUG'] = False
application.config['ENV'] = 'production'
