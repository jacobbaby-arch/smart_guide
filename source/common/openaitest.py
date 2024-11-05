import openai

# Set your OpenAI API key
openai.api_key = ''



# Send a prompt to the GPT model
response = openai.Completion.create(
  
  engine="text-davinci-003",  # You can replace with any GPT model version you want
  prompt="Hello, can you explain how ChatGPT API works?",  # The input prompt
  max_tokens=100,  # Controls the length of the output
  temperature=0.7  # Controls randomness: 0.0 for deterministic, 1.0 for randomness
)

# Print the model's response
print(response.choices[0].text.strip())
