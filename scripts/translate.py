# NOTE: This script does not need to be run. The output files are already included in the repository.
#       We include this script to show how the translations were generated, and, especially, to preserve
#       the prompt and pipeline used to generate the translations.

import os
from glob import glob
from openai import OpenAI

# Requires OpenAI API key to be set in the environment variable OPENAI_API_KEY
client = OpenAI()

# Path to texts from https://github.com/jtauber/apostolic-fathers
PATH_TO_APOSTOLIC_FATHERS = "../../apostolic-fathers/texts"

system_prompt = {
  "role": "system",
  "content": "You are an expert in ancient languages. Your role is to provide a clear, natural, and accurate translation into excellent, readable, and idiomatic modern English for every line of ancient Greek/Latin that I give you. Aim for a 6th grade reading level. Do not write anything else."
}
messages = []

def get_translation(line):
  messages.append({
    "role": "user",
    "content": line
  })
  response = client.chat.completions.create(
    model="gpt-4o-2024-05-13",
    messages=[
      system_prompt,
      *messages[-6:]
    ]
  )
  content = response.choices[0].message.content
  messages.append({
    "role": "system",
    "content": content
  })
  return content

pwd = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(pwd, os.pardir))

for filename in glob(f"{PATH_TO_APOSTOLIC_FATHERS}/*.txt"):
    print(filename)
    output_filename = f"{parent_dir}/{filename.split('/')[-1].replace('.txt', '.en.txt')}"

    # if output file already exists, skip
    if glob(output_filename):
        continue

    with open(filename) as f:
        lines = f.readlines()

    translation_lines = []
    for line in lines:
        print(line.strip())
        line_id, text = line.split(" ", 1)
        translation = get_translation(text.strip())
        print(line_id, ">>", translation)
        translation_lines.append(f"{line_id} {translation.strip()}")

    with open(output_filename, "w") as f:
        f.write("\n".join(translation_lines))