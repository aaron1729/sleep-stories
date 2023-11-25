import spacy
nlp = spacy.load("en_core_web_sm")


from strings import *

# print(my_cool_string)

# my_var = 5

# print(my_func(my_var))



# print(user_prompt_for_stops("dest", 30, "boat", None))


# print(system_prompt_for_story("shorty", 5))



def my_func(str):
    return str + str

# print(my_func("hello"))


def my_func1(str):
    return my_func2(str) + str

def my_func2(str):
    return "hello" + str + "hi"

print(my_func1("abc"))


text = "Hello world! I remember that Mr. Smith Sr. went to Mt. Wilson to watch the St. Teresa eclipse. This is a test text.! It contains several sentences. ... Or does it???"
doc = nlp(text)
sentences = [sentence.text for sentence in doc.sents]
for sentence in sentences:
    print(f"{sentence}")