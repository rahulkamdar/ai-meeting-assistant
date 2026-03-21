FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set environment variables to fix OpenBLAS threading warnings
ENV OPENBLAS_NUM_THREADS=1
ENV OMP_NUM_THREADS=1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir openai-whisper
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory
COPY src/ ./src/

# Copy config directory structure (example file only)
COPY config/config.example.yaml ./config/config.example.yaml
