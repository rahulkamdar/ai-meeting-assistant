#!/usr/bin/env python3
"""
AI Meeting Assistant - Transcript Analysis
Analyzes transcripts using LLM APIs (OpenAI, Anthropic, or OpenRouter)
"""

import os
import sys
import yaml
from pathlib import Path

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    
    if not config_path.exists():
        print("❌ config/config.yaml not found!")
        print("📝 Copy config.example.yaml to config.yaml and add your API keys")
        sys.exit(1)
    
    with open(config_path) as f:
        return yaml.safe_load(f)

def get_llm_client(config):
    """Initialize LLM client based on provider"""
    provider = config['llm_provider']
    api_key = config['api_keys'].get(provider)
    
    if not api_key or api_key == "sk-...":
        print(f"❌ API key for {provider} not configured in config.yaml")
        sys.exit(1)
    
    if provider == "openai":
        from openai import OpenAI
        return OpenAI(api_key=api_key), config['model']
    
    elif provider == "anthropic":
        from anthropic import Anthropic
        return Anthropic(api_key=api_key), config['model']
    
    elif provider == "openrouter":
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        return client, config['model']
    
    else:
        print(f"❌ Unsupported provider: {provider}")
        sys.exit(1)

def analyze_transcript(transcript_text, config):
    """Analyze transcript using configured LLM"""
    client, model = get_llm_client(config)
    provider = config['llm_provider']
    
    analysis_prompt = f"""Analyze this meeting transcript and provide:

1. **Summary**: A concise overview of the meeting (2-3 paragraphs)
2. **Action Items**: List all tasks, commitments, and follow-ups with assigned owners
3. **Key Decisions**: Important decisions made during the meeting
4. **Open Questions**: Unresolved questions or topics needing follow-up

Transcript:
{transcript_text}

Format your response in clear Markdown sections."""

    print(f"\n🤖 Analyzing with {provider} ({model})...\n")
    
    try:
        if provider in ["openai", "openrouter"]:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert meeting analyst. Provide clear, actionable insights."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        
        elif provider == "anthropic":
            response = client.messages.create(
                model=model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            return response.content[0].text
    
    except Exception as e:
        print(f"❌ Error calling {provider} API: {e}")
        sys.exit(1)

def interactive_qa(transcript_text, config):
    """Interactive Q&A about the transcript"""
    client, model = get_llm_client(config)
    provider = config['llm_provider']
    
    print("\n💬 Interactive Q&A Mode (type 'quit' to exit)")
    print("Ask questions about the transcript...\n")
    
    while True:
        question = input("❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if not question:
            continue
        
        prompt = f"""Based on this meeting transcript, answer the following question:

Question: {question}

Transcript:
{transcript_text}

Provide a clear, specific answer based only on information in the transcript."""

        try:
            if provider in ["openai", "openrouter"]:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                answer = response.choices[0].message.content
            
            elif provider == "anthropic":
                response = client.messages.create(
                    model=model,
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = response.content[0].text
            
            print(f"\n💡 {answer}\n")
        
        except Exception as e:
            print(f"❌ Error: {e}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_transcript.py <transcript_file>")
        sys.exit(1)
    
    transcript_path = Path(sys.argv[1])
    
    if not transcript_path.exists():
        print(f"❌ Transcript not found: {transcript_path}")
        sys.exit(1)
    
    # Load config
    config = load_config()
    
    # Read transcript
    with open(transcript_path) as f:
        transcript_text = f.read()
    
    print(f"📄 Loaded transcript: {transcript_path.name}")
    print(f"📏 Length: {len(transcript_text)} characters\n")
    
    # Generate analysis
    if config['analysis']['generate_summary']:
        analysis = analyze_transcript(transcript_text, config)
        
        # Save analysis
        output_path = transcript_path.with_name(f"{transcript_path.stem}_analysis.md")
        with open(output_path, 'w') as f:
            f.write(analysis)
        
        print(analysis)
        print(f"\n✅ Analysis saved to: {output_path}")
    
    # Interactive Q&A
    if config['analysis']['answer_questions']:
        interactive_qa(transcript_text, config)

if __name__ == "__main__":
    main()
