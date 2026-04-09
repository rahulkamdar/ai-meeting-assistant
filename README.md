# AI Meeting Assistant 🎙️

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Automated audio transcription with speaker diarization and translation. Supports 99+ languages with automatic translation to English.

## Features

- **Speaker Diarization**: Automatically identifies and labels different speakers
- **Multi-Language Support**: Works with 99+ languages (Gujarati, Hindi, Spanish, etc.)
- **Auto-Translation**: Translate non-English audio to English while preserving speaker labels
- **High-Quality Transcription**: Uses OpenAI Whisper
- **Privacy-First**: All processing happens locally in Docker
- **Simple CLI**: Just specify the language code

## Quick Start

### 1. Clone and Build
```bash
git clone https://github.com/rahulkamdar/ai-meeting-assistant.git
cd ai-meeting-assistant
docker build -t transcriber .
```

### 2. Run
```bash
# Set your Hugging Face token
export HF_TOKEN="your_hf_token_here"

# Auto-detect language
./transcribe.sh audio.m4a

# Gujarati → English
./transcribe.sh audio.m4a gu

# Spanish → English
./transcribe.sh audio.m4a es
```

## Usage
```bash
./transcribe.sh <audio-file> [language-code]
```

**Arguments:**
- `audio-file`: Path to your audio recording
- `language-code` (optional): Source language - auto-translates to English
  - `gu` - Gujarati
  - `hi` - Hindi  
  - `es` - Spanish
  - `fr` - French
  - [See all 99+ languages](https://github.com/openai/whisper#available-models-and-languages)

**Examples:**
```bash
# Auto-detect (transcribe in original language)
./transcribe.sh meeting.m4a

# Gujarati audio → English transcript with speakers
./transcribe.sh financial_call.m4a gu

# Spanish audio → English transcript with speakers
./transcribe.sh client_meeting.m4a es
```

## How It Works

1. **Audio Conversion**: Converts to WAV format
2. **Speaker Diarization**: Identifies who spoke when (pyannote.audio)
3. **Translation**: Translates to English if language code specified
4. **Transcription**: High-quality speech-to-text (Whisper)
5. **Output**: Speaker-labeled English transcript

## Example Output

Input: Gujarati audio with 2 speakers  
Command: `./transcribe.sh meeting.m4a gu`
```
[SPEAKER_00] Good morning, how are you today?
[SPEAKER_01] I am doing well, thank you for asking.
[SPEAKER_00] Let's discuss the financial planning details.
[SPEAKER_01] Yes, I have prepared the documents.
```

## Prerequisites

- Docker Desktop ([Download](https://www.docker.com/products/docker-desktop))
- Hugging Face account ([Get token](https://huggingface.co/settings/tokens))

## Supported Audio Formats

- `.m4a`, `.mp3`, `.wav`, `.mp4`
- Any format supported by FFmpeg

## Privacy & Security

- ✅ All processing happens locally in Docker
- ✅ Audio never leaves your machine
- ✅ No cloud processing required
- ✅ Free for transcription/translation (only Whisper + pyannote)

## Optional: AI Analysis

After transcription, you can analyze with LLMs:
```bash
# Setup (one-time)
cp config/config.example.yaml config/config.yaml
# Add your OpenAI/Anthropic API key to config.yaml

# Analyze transcript
python src/analyze_transcript.py audio_transcript.txt
```

Get summaries, action items, and Q&A from your transcripts.

## Troubleshooting

**"HF_TOKEN not set"**
```bash
export HF_TOKEN="your_huggingface_token"
```

**Docker build fails**
```bash
docker system prune -a -f
docker build --no-cache -t transcriber .
```

## Contributing

Contributions welcome! Open an issue or submit a PR.

## License

MIT License - see [LICENSE](LICENSE)

## Acknowledgments

- [pyannote.audio](https://github.com/pyannote/pyannote-audio) - Speaker diarization
- [OpenAI Whisper](https://github.com/openai/whisper) - Transcription & translation

---

⭐ Star this repo if you find it useful!

## Troubleshooting

### TypeError: got an unexpected keyword argument 'use_auth_token'

This is fixed in the latest version. If you cloned an older version:

```bash
docker build --no-cache -t transcriber .
```

The pinned dependency versions in `requirements.txt` resolve compatibility issues between pyannote.audio, speechbrain, and huggingface-hub.
