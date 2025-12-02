"""
Configuration file for the Conversational AI
Adjust these settings to customize your AI assistant
"""

# ============================================
# AUDIO SETTINGS
# ============================================

# How many audio samples to read at a time
# Lower = more responsive but more CPU usage
CHUNK = 1024

# Audio format (16-bit is standard for speech)
# Don't change this unless you know what you're doing
FORMAT = "paInt16"

# Number of audio channels (1 = mono, 2 = stereo)
# Mono is fine for speech recognition
CHANNELS = 1

# Sample rate in Hz (16000 = 16kHz is good for speech)
# Higher = better quality but slower processing
RATE = 16000

# Volume threshold to detect speech (adjust if too sensitive)
# Lower number = more sensitive (picks up quieter sounds)
# Higher number = less sensitive (ignores background noise)
# Good range: 300-800
SILENCE_THRESHOLD = 500

# How many seconds of silence before stopping recording
# Lower = faster but might cut you off
# Higher = slower but more forgiving
SILENCE_DURATION = 2.0

# ============================================
# AI MODEL SETTINGS
# ============================================

# Speech-to-Text model (Whisper)
# Options: "tiny.en" (fastest), "base.en", "small.en", "medium.en"
# Larger models are more accurate but slower
WHISPER_MODEL = "tiny.en"

# Whisper device ("cpu" or "cuda" if you have an NVIDIA GPU)
WHISPER_DEVICE = "cpu"

# Whisper compute type
# Options: "int8" (fastest), "int16", "float16", "float32"
WHISPER_COMPUTE_TYPE = "int8"

# LLM Model (via Ollama)
# Options: "phi3.5" (recommended), "llama2", "mistral", "gemma"
# Run "ollama list" to see available models
OLLAMA_MODEL = "phi3.5"

# System prompt (defines AI personality and behavior)
# Make this whatever you want!
SYSTEM_PROMPT = """You are a helpful, concise AI assistant. 
Keep responses brief and conversational. 
Speak naturally as if talking to a friend."""

# ============================================
# TEXT-TO-SPEECH SETTINGS
# ============================================

# TTS Engine to use
# Options: "kokoro" (recommended), "piper" (faster but lower quality)
TTS_ENGINE = "kokoro"

# Kokoro voice (if using Kokoro)
# Check Kokoro documentation for available voices
KOKORO_VOICE = "default"

# ============================================
# PERFORMANCE SETTINGS
# ============================================

# Maximum response length from LLM (in tokens)
# Lower = faster responses, shorter answers
# Higher = slower responses, longer answers
MAX_TOKENS = 150

# Temperature for LLM (creativity setting)
# 0.0 = very deterministic (same answer every time)
# 1.0 = very creative (varied answers)
# Good range: 0.3-0.8
TEMPERATURE = 0.7

# Enable verbose logging (shows more details)
# True = show all details, False = minimal output
VERBOSE = True

# ============================================
# ADVANCED SETTINGS
# ============================================

# Number of parallel beams for Whisper transcription
# Higher = more accurate but slower
# 1 = fastest (recommended for speed)
WHISPER_BEAM_SIZE = 1

# Enable VAD (Voice Activity Detection) filter
# Can improve accuracy in noisy environments
WHISPER_VAD_FILTER = False

# Condition on previous text in Whisper
# Can improve accuracy for continuous conversation
WHISPER_CONDITION_ON_PREVIOUS_TEXT = False

# ============================================
# EXPERIMENTAL SETTINGS
# ============================================

# Auto-adjust silence threshold based on ambient noise
# (Not yet implemented)
AUTO_ADJUST_THRESHOLD = False

# Save conversation history to file
# (Not yet implemented)
SAVE_CONVERSATION = False

# Conversation history file path
HISTORY_FILE = "conversation_history.txt"

