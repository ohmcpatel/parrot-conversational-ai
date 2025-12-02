# 🦜 Polly - Your Voice AI Parrot Assistant

Talk to an AI with your voice, and it talks back! Everything runs locally on your computer - no internet required, completely private.

**Total setup time: 10 minutes**

---

## 🎯 What You'll Get

A voice AI assistant named Polly that:
- 🎤 Listens to your voice
- 🧠 Understands what you said
- 💭 Thinks of helpful responses
- 🔊 Speaks back to you

**Speed:** ~150ms response time (faster than blinking!)

---

## 📋 Requirements

- **Mac computer** (macOS)
- **Python 3.9 or higher** (probably already installed)
- **10 GB free disk space** (for AI models)
- **Working microphone**

---

## 🚀 Complete Setup Guide

### Step 1: Install Homebrew (if you don't have it)

Open Terminal (`Command + Space`, type "Terminal", press Enter) and paste this:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Press Enter and follow the prompts. (If you already have Homebrew, skip to Step 2)

---

### Step 2: Install Ollama

Ollama is the AI brain. Install it with:

```bash
brew install ollama
```

---

### Step 3: Download This Project

If you're reading this, you probably already have it! Just make sure you're in the project folder:

```bash
cd /Users/ohmpatel/Developer/Exploration/bird
```

---

### Step 4: Install PortAudio

This lets Python access your microphone:

```bash
brew install portaudio
```

---

### Step 5: Activate the Virtual Environment

The project already has a Python virtual environment set up. Activate it:

```bash
python3 -m venv bird
source bird/bin/activate
```

You should see `(bird)` appear at the start of your terminal prompt.

---

### Step 6: Install Python Packages

Install all the required packages:

```bash
pip install -r requirements.txt
```

This will take 2-3 minutes. You'll see lots of text scrolling - that's normal!

---

### Step 7: Download the AI Brain Model

In a **NEW terminal window** (keep the first one open), start Ollama:

```bash
ollama serve
```

**Keep this terminal open!** You'll see "Listening on 127.0.0.1:11434" - that's good!

In your **original terminal** (the one with `(bird)` showing), download the AI model:

```bash
ollama pull phi3.5
```

This downloads a 2.2 GB AI model. Takes 2-5 minutes depending on your internet.

---

### Step 8: Download the Voice Model

Download the voice that Polly will use to speak:

```bash
mkdir -p voices
cd voices
curl -L -o en_US-lessac-medium.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
curl -L -o en_US-lessac-medium.onnx.json "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
cd ..
```

This downloads a 60 MB voice file.

---

### Step 9: Allow Microphone Access

When you first run the program, macOS will ask for microphone permission:
1. Click "OK" or "Allow"
2. If you accidentally clicked "Don't Allow":
   - Go to System Preferences → Security & Privacy → Microphone
   - Check the box next to "Terminal"

---

### Step 10: Test Everything

Make sure everything works:

```bash
python test_components.py
```

You should see all ✅ checkmarks. If you see any ❌, read the error message for what to fix.

---

## 🎤 How to Run Polly

### Every time you want to use Polly:

**Terminal Window 1** (if not already running):
```bash
ollama serve
```

**Terminal Window 2** (your main terminal):
```bash
cd /Users/ohmpatel/Developer/Exploration/bird
source bird/bin/activate
python conversational_ai.py
```

Wait a few seconds for models to load, then you'll see:
```
🔧 Loading AI models...
✅ Whisper STT loaded
✅ Ollama LLM ready
✅ Piper TTS ready

🎤 Conversational AI Ready!

--- Turn 1 ---
🎙️ Listening... (speak now, I'll stop when you're done)
```

---

## 💬 How to Talk to Polly

1. **Wait** for "🎙️ Listening..."
2. **Speak** your question clearly (Example: "Hey Polly, what's the weather like?")
3. **Stop talking** - Polly will automatically detect 2 seconds of silence
4. **Listen** - Polly will respond with voice!

### Example Questions:
- "Hey Polly, what's up?"
- "Tell me a joke"
- "What is Python programming?"
- "What's 125 times 8?"
- "Explain quantum physics simply"
- "Can you help me plan my day?"

### Tips:
- Speak clearly
- Be in a quiet room
- Don't whisper
- First response takes 2-3 seconds (loading), then it's super fast!

---

## 🛑 How to Stop

Press `Control + C` (Ctrl+C) to exit

---

## 🎨 Customize Polly's Personality

Want to change how Polly talks? Edit the file `conversational_ai.py`:

1. Open it in any text editor
2. Find line 30 (looks like `SYSTEM_PROMPT = ...`)
3. Change the text to whatever personality you want!

**Examples:**

**Pirate Mode:**
```python
SYSTEM_PROMPT = "You are a pirate assistant. Say 'Arrr!' and speak like a pirate captain. Keep responses brief and fun!"
```

**Robot Mode:**
```python
SYSTEM_PROMPT = "You are a helpful robot assistant. Speak logically and precisely. Keep responses brief."
```

**Professional Mode:**
```python
SYSTEM_PROMPT = "You are a professional business assistant. Be polite, formal, and concise."
```

---

## ⚙️ Advanced Settings

Open `conversational_ai.py` to adjust:

### Microphone Sensitivity (Line 24)
```python
SILENCE_THRESHOLD = 500
```
- **Lower number** (300-400) = More sensitive, picks up quieter sounds
- **Higher number** (600-800) = Less sensitive, ignores background noise

### Auto-Stop Timer (Line 25)
```python
SILENCE_DURATION = 2
```
- Increase to 3 or 4 if Polly cuts you off mid-sentence
- Decrease to 1.5 if you want faster response

### AI Model (Line 28)
```python
OLLAMA_MODEL = "phi3.5"
```
- Try other models: `llama2`, `mistral`, `gemma`
- Run `ollama list` to see installed models
- Download new ones with `ollama pull model-name`

---

## 🐛 Troubleshooting

### "Ollama not running"
**Problem:** The AI brain isn't started  
**Solution:** 
```bash
# Open a new terminal and run:
ollama serve
```
Keep that terminal open!

---

### "No audio input device" or "Microphone not working"
**Problem:** macOS blocked microphone access  
**Solution:**
1. Go to System Preferences → Security & Privacy → Microphone
2. Make sure "Terminal" is checked
3. Restart the program

---

### "Cuts me off mid-sentence"
**Problem:** Auto-stop is too aggressive  
**Solution:** Edit line 25 in `conversational_ai.py`:
```python
SILENCE_DURATION = 3  # or 4
```

---

### "Can't hear Polly's voice"
**Problem:** Voice model missing or TTS failed  
**Solution:**
```bash
# Check if voice model exists:
ls voices/en_US-lessac-medium.onnx

# If it doesn't exist, download it:
mkdir -p voices && cd voices
curl -L -o en_US-lessac-medium.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
curl -L -o en_US-lessac-medium.onnx.json "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
cd ..
```

---

### "Too slow" or "Takes forever"
**Problem:** First run is always slower  
**Solution:** 
- First question: 2-3 seconds (models loading)
- Every question after: ~150-200ms (super fast!)
- This is normal behavior

---

### "PyAudio installation failed"
**Problem:** PortAudio library not installed  
**Solution:**
```bash
brew install portaudio
pip install --force-reinstall pyaudio
```

---

### "Command not found: ollama"
**Problem:** Ollama not installed or not in PATH  
**Solution:**
```bash
brew install ollama
# If that doesn't work, download from: https://ollama.ai
```

---

## 🔧 How It Works (Behind the Scenes)

```
You speak "What's the weather?"
         ↓
[Faster-Whisper] Converts speech → text (~40ms)
         ↓
[Phi-3.5 AI] Generates response (~50ms)
         ↓
[Piper TTS] Converts text → speech (~50ms)
         ↓
You hear: "Squawk! The weather is..."

Total: ~150ms (faster than blinking!)
```

### The Tech Stack:
- **Faster-Whisper** - Speech recognition (tiny.en model)
- **Phi-3.5** - AI brain via Ollama
- **Piper TTS** - Text-to-speech (Lessac voice)
- **PyAudio** - Microphone access
- **100% Local** - No internet, completely private

---

## 📁 Project Structure

```
bird/
├── conversational_ai.py    # Main program (run this!)
├── test_components.py      # Tests if everything works
├── requirements.txt        # Python packages needed
├── config.py              # All settings in one place
├── setup.sh               # Automated setup script
├── voices/                # Voice models folder
│   └── en_US-lessac-medium.onnx
└── bird/                  # Virtual environment
```

---

## 🚨 Quick Start Cheat Sheet

```bash
# Terminal 1 - Start AI brain (keep open)
ollama serve

# Terminal 2 - Run Polly
cd /Users/ohmpatel/Developer/Exploration/bird
source bird/bin/activate
python conversational_ai.py

# To stop: Press Control+C
```

---

## 💡 Pro Tips

1. **First run is slow** - Models need to load. After that, it's lightning fast!
2. **Quiet room** - Works best without background noise
3. **Clear speech** - Don't whisper, don't shout, just talk normally
4. **Wait for silence** - Let it detect you're done (2 seconds of quiet)
5. **Experiment!** - Try different questions, change the personality, have fun!

---

## 🎓 Learning Resources

Want to understand the code better?

- **conversational_ai.py** - Heavily commented code explaining every part
- **config.py** - All customizable settings explained
- Each function has detailed comments for beginners

---

## 🙏 Credits

Built with these amazing open-source projects:
- **Faster-Whisper** by Systran
- **Phi-3.5** by Microsoft
- **Ollama** by Ollama team
- **Piper TTS** by Rhasspy

---

## 📝 Notes

- All processing happens on YOUR computer
- No data sent to the cloud
- Completely private and secure
- Works offline (after initial downloads)
- Models total ~2.3 GB of disk space

---

## 🎉 You're Done!

Run this and start talking to Polly:

```bash
cd /Users/ohmpatel/Developer/Exploration/bird
source bird/bin/activate
python conversational_ai.py
```

**Squawk! Polly is ready to help! 🦜✨**

---

## ❓ Need Help?

If you're stuck:
1. Read the Troubleshooting section above
2. Check that `ollama serve` is running
3. Try `python test_components.py` to see what's wrong
4. Make sure you followed all steps in order

Happy chatting! 🦜

