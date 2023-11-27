
from openai import OpenAI
client = OpenAI()

import models

import spacy
nlp = spacy.load("en_core_web_sm")


# from strings import * # this imports that code directly to the namespace.
import strings # this imports foo from there as strings.foo instead.



# print(my_cool_string)

# my_var = 5

# print(my_func(my_var))



# print(user_prompt_for_stops("dest", 30, "boat", None))


# print(system_prompt_for_story("shorty", 5))



# def my_func(str):
#     return str + str

# # print(my_func("hello"))

# def my_func1(str):
#     return my_func2(str) + str

# def my_func2(str):
#     return "hello" + str + "hi"

# print(my_func1("abc"))


# text = "Hello world! I remember that Mr. Smith Sr. went to Mt. Wilson to watch the St. Teresa eclipse. This is a test text.! It contains several sentences. ... Or does it???"
# doc = nlp(text)
# sentences = [sentence.text for sentence in doc.sents]
# for sentence in sentences:
#     print(f"{sentence}")





my_list = ["abc", "def", "123", "XYZ"]

my_string = f"""the list, joined, is: {'''
'''.join(my_list)}"""

print(my_string)

newline = "\n"

my_string_again = f"the list, joint, is: {strings.nn.join(my_list)}"

print("my_string_again is:", my_string_again)

my_tuple = (5, 7, 9, 3)

(a, b, c, d) = my_tuple

print("c is:", c)

e, f = None, None

print("f is:", f)

def hello(a, b):
    hello = "str"
    return hello + a + b

print(hello("hi", "there"))

my_IPA_string = "/ˈpɑː.sɑr ˈsɛ.ni ˈuː.bʊd/"

completion = client.chat.completions.create(
        model = models.gpt_model,
        messages = [{"role": "user", "content": "Please tell me how to pronounce 'Pasar Seni Ubud' using the International Phonetic Alphabet (IPA). Please do not respond with anything besides the IPA."}]
    )
print("the pronunciation is:", completion.choices[0].message.content)