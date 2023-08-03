#!/bin/python

import chatgpt

chat = chatgpt.Chat()
chat = chatgpt.Chat(system_prompt="du bisch dumm")
print(chat.get_history())
# print(chat.say("hi"))
# print(chat.say("can you quote my last message?"))
