# Detailed Usage Guide

## Installation

### Prerequisites
- Docker Desktop
- Hugging Face account
- (Optional) LLM API key

### Setup Steps

1. **Clone and enter directory**
```bash
   git clone https://github.com/rahulkamdar/ai-meeting-assistant.git
   cd ai-meeting-assistant
```

2. **Configure API keys**
```bash
   cp config/config.example.yaml config/config.yaml
   # Edit config.yaml with your preferred editor
```

3. **Build Docker image**
```bash
   docker build -t meeting-assistant .
```

## Basic Usage

### Transcription Only
```bash
export HF_TOKEN="your_hugging_face_token"
./transcribe.sh recordings/meeting.m4a
```

Output: `recordings/meeting_transcript.txt`

### With AI Analysis
```bash
# After transcription
python src/analyze_transcript.py recordings/meeting_transcript.txt
```

Output: `recordings/meeting_analysis.md`

## Advanced Usage

### Batch Processing
```bash
for file in recordings/*.m4a; do
    ./transcribe.sh "$file"
done
```

### Custom Whisper Model

Edit `src/process_audio.py`:
```python
whisper_model = whisper.load_model("medium")  # or "large"
```

### Different LLM Models

Edit `config/config.yaml`:
```yaml
model: "claude-3-opus-20240229"  # Use Claude Opus
# or
model: "gpt-4"  # Use GPT-4
```

## Tips & Best Practices

1. **Audio Quality**: Better audio = better transcription
   - Use high-quality recordings (48kHz recommended)
   - Minimize background noise
   
2. **Speaker Separation**: Works best with:
   - 2-6 speakers
   - Clear audio levels
   - Minimal cross-talk

3. **File Size**: For very long meetings (2+ hours):
   - Consider splitting into chunks
   - Use `medium` or `large` Whisper model for better accuracy

4. **Privacy**: 
   - Audio never leaves your machine
   - Only transcripts are sent to LLM APIs (if enabled)
   - Store API keys securely in `config/config.yaml`
