#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from pyannote.audio import Pipeline
import whisper

def log(msg):
    print(f"[TRANSCRIBE] {msg}", flush=True)

if len(sys.argv) < 2:
    log("ERROR: No audio file provided")
    sys.exit(1)

input_file = Path(sys.argv[1])
if not input_file.exists():
    log(f"ERROR: File not found: {input_file}")
    sys.exit(1)

log(f"Processing: {input_file.name}")

# Convert to WAV
wav_file = input_file.with_suffix('.wav')
log("Converting to WAV...")
subprocess.run([
    'ffmpeg', '-y', '-i', str(input_file),
    '-ar', '16000', '-ac', '1', str(wav_file)
], check=True, capture_output=True)

# Load models
log("Loading diarization pipeline...")
hf_token = os.getenv('HF_TOKEN')
if not hf_token:
    log("ERROR: HF_TOKEN not set")
    sys.exit(1)

diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=hf_token  # Changed from use_auth_token
)

log("Loading Whisper model...")
whisper_model = whisper.load_model("base")

# Run diarization
log("Running speaker diarization...")
diarization = diarization_pipeline(str(wav_file))

# Run transcription
log("Running transcription...")
transcription = whisper_model.transcribe(str(wav_file))

# Merge results
log("Merging speaker labels with transcription...")
output_lines = []

for segment in transcription['segments']:
    seg_start = segment['start']
    seg_end = segment['end']
    text = segment['text'].strip()
    
    # Find overlapping speaker
    speaker = "UNKNOWN"
    for turn, _, spk in diarization.itertracks(yield_label=True):
        if turn.start <= seg_start < turn.end:
            speaker = spk
            break
    
    output_lines.append(f"[{speaker}] {text}")

# Save output
output_file = input_file.with_name(f"{input_file.stem}_transcript.txt")
with open(output_file, 'w') as f:
    f.write('\n'.join(output_lines))

log(f"COMPLETE! Output: {output_file}")
