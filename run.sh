#!/bin/bash

# Run the Flask app
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=0
export FLASK_RUN_PORT=5000

# Activate the virtual environment
. venv/bin/activate

# Run database migrations
python migrate.py

# Run Flask
flask run --host=0.0.0.0