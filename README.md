# Audiora

> Listen to anything, anytime, leveraging AI.

Audiora is an AI-enhanced audio platform that transforms user preferences into personalized engaging audio experiences.

## Features

- 🎯 Personalized Learning: AI-driven audiocasts tailored to your preferences
- 🔊 Seamless TTS: Natural-sounding audio conversion
- 📚 Diverse Content: Wide range of topics from professional skills to self-improvement
- 📱 Mobile-First: Optimized for on-the-go learning
- ⚡ Continuous Playback: Seamless cross-device listening

## Quick Start

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Get your LLM Api keys - Openai | Anthropic | Gemini
- Get your TTS Api key Openai | Elevenlabs

### Installation

1. Clone the repository:

```bash
git clone https://github.com/nwaughachukwuma/audiora.git
cd audiora
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables in .env:

```bash
OPENAI_API_KEY="your-openai-api-key"
ANTHROPIC_API_KEY="your-anthropic-api-key"
GEMINI_API_KEY="your-gemini-api-key"
ELEVENLABS_API_KEY="your-elevenlabs-api-key"
APP_URL="http://localhost:8080"
```

4. Launch the application:

```bash
streamlit run app.py
```

## Usage

- Enter a prompt or choose from examples for your audiocast
- Tell the AI your preferences over a chat sessionn
- Click "Generate Audiocast"
- Listen and enjoy your personalized audio content

## Tech Stack

- Python and Streamlit
- AI: Custom models for TTS and content generation
- Pydub for audio enhancements

## Contributing

- Fork the repository
- Create a feature branch (git checkout -b feature/amazing-feature)
- Commit changes (git commit -m 'Add amazing feature')
- Push to branch (git push origin feature/amazing-feature)
- Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Sponsors

- VeedoAI: https://veedo.ai

## Contact

- Email: chuks@veedo.ai
- Twitter: @ChukwumaNWaugha
