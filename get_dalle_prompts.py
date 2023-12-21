###############
# as of 12/20/2023, this function is hard-coded to run through just certain items in the list
    # chunks_as_lists_of_cues
# to save time. be sure to change this manually, if desired.
###############

from openai import OpenAI
client = OpenAI()

import models
import strings
from inputs import *
from art_styles import *

timestamp = strings.time_now()

# if art_style_description_filename is omitted, we just get the most recent art-style-description file associated to that art_style.
def get_dalle_prompts(cues_filename, art_style, art_style_description_filename = None):

    destination = cues_filename.split("_")[1]
    destination_fullname = inputs[destination]["destination_fullname"]

    if not art_style_description_filename:
        art_style_description_filename = strings.get_latest_filename(art_style, "art-style-descriptions")
    
    print(f"getting dalle prompts for {cues_filename} in the art style {art_style}, as described in {art_style_description_filename}")
    
    art_style_key = art_style_description_filename.split("_")[1]
    art_style_fullname = art_styles[art_style_key]

    art_style_description = open(f"art-style-descriptions/{art_style_description_filename}", "r").read()


    system_prompt_for_dalle_prompts = strings.system_prompt_for_dalle_prompts(destination_fullname, art_style_fullname, art_style_description)
    system_message_for_dalle_prompts = {"role": "system", "content": system_prompt_for_dalle_prompts}
    print(f"\nsystem_prompt_for_dalle_prompts is:\n\n{system_prompt_for_dalle_prompts}\n")
    message_list = [system_message_for_dalle_prompts]

    cues_string = open(f"cues/{cues_filename}", "r").read()
    chunks_as_cues_strings = cues_string.split(strings.separator)
    chunks_as_lists_of_cues = [chunk_as_cues_string.split("\n") for chunk_as_cues_string in chunks_as_cues_strings]

    dalle_prompts = []
    for (index, chunk_as_list_of_cues) in enumerate(chunks_as_lists_of_cues[1: 4]):
        chunk = chunks_as_cues_strings[index]
        for cue in chunk_as_list_of_cues:
            print(f"\nat {strings.time_now()}, getting dalle prompt for the cue:\n\n{cue}")
            user_prompt_for_dalle_prompt = f"SNIPPET:\n\n{cue}\n\nCONTEXT:\n\n{chunk}"
            user_message_for_dalle_prompt = {"role": "system", "content": user_prompt_for_dalle_prompt}
            message_list.append(user_message_for_dalle_prompt)
            completion = client.chat.completions.create(
                model = models.gpt_model,
                messages = message_list
            )
            assistant_prompt_with_dalle_prompt = completion.choices[0].message.content
            assistant_message_with_dalle_prompt = {"role": "assistant", "content": assistant_prompt_with_dalle_prompt}
            message_list.append(assistant_message_with_dalle_prompt)
            dalle_prompts.append(assistant_prompt_with_dalle_prompt)
            print(f"\nand the dalle prompt is:\n\n{assistant_prompt_with_dalle_prompt}\n")
    
    dalle_prompts_string = strings.separator.join(dalle_prompts)
    dalle_prompts_filename = f"dalle-prompts_for_{cues_filename[:-4]}_in_{art_style}_at_{timestamp}.txt"
    dalle_prompts_file = strings.open_safe("dalle-prompts", dalle_prompts_filename, "w")
    dalle_prompts_file.write(dalle_prompts_string)
    dalle_prompts_file.close()

    return None



### let's get some dalle prompts!
# get_dalle_prompts(...)
# get_dalle_prompts("cues_dubai_2023-11-28_22-32-51_short.txt", "rothko")
# get_dalle_prompts("cues_cinqueterre_2023-12-05_17-42-24_long.txt", "rococo")
# get_dalle_prompts("cues_cinqueterre_2023-12-05_17-42-24_long.txt", "gothic")
# get_dalle_prompts("cues_cinqueterre_2023-12-05_17-42-24_long.txt", "retrofuturism")
# get_dalle_prompts("cues_cinqueterre_2023-12-05_17-42-24_long.txt", "steampunk")
# get_dalle_prompts("cues_cinqueterre_2023-12-05_17-42-24_long.txt", "acrylic-pour")
# get_dalle_prompts("cues_cinqueterre_2023-12-05_17-42-24_long.txt", "autumn-skye")
# get_dalle_prompts("cues_cinqueterre_2023-12-05_17-42-24_long.txt", "impressionism")

for input in inputs:
    # for just a first pass at images (12/20/2023), do the short stories since this should give more variability in images to choose from.
    cues_filename = strings.get_latest_filename(input, "cues", "short")
    art_style = inputs[input]["art_style"]
    print(f"getting dalle prompts...\ncues file: {cues_filename}\nart_style: {art_style}")
    get_dalle_prompts(cues_filename, art_style)