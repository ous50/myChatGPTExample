import openai

# API key
openai.api_key = 'sk-'


model_selection = input("What Model would you like to \n") or "gpt-3.5-turbo"


question = input("Input your question.\nThis scricpt only supports one question + one answers.\n")

completetion = openai.ChatCompletion.create(
    model=model_selection,
    messages=[
        {
            "role": "user",
            "content": question
         }
    ]
)

print(completetion.choices[0].message.content)
