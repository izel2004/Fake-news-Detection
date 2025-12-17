#!/bin/bash

echo "Starting Fake News Detection System..."

# Step 1: Create virtual environment
python -m venv venv

# Step 2: Activate virtual environment
source venv/bin/activate

# Step 3: Install required packages
pip install --upgrade pip
pip install flask pandas scikit-learn

# Step 4: Train the model
echo "Training model using fake.csv and true.csv..."
python model.py

# Step 5: Run the Flask app
echo "Running website..."
python app.py
