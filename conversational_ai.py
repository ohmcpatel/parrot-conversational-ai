#!/usr/bin/env python3
"""
Fast Local Conversational AI Demo
Uses: Faster-Whisper (STT) + Ollama (LLM) + Piper (TTS)
"""

import os
import subprocess
import tempfile
import time
import wave

import numpy as np
import ollama
import pyaudio

# Import the AI components
from faster_whisper import WhisperModel

# ============================================
# CONFIGURATION
# ============================================

# Audio recording settings
CHUNK = 1024  # How many audio samples to read at a time
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio (1 channel)
RATE = 16000  # Sample rate: 16kHz (good for speech)
SILENCE_THRESHOLD = 500  # Volume level to detect silence
SILENCE_DURATION = 2  # Seconds of silence before stopping recording

# AI Model settings
WHISPER_MODEL = "tiny.en"  # Fast English-only model
OLLAMA_MODEL = "phi3.5"  # The LLM model name
SYSTEM_PROMPT = """You are a friendly parrot personal assistant! Your name is Polly and you're here to help. 
You're enthusiastic, cheerful, and occasionally squawk with excitement. 
You greet people with 'Squawk! What's up!' and you're very helpful with tasks.
Keep your responses brief and conversational (2-3 sentences max).
You love to help but also add a bit of parrot personality - maybe repeat an important word or add 'squawk' when excited.
Remember: you're a helpful parrot, not just mimicking - you actually understand and assist!"""

# ============================================
# STEP 1: Initialize the AI Models
# ============================================

print("🔧 Loading AI models (this may take a moment)...")

# Load Whisper model for Speech-to-Text
# compute_type="int8" makes it faster on CPU
whisper_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print("✅ Whisper STT loaded")

# Piper TTS will be called via command line
# Check if piper is installed and voice model exists
try:
    subprocess.run(["piper", "--help"], capture_output=True, check=True)
    voice_model_path = os.path.join(os.path.dirname(__file__), "voices", "en_US-lessac-medium.onnx")
    if os.path.exists(voice_model_path):
        print("✅ Piper TTS ready")
    else:
        print("⚠️  Piper TTS installed but voice model missing")
        print("   Voice model should be at: voices/en_US-lessac-medium.onnx")
        print("   Continuing anyway (will print responses if TTS fails)")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("❌ Piper TTS not found. Install with: pip install piper-tts")
    exit(1)

# Check if Ollama is running and model is available
try:
    ollama.list()
    print("✅ Ollama LLM ready")
except Exception:
    print("❌ Ollama not running. Start it with: ollama serve")
    print(f"   Then install model with: ollama pull {OLLAMA_MODEL}")
    exit(1)

print("\n🎤 Conversational AI Ready!\n")

# ============================================
# STEP 2: Audio Recording Function
# ============================================


def record_audio_until_silence():
    """
    Records audio from the microphone until silence is detected.
    Returns the path to the saved audio file.
    """
    print("🎙️  Listening... (speak now, I'll stop when you're done)")

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the microphone stream
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    frames = []  # Store audio data here
    silent_chunks = 0
    recording_started = False

    while True:
        # Read audio data from microphone
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert audio data to numbers to check volume
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()

        # If volume is above threshold, we're recording
        if volume > SILENCE_THRESHOLD:
            recording_started = True
            silent_chunks = 0
        elif recording_started:
            silent_chunks += 1

        # If silent for too long, stop recording
        silence_seconds = (silent_chunks * CHUNK) / RATE
        if recording_started and silence_seconds > SILENCE_DURATION:
            break

    # Clean up
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wf = wave.open(temp_file.name, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    print("✅ Recording complete")
    return temp_file.name


# ============================================
# STEP 3: Speech-to-Text Function
# ============================================


def transcribe_audio(audio_file_path):
    """
    Converts audio file to text using Faster-Whisper.
    Returns the transcribed text.
    """
    print("🧠 Transcribing your speech...")
    start_time = time.time()

    # Run Whisper transcription
    segments, info = whisper_model.transcribe(
        audio_file_path,
        beam_size=1,  # Faster but slightly less accurate
        language="en",
    )

    # Combine all segments into one text
    text = " ".join([segment.text for segment in segments]).strip()

    elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
    print(f"✅ Transcribed in {elapsed:.0f}ms: '{text}'")

    return text


# ============================================
# STEP 4: LLM Response Function
# ============================================


def get_llm_response(user_text):
    """
    Gets a response from the Ollama LLM.
    Returns the AI's text response.
    """
    print("💭 Thinking...")
    start_time = time.time()

    # Send message to Ollama
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )

    ai_response = response["message"]["content"].strip()

    elapsed = (time.time() - start_time) * 1000
    print(f"✅ LLM responded in {elapsed:.0f}ms")
    print(f"🤖 AI says: {ai_response}")

    return ai_response


# ============================================
# STEP 5: Text-to-Speech Function
# ============================================


def speak_text(text):
    """
    Converts text to speech using Piper TTS and plays it.
    """
    print("🔊 Speaking...")
    start_time = time.time()

    # Create temporary file for the speech audio
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio.close()

    # Path to the voice model
    voice_model = os.path.join(os.path.dirname(__file__), "voices", "en_US-lessac-medium.onnx")

    # Run Piper TTS to generate speech
    # Pass generated text as stdin, without interpreting it as shell syntax
    result = subprocess.run(
        ["piper", "--model", voice_model, "--output_file", temp_audio.name],
        input=text,
        text=True,
        check=False,
        capture_output=True,
    )

    # Check if the file was created and has content
    if os.path.exists(temp_audio.name) and os.path.getsize(temp_audio.name) > 0:
        # Play the audio using afplay (macOS)
        subprocess.run(["afplay", temp_audio.name], check=True)
        elapsed = (time.time() - start_time) * 1000
        print(f"✅ Speech completed in {elapsed:.0f}ms\n")
    else:
        # If piper fails, just print the text
        print(f"⚠️  TTS failed, text response: {text}")
        if result.stderr:
            print(f"   Error: {result.stderr}\n")

    # Clean up
    try:
        os.unlink(temp_audio.name)
    except:
        pass


# ============================================
# STEP 6: Main Conversation Loop
# ============================================


def main():
    """
    Main function that runs the conversational loop.
    """
    print("=" * 50)
    print("CONVERSATIONAL AI - Press Ctrl+C to exit")
    print("=" * 50)
    print()

    conversation_count = 0

    try:
        while True:
            conversation_count += 1
            print(f"\n--- Turn {conversation_count} ---")

            # Step 1: Record user's voice
            audio_file = record_audio_until_silence()

            # Step 2: Convert speech to text
            user_text = transcribe_audio(audio_file)
            os.unlink(audio_file)  # Delete temp audio file

            # Skip if nothing was said
            if not user_text or len(user_text) < 2:
                print("⚠️  Didn't catch that, try again")
                continue

            # Step 3: Get LLM response
            ai_response = get_llm_response(user_text)

            # Step 4: Speak the response
            speak_text(ai_response)

            # Show ready for next turn
            print("Ready for next question...")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


# ============================================
# RUN THE PROGRAM
# ============================================

if __name__ == "__main__":
    main()
