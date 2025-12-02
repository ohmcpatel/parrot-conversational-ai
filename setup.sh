#!/bin/bash
# Setup script for Fast Local Conversational AI

echo "🚀 Setting up Fast Local Conversational AI..."
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "📦 Activating virtual environment..."
    source bird/bin/activate
fi

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Piper TTS is already in requirements.txt
echo "🔊 Piper TTS installed from requirements"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "⚠️  Ollama is not installed!"
    echo "Please install it from: https://ollama.ai/download"
    echo "Or run: brew install ollama"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434 &> /dev/null; then
    echo ""
    echo "⚠️  Ollama is not running!"
    echo "Please start it in another terminal with: ollama serve"
    echo "Then run this setup script again."
    exit 1
fi

# Pull the Phi-3.5 model
echo "🧠 Downloading Phi-3.5 model (this may take a few minutes)..."
ollama pull phi3.5

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the conversational AI:"
echo "  python conversational_ai.py"
echo ""

