
from openai import OpenAI
client = OpenAI()


import re

import spacy
nlp = spacy.load("en_core_web_sm")

import strings
import models



pattern_for_roman_numerals = r"[IVXLCDM][^a-zA-Z]"

london_short = open("stories/story_london_2023-11-28_22-32-51_short.txt", "r").read()
berkeley_long = open("stories/story_berkeley_2023-11-28_22-32-51_long.txt", "r").read()

matches = re.finditer(pattern_for_roman_numerals, berkeley_long)

for match in matches:
    print(berkeley_long[match.start() - 15: match.end() + 15])