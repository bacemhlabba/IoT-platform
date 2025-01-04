#!/bin/bash

# Run the Flask app
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=0
export FLASK_RUN_PORT=5000

# Activate the virtual environment
source venv/bin/activate

# Run Flask
venv/bin/flask run