import os
import openai

openai.api_type = "azure"
openai.api_base = "https://openai-sandbox-jep.openai.azure.com/"
openai.api_version = "2022-12-01"

# Get the API key from the environment variable
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

response = openai.Completion.create(
    engine="davinci3",
    prompt="escribime un haiku sobre openai",
    temperature=2,
    max_tokens=1000,
    top_p=0.5,
    frequency_penalty=0,
    presence_penalty=0,
    best_of=1,
    stop=None
)


response = response['choices'][0]['text']

print(response)
