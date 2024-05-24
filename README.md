# Telegram Bot: VoiceGPT

This is a Telegram bot that lets users chat with ChatGPT through Telegram. Both written and voice messages are supported. The bot will always transcribe voice messages to text first (and send it back as reference) and also respond through both text and voice. Hence, maximum flexibility of use-cases ia guaranteed.

## How To Use

### Requirements

#### Software

- Linux Distro
- `python3` with the following modules:
  - `aiogram`
  - `openai`
- `ffmpeg`
- Speech-to-text (STT)
  - `whisper.cpp` (with a model)
- Text to speech (TTS) (configurable)
  - gTTS (`gtts-cli`)
  - Coqui TTS (https://docs.coqui.ai/en/latest/docker_images.html)

#### APIs

- OpenAI API key (https://platform.openai.com/docs/quickstart)
- Telegram bot API key (https://core.telegram.org/bots/tutorial)

### Configuration

The following environment variables need to be set:
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`

### Run

For testing, simply run `main.py`

For productive use, install the `telegram-bot-voicegpt.service` systemd unit file.
