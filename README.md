# AI Meeting Assistant 🎙️

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An automated audio transcription and speaker diarization tool with AI-powered analysis. Upload your meeting recordings and get speaker-labeled transcripts, summaries, action items, and insights.

## Features

- **Speaker Diarization**: Automatically identifies and labels different speakers
- **High-Quality Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- **AI Analysis**: Leverage GPT-4, Claude, or other LLMs to:
  - Summarize conversations
  - Extract action items and decisions
  - Answer questions about the transcript
- **Docker-Based**: Runs consistently across all platforms
- **Privacy-First**: Processes everything locally, only sends transcripts to LLM if you choose

## Prerequisites

- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- Hugging Face account and API token ([Get one here](https://huggingface.co/settings/tokens))
- (Optional) API key for your preferred LLM:
  - [OpenAI API](https://platform.openai.com/api-keys)
  - [Anthropic API](https://console.anthropic.com/)
  - [OpenRouter](https://openrouter.ai/keys)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rahulkamdar/ai-meeting-assistant.git
cd ai-meeting-assistant
```

### 2. Set Up Configuration
```bash
# Copy example config
cp config/config.example.yaml config/config.yaml

# Edit with your API keys
nano config/config.yaml
```

### 3. Build Docker Image
```bash
docker build -t meeting-assistant .
```

### 4. Run Transcription
```bash
# Set your Hugging Face token
export HF_TOKEN="your_hf_token_here"

# Transcribe an audio file
./transcribe.sh path/to/your/audio.m4a
```

### 5. Analyze with AI (Optional)
```bash
# After transcription completes
python src/analyze_transcript.py path/to/your/audio_transcript.txt
```

## Configuration

Edit `config/config.yaml` to customize:
```yaml
# LLM Provider (openai, anthropic, openrouter)
llm_provider: "openai"

# Model selection
model: "gpt-4-turbo-preview"  # or "claude-3-opus-20240229"

# Analysis options
analysis:
  generate_summary: true
  extract_action_items: true
  answer_questions: true
```

## Project Structure
```
ai-meeting-assistant/
├── src/
│   ├── process_audio.py      # Core transcription logic
│   └── analyze_transcript.py # LLM analysis
├── config/
│   ├── config.example.yaml   # Example configuration
│   └── config.yaml           # Your config (gitignored)
├── docs/
│   ├── USAGE.md             # Detailed usage guide
│   └── API.md               # API integration details
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
└── transcribe.sh           # Main execution script
```

## How It Works

1. **Audio Conversion**: Converts input audio to WAV format for processing
2. **Speaker Diarization**: Uses pyannote.audio to identify speaker segments
3. **Transcription**: OpenAI Whisper transcribes each segment
4. **Merging**: Combines diarization + transcription into speaker-labeled text
5. **AI Analysis**: (Optional) Sends transcript to your chosen LLM for insights

## Supported Audio Formats

- `.m4a` (most common for meeting recordings)
- `.mp3`
- `.wav`
- `.mp4` (extracts audio)
- Any format supported by FFmpeg

## Example Output
```
[SPEAKER_00] Good morning everyone, thanks for joining today's product review.
[SPEAKER_01] Happy to be here. I've prepared some updates on the Q2 roadmap.
[SPEAKER_00] Great, let's start with that.
[SPEAKER_01] So we're planning to ship three major features...
```

**AI Summary:**
> This was a product planning meeting with 2 participants discussing Q2 roadmap priorities, feature timelines, and resource allocation.

**Action Items:**
- [ ] SPEAKER_01: Share Q2 roadmap doc by EOD
- [ ] SPEAKER_00: Schedule follow-up with engineering team
- [ ] SPEAKER_01: Prepare cost estimates for new features

## Privacy & Security

- Audio files are **never uploaded** - all processing happens locally in Docker
- Only the generated transcript is sent to LLM APIs (if you enable analysis)
- API keys are stored locally in `config/config.yaml` (gitignored)
- You can run transcription-only mode without any external API calls

## Troubleshooting

### "Format not recognized" error
- Ensure FFmpeg is properly installed in the Docker container
- Try converting your audio to `.wav` first using an external tool

### "HF_TOKEN not set" error
```bash
export HF_TOKEN="your_hugging_face_token"
```

### Docker build fails
```bash
# Clean Docker cache
docker system prune -a -f
docker build --no-cache -t meeting-assistant .
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- [pyannote.audio](https://github.com/pyannote/pyannote-audio) for speaker diarization
- [OpenAI Whisper](https://github.com/openai/whisper) for transcription
- Built with Docker for cross-platform compatibility

---

⭐ If you find this useful, please star the repo!
