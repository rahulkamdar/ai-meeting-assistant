#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 <audio-file> [language-code]"
    echo ""
    echo "Arguments:"
    echo "  audio-file      Path to audio file"
    echo "  language-code   (Optional) Source language code (e.g., 'gu', 'es', 'hi')"
    echo "                  If not specified, uses config.yaml or auto-detects"
    echo ""
    echo "Examples:"
    echo "  $0 audio.m4a           # Auto-detect or use config"
    echo "  $0 audio.m4a gu        # Gujarati to English"
    echo "  $0 audio.m4a es        # Spanish to English"
    echo "  $0 audio.m4a hi        # Hindi to English"
    exit 1
}

if [ -z "$1" ]; then
    usage
fi

if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: HF_TOKEN not set. Run: export HF_TOKEN=your-token"
    exit 1
fi

AUDIO_FILE="$1"
LANGUAGE="${2:-}"  # Optional second argument

echo "Building Docker image..."
docker build -t transcriber .

echo "Running transcription..."
if [ -n "$LANGUAGE" ]; then
    echo "Language: $LANGUAGE → English"
    docker run --rm \
        -e HF_TOKEN="$HF_TOKEN" \
        -e LANGUAGE="$LANGUAGE" \
        -v "$(pwd)":/app \
        transcriber \
        python src/process_audio.py "/app/$AUDIO_FILE"
else
    echo "Language: auto-detect or from config"
    docker run --rm \
        -e HF_TOKEN="$HF_TOKEN" \
        -v "$(pwd)":/app \
        transcriber \
        python src/process_audio.py "/app/$AUDIO_FILE"
fi
