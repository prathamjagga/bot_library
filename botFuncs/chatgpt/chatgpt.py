
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

# chatgpt_response("")
