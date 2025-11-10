#!/bin/bash

# EvoTransformer Dashboard Startup Script
# This script sets up and starts the customer dashboard

echo "=========================================="
echo "  EvoTransformer Customer Dashboard      "
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

echo ""
echo "=========================================="
echo "🚀 Starting Dashboard Server..."
echo "=========================================="
echo ""
echo "📊 Dashboard URL: http://localhost:5000"
echo "🔌 API Endpoints: http://localhost:5000/api/*"
echo "💚 Health Check: http://localhost:5000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py
