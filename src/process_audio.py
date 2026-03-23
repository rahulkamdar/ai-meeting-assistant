#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from pyannote.audio import Pipeline
import whisper
import yaml

def log(msg):
    print(f"[TRANSCRIBE] {msg}", flush=True)

def load_config():
    """Load configuration if it exists"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return None

if len(sys.argv) < 2:
    log("ERROR: No audio file provided")
    sys.exit(1)

input_file = Path(sys.argv[1])
if not input_file.exists():
    log(f"ERROR: File not found: {input_file}")
    sys.exit(1)

log(f"Processing: {input_file.name}")

# Load config
config = load_config()
whisper_model_size = "base"
translate_to_english = False

# Check for command-line language argument (via environment variable)
language = os.getenv('LANGUAGE')

if language:
    # Language specified via command line - always translate to English
    translate_to_english = True
    log(f"Command-line language: {language} → English translation enabled")
    # Use medium model for better translation quality
    whisper_model_size = "medium"
elif config and 'transcription' in config:
    # Fall back to config file
    language = config['transcription'].get('language')
    whisper_model_size = config['transcription'].get('whisper_model', 'base')
    translate_to_english = config['transcription'].get('translate_to_english', False)
    
    if translate_to_english and language and language != 'en':
        log(f"Config: {language} → English translation")
    elif language:
        log(f"Config: Transcribe in {language}")
    else:
        log("Config: Auto-detect language")
else:
    log("No config found - auto-detecting language")

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
    use_auth_token=hf_token
)

log(f"Loading Whisper model ({whisper_model_size})...")
whisper_model = whisper.load_model(whisper_model_size)

# Run diarization
log("Running speaker diarization...")
diarization = diarization_pipeline(str(wav_file))

# Run transcription or translation
if translate_to_english and language and language != 'en':
    log(f"Translating {language} audio to English...")
    transcription = whisper_model.transcribe(str(wav_file), language=language, task='translate')
else:
    log("Running transcription...")
    transcription_options = {}
    if language:
        transcription_options['language'] = language
    transcription = whisper_model.transcribe(str(wav_file), **transcription_options)

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
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

log(f"COMPLETE! Output: {output_file}")

# Log detected language if auto-detect was used
if not language and 'language' in transcription:
    log(f"Detected language: {transcription['language']}")
