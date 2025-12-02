#!/usr/bin/env python3
"""
Test script to verify all components are working
Run this before running the full conversational AI
"""

import sys

print("🧪 Testing Conversational AI Components...\n")

# Test 1: Faster-Whisper
print("1️⃣  Testing Faster-Whisper (STT)...")
try:
    from faster_whisper import WhisperModel

    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    print("   ✅ Faster-Whisper loaded successfully")
except Exception as e:
    print(f"   ❌ Error loading Faster-Whisper: {e}")
    print("   Fix: pip install faster-whisper")
    sys.exit(1)

# Test 2: Ollama
print("\n2️⃣  Testing Ollama (LLM)...")
try:
    import ollama

    models = ollama.list()
    print("   ✅ Ollama is running")

    # Check if phi3.5 is available
    if hasattr(models, "models"):
        model_names = [m.model for m in models.models]
    elif isinstance(models, dict) and "models" in models:
        model_names = [m.get("model", m.get("name", "")) for m in models["models"]]
    else:
        model_names = []

    if any("phi3.5" in name for name in model_names):
        print("   ✅ Phi-3.5 model is available")
    else:
        print("   ⚠️  Phi-3.5 model not found")
        print("   Run: ollama pull phi3.5")
except Exception as e:
    print(f"   ❌ Error connecting to Ollama: {e}")
    print("   Fix: Start Ollama with 'ollama serve'")
    sys.exit(1)

# Test 3: Piper TTS
print("\n3️⃣  Testing Piper TTS...")
try:
    import subprocess

    result = subprocess.run(["piper", "--help"], capture_output=True, check=True)
    print("   ✅ Piper TTS is installed")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("   ❌ Piper TTS not found")
    print("   Fix: pip install piper-tts")
    sys.exit(1)

# Test 4: PyAudio
print("\n4️⃣  Testing PyAudio (Microphone)...")
try:
    import pyaudio

    audio = pyaudio.PyAudio()

    # Check if there's at least one input device
    input_devices = []
    for i in range(audio.get_device_count()):
        dev_info = audio.get_device_info_by_index(i)
        if dev_info["maxInputChannels"] > 0:
            input_devices.append(dev_info["name"])

    audio.terminate()

    if input_devices:
        print(f"   ✅ PyAudio loaded, found {len(input_devices)} input device(s)")
        print(f"   📱 Using: {input_devices[0]}")
    else:
        print("   ⚠️  No input devices found")
        print("   Check microphone connection and permissions")
except Exception as e:
    print(f"   ❌ Error with PyAudio: {e}")
    print("   Fix (macOS): brew install portaudio && pip install pyaudio")
    print("   Fix (Linux): sudo apt-get install portaudio19-dev && pip install pyaudio")
    sys.exit(1)

# Quick LLM test
print("\n5️⃣  Testing LLM response speed...")
try:
    import time

    import ollama

    start = time.time()
    response = ollama.chat(model="phi3.5", messages=[{"role": "user", "content": "Hi"}])
    elapsed = (time.time() - start) * 1000

    print(f"   ✅ LLM responded in {elapsed:.0f}ms")
    print(f"   🤖 Response: {response['message']['content'][:50]}...")
except Exception as e:
    print(f"   ⚠️  Could not test LLM: {e}")

print("\n" + "=" * 50)
print("✅ All components are ready!")
print("=" * 50)
print("\nYou can now run: python conversational_ai.py")
