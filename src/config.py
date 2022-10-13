import logging
import platform
from pathlib import Path
import os
import openai

# Determine environment
on_laptop = platform.system() == "Darwin"

# Set up output dir
if on_laptop:
    output_dir = (Path.cwd() / '..' / 'output').resolve()
else:
    output_dir = Path("/var/data/output")

if not output_dir.exists():
    logger.warn(f"Output directory {output_dir} does not exist. Creating it.")
    output_dir.mkdir()

# GPT3 settings
gpt3_token_limit = 3200
default_openai_model = "text-davinci-002"
openai.api_key = os.getenv("OPENAI_API_KEY")
available_openai_models = [model['id'] for model in openai.Model.list()['data']]

# Debugging checks
if __name__ == '__main__':
    print('on_laptop:', on_laptop)
    print('output_dir:', output_dir)
    print('gpt3_token_limit:', gpt3_token_limit)
    print(available_openai_models)


