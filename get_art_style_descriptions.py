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

        art_style_description_file = strings.open_safe("art-style-descriptions", f"art-style-description_{key}_{timestamp}.txt", "w")
        art_style_description_file.write(art_style_description)
        art_style_description_file.close()
    
    return None



### let's get some art style descriptions!
# get_art_style_description(...)
# get_art_style_description("rothko")
# get_art_style_description("rococo")
# get_art_style_description("gothic")
# get_art_style_description("retrofuturism")
# get_art_style_description("steampunk")
# get_art_style_description("acrylic-pour")
# get_art_style_description("autumn-skye")
# get_art_style_description("impressionism")

# get_art_style_description("navajo")
# get_art_style_description("chihuly")
# get_art_style_description("mayan")
# get_art_style_description("moroccan")
# get_art_style_description("ghanaian")
# get_art_style_description("ethiopian")
# get_art_style_description("baroque")
# get_art_style_description("chinese-silk")
# get_art_style_description("chinese-ink-wash")
# get_art_style_description("tanjore")
# get_art_style_description("graffiti")
# get_art_style_description("mithila")
# get_art_style_description("tapa")
# get_art_style_description("icelandic-illuminated")
# get_art_style_description("viking-engraving")
# get_art_style_description("minhwa")
# get_art_style_description("mughal")
# get_art_style_description("carribean-folk")
# get_art_style_description("quebecois")
# get_art_style_description("oil")
# get_art_style_description("american-romanticism")
# get_art_style_description("peruvian")
