import random
from botbuilder.core import TurnContext

import openai

openai.api_key = "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"


def chatgpt_response(text: str) -> str:
    """
    takes some text and returns chatgpt's response for it
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": text},
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return result

    pass


def recognize_simple_message(msg: str) -> tuple:

    msg = msg.lower()

    # checking if it is a greeting message
    greetings = ['hi', 'hello', 'hey', 'heya', 'bonjour',
                 'welcome', 'how are you', 'what\'s happening', 'what\'s up']
    for val in greetings:
        resp_list = ['Hi, how can I help you today', 'Howdy, how are you?', 'Hey :)',
                     'Hello there, I hope you are doing good, how can I assist you today.']
        if msg.__contains__(val):
            return "greeting", random.choice(resp_list)

    # checking if it is a leaving message
    leaving_messages = ['bye', 'see you', 'by', 'take care']
    for val in leaving_messages:
        resp_list = ['Good Bye!', 'See you soon!', 'Bye, have a good Day.']
        if msg.__contains__(val):
            return "leaving", random.choice(resp_list)

    return "other", None

    pass


def ask_anything_flow(text):
    return chatgpt_response(text)
    pass
