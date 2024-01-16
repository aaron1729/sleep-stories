
from openai import OpenAI
client = OpenAI()


import regex as re

import spacy
nlp = spacy.load("en_core_web_sm")

import strings
import models



import subprocess



print("hello")

# pattern_for_low_roman_numerals = r" (X{0,2}(?:I?X|IV|VI{0,3}|I{1,3}))[^A-Za-z]"
pattern_for_low_roman_numerals = r" (X{0,2}(?:I?X|IV|VI{0,3}|I{1,3}))\P{L}"

roman_numerals_appearing = re.findall(pattern_for_low_roman_numerals, "hell Vé.alo I! VI.øringsfossen")

print(roman_numerals_appearing)


# # print("goodbye")


# # pattern_for_roman_numerals = r"[IVXLCDM][^a-zA-Z]"

# # london_short = open("stories/story_london_2023-11-28_22-32-51_short.txt", "r").read()
# # berkeley_long = open("stories/story_berkeley_2023-11-28_22-32-51_long.txt", "r").read()

# # matches = re.finditer(pattern_for_roman_numerals, berkeley_long)

# # for match in matches:
# #     print(berkeley_long[match.start() - 15: match.end() + 15])

# # print("hello ∅ bye")

# ### the function below is half-baked. hopefully it won't be necessary.

# # years are tricky to say correctly in standard informal american parlance. so, here's a function that returns the correct spelling/pronunciation.
# def year_to_string(num):
#     if num == 0:
#         return "zero"
#     if num == 1:
#         return "one"
#     if num == 2:
#         return "two"
#     if num == 3:
#         return "three"
#     if num == 4:
#         return "four"
#     if num == 5:
#         return "five"
#     if num == 6:
#         return "six"
#     if num == 7:
#         return "seven"
#     if num == 8:
#         return "eight"
#     if num == 9:
#         return "nine"
#     if num == 10:
#         return "ten"
#     if num == 11:
#         return "eleven"
#     if num == 12:
#         return "twelve"
#     if num == 13:
#         return "thirteen"
#     if num == 14:
#         return "fourteen"
#     if num == 15:
#         return "fifteen"
#     if num == 16:
#         return "sixteen"
#     if num == 17:
#         return "seventeen"
#     if num == 18:
#         return "eighteen"
#     if num == 19:
#         return "nineteen"
#     if num == 20:
#         return "twenty"
#     if num == 30:
#         return "thirty"
#     if num == 40:
#         return "forty"
#     if num == 50:
#         return "fifty"
#     if num == 60:
#         return "sixty"
#     if num == 70:
#         return "seventy"
#     if num == 80:
#         return "eighty"
#     if num == 90:
#         return "ninety"


