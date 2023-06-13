import os
import openai

openai.api_key = os.getenv("OPENAI_API_TOKEN")
model = openai.Model.list()

print(model)
print("------------------------")
print("The most popular model is 'gpt-3.5-turbo'")
