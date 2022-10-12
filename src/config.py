import logging
import platform
from pathlib import Path
import os


# Determine environment
on_laptop = platform.system() == "Darwin"


# Set up output dir
if on_laptop:
    output_dir = (Path.cwd() / '..' / 'output').resolve()
else:
    output_dir = Path("/root/output")

if not output_dir.exists():
    logger.warn(f"Output directory {output_dir} does not exist. Creating it.")
    output_dir.mkdir()

# GPT3 settings
gpt3_token_limit = 3200


# Debugging checks
if __name__ == '__main__':
    print('on_laptop:', on_laptop)
    print('output_dir:', output_dir)
    print('gpt3_token_limit:', gpt3_token_limit)

