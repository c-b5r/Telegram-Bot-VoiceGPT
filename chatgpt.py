#!/bin/python

import openai
import os
from typing import List, Optional, Union

openai.api_key = os.environ.get("OPENAI_API_KEY")

class Chat:
  def __init__(
      self,
      openai_api_key:    str                        = None,
      model:             str                        = "gpt-3.5-turbo",
      # system_prompt:     str                        = "You are a helpful assistant.",
      system_prompt:     str                        = None,
      temperature:       float                      = 0.5,
      max_tokens:        int                        = 256,
      messages:          list                       = [],
      n:                 int                        = 1,
      stop:              Optional[Union[str, list]] = None,
      presence_penalty:  float                      = 0,
      frequency_penalty: float                      = 0.1,
      ):
        self.openai_api_key    = openai_api_key
        self.model             = model
        self.temperature       = temperature
        self.max_tokens        = max_tokens
        self.n                 = n
        self.stop              = stop
        self.presence_penalty  = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.messages = messages or []

        if system_prompt != None:
          self.system_prompt = system_prompt
          self.messages = [{"role": "system", "content": system_prompt}]


  def say(self, prompt):
    self.messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
      model             = self.model,
      messages          = self.messages,
      temperature       = self.temperature,
      max_tokens        = self.max_tokens,
      n                 = self.n,
      stop              = self.stop,
      presence_penalty  = self.presence_penalty,
      frequency_penalty = self.frequency_penalty,
      )

    generated_texts = [
      choice.message["content"].strip() for choice in response["choices"]
      ]

    self.messages.append({"role": "assistant", "content": generated_texts[0]})

    return generated_texts[0]


  def reset_history(self):
    if self.messages == []:
      return

    history = ""
    for message in self.messages:
      history += f"{message['role']}: {message['content']}\n"

    return history[:-1]


  def get_history(self):
    if self.messages == []:
      return

    history = ""
    for message in self.messages:
      history += f"{message['role']}: {message['content']}\n"

    return history[:-1]