from transformers import GPT2Tokenizer
import pickle

print('Caching the tokenizer')
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

tokenizer_destination = 'output/gpt2_tokenizer.pkl'
with open(tokenizer_destination, 'wb') as f:
    pickle.dump(tokenizer, f)

print(f'Tokenizer cached to {tokenizer_destination}')
