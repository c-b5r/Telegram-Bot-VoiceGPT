#!/bin/python3

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os, subprocess
import chatgpt

# Read the token from a file
with open("/home/cb/.key/me/t/cb5r_VoiceGPT_Bot", "r") as file:
  token = file.read().strip()

# Create a bot instance
bot = Bot(token=token)

# Create a dispatcher instance
dp = Dispatcher(bot)

# Temp file settings
tmpdir = "/tmp/.telegram-bot"

# Language
languages = ["en", "de"]
language = languages[0]

# Chats database
chats = {}


def convertOgg2Wav(inputFile: str, outputFile: str):
  subprocess.call(f"ffmpeg -i '{inputFile}' -ac 1 -ar 16k '{outputFile}'", shell=True)

def voiceRecognition(audioFile: str):
  # Transcribe speech to text using whisper
  global language
  subprocess.call(f"whisper.cpp-base --language {language} --output-txt '{audioFile}'", shell=True)
  textFile = os.path.join(tmpdir, f"{audioFile}.txt")

  # Get transcript from text file
  with open(textFile, "r") as file:
    return file.read().strip()

def getGptResponse(id: int, prompt: str):
  if id in chats:
    return chats[id].say(prompt)
  else:
    return chatgpt.Chat().say(prompt)

def gtts(inputFile: str, outputFile: str):
  global language
  subprocess.call(f"gtts-cli --lang {language} --file '{inputFile}' | ffmpeg -i pipe:0 -f opus -ac 1 -ar 48k -b:a 32k {outputFile}", shell=True)

def escapeSpecialChars(text: str):
  for char in ['*', '_', '`', '[', ']', '!', '.']:
    text = text.replace(f"{char}", f"\{char}")
  return text

def cleanTempFiles(file_id: str):
  subprocess.call(f"rm {tmpdir}/{file_id}*", shell=True)


# Define a handler function
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
  words = message.text.split()
  cmd = words[0]

  # COMMAND: Change language
  global language
  if cmd in ["/language", "/lang"]:
    if len(words) == 1:
      await message.answer(f"Language = {language}")
    else:
      if words[1] in languages:
        language = words[1]
        await message.answer(f"Changed language to: {language}")
      else:
        await message.answer(f"ERROR: Choose an available language: {languages}")

  # COMMAND: Enter conversation
  elif cmd in ["/conversation", "/convo", "/conv"]:
    chats[message.from_user.id] = chatgpt.Chat()
    await message.answer(f"Starting a new conversation")

  # COMMAND: Exit conversation
  elif cmd == "/exit":
    del chats[message.from_user.id]
    await message.answer(f"Exiting the conversation")

  # DEFAULT: Answer messages
  else:
    # Get ChatGPT response
    response_text = getGptResponse(message.from_user.id, message.text)

    # Respond with ChatGPT response
    await message.answer(response_text)

    # Create voice message from ChatGPT response
    output_message_voice_file_ogg = tts(file_id=message.message_id, text=response_text)

    # Respond with TTS voice message of ChatGPT response
    await message.answer_voice(voice=open(output_message_voice_file_ogg, "rb"))

    # Clear temp files
    cleanTempFiles(file_id=message.message_id)


# Define a handler function for voice messages
@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_voice_message(message: types.Message):
  # Get the voice message object
  file_id = message.voice.file_id

  # Save the voice message to temp directory
  prompt_voice_file_ogg = os.path.join(tmpdir, f"{file_id}.ogg")
  prompt_voice_file_wav = os.path.join(tmpdir, f"{file_id}.wav")

  # Download OGG voice message to tempdirectory
  await message.voice.download(prompt_voice_file_ogg)

  # Convert the audio to 16khz mono using ffmpeg
  convertOgg2Wav(inputFile=prompt_voice_file_ogg, outputFile=prompt_voice_file_wav)

  # Transcribe speech to text using whisper
  prompt_text = voiceRecognition(prompt_voice_file_wav)

  # Escape aiogram special characters
  prompt_text = escapeSpecialChars(prompt_text)

  # Respond with prompt transcript
  await message.reply(f"*TRANSCRIPT*\n\n{prompt_text}", parse_mode=types.ParseMode.MARKDOWN_V2)

  # Get ChatGPT response
  response_text = getGptResponse(message.from_user.id, prompt_text)

  # Respond with ChatGPT response
  await message.answer(response_text)

  # Create voice message from ChatGPT response
  output_message_voice_file_ogg = tts(file_id=file_id, text=response_text)

  # Respond with TTS voice message of ChatGPT response
  await message.answer_voice(voice=open(output_message_voice_file_ogg, "rb"))

  # Clear temp files
  cleanTempFiles(file_id=file_id)


# Util function: gTTS
def tts(file_id, text):
  # Write ChatGPT response to text file
  response_text_file = os.path.join(tmpdir, f"{file_id}-response.txt")
  with open(response_text_file, "w") as file:
    file.write(text)

  # Run text-to-speech on response using gTTS
  output_message_voice_file_ogg = os.path.join(tmpdir, f"{file_id}-response.ogg")

  # Run gTTS
  gtts(inputFile=response_text_file, outputFile=output_message_voice_file_ogg)

  return output_message_voice_file_ogg


# Start the bot
if __name__ == '__main__':
  try:
    os.makedirs(tmpdir)
    print(f"Directory '{tmpdir}' created successfully.")
  except Exception as e:
    print(f"Error creating directory '{tmpdir}': {e}")

  executor.start_polling(dp, skip_updates=True)
