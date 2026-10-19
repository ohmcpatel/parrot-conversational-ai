# Polly

A local voice assistant for macOS. Speak into the microphone; Polly transcribes your question, generates a short reply, and reads it aloud.

```text
Microphone → faster-whisper → Phi-3.5 via Ollama → Piper → Speaker
```

The runtime uses local models after the initial downloads. This is a small, single-turn prototype: each reply receives the system prompt and current utterance, without conversation history or web access.

## Run locally

Requires macOS, Python 3.11, a microphone, and [Ollama](https://ollama.com). Audio playback currently uses macOS `afplay`.

```bash
git clone https://github.com/ohmcpatel/parrot-conversational-ai.git
cd parrot-conversational-ai
brew install portaudio ollama
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start Ollama in a separate terminal:

```bash
ollama serve
```

Then download the language model and run the assistant:

```bash
ollama pull phi3.5
python test_components.py
python conversational_ai.py
```

The repository includes the Piper Lessac voice files in `voices/`. Whisper's `tiny.en` model downloads on first use. Allow microphone access for your terminal, speak after the listening prompt, and press **Ctrl+C** to stop.

## Settings

Edit the constants at the top of [conversational_ai.py](conversational_ai.py):

| Setting | Default |
| --- | --- |
| Speech recognition | `tiny.en`, CPU int8 |
| Language model | `phi3.5` |
| End-of-turn silence | 2 seconds |
| Microphone silence threshold | 500 |
| Personality | `SYSTEM_PROMPT` |

`config.py` contains reference settings, but the main script currently uses its own constants.

## Practical limits

- English speech recognition; one utterance at a time.
- The silence detector can cut off a slow speaker or wait too long in a noisy room.
- End-to-end latency depends on your machine, model, and utterance, and includes the silence window. No fixed response-time guarantee is claimed.
- Generated text is printed if voice output fails. Check the Piper executable, bundled voice path, and macOS audio output first.

Built with [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [Ollama](https://github.com/ollama/ollama), Microsoft's Phi-3.5, and Piper TTS.
