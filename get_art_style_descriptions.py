from openai import OpenAI
client = OpenAI()

import models
import strings

from art_styles import *

timestamp = strings.time_now()

# input: a key in the art_styles dictionary. if this is left empty, we do all of them.
def get_art_style_description(key = None):

    if not key:
        keys = art_styles.keys()
    else:
        keys = [key]
    
    for key in keys:

        art_style = art_styles[key]

        print(f"getting a description of {art_style} with timestamp {timestamp} at {strings.time_now()}")

        user_prompt_for_art_style_description = strings.user_prompt_for_art_style_description(art_style)
        user_message_for_art_style_description = {"role": "user", "content": user_prompt_for_art_style_description}
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = [user_message_for_art_style_description]
        )
        art_style_description = completion.choices[0].message.content

        art_style_description_file = open(f"art-style-descriptions/art-style-description_{key}_{timestamp}.txt", "w")
        art_style_description_file.write(art_style_description)
        art_style_description_file.close()
    
    return None



### let's get some art style descriptions!
# get_art_style_description()
# get_art_style_description("cave")