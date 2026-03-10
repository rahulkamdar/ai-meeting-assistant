#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <audio-file>"
    exit 1
fi

if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: HF_TOKEN not set. Run: export HF_TOKEN=your-token"
    exit 1
fi

AUDIO_FILE="$1"

echo "Building Docker image..."
docker build -t transcriber .

echo "Running transcription..."
docker run --rm \
    -e HF_TOKEN="$HF_TOKEN" \
    -v "$(pwd)":/app \
    transcriber \
    python process_audio.py "/app/$AUDIO_FILE"
