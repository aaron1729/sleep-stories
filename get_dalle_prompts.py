from openai import OpenAI
client = OpenAI()

import models
import strings
from inputs import *

timestamp = strings.time_now()

# inputs:
    # a cues filename;
    # an art-styles filename that contains an art style for that destination.
# if the latter is omitted, we automatically get the most recent one that contains an art style for that destination.

def get_dalle_prompts(cues_filename, art_styles_filename_arg = None):

    destination = cues_filename.split("_")[1]
    destination_fullname = inputs[destination]

    if not art_styles_filename_arg:
        art_styles_filenames = strings.get_all_unhidden_files("art-styles")
        art_styles_filenames.sort()
    else:
        art_styles_filenames = [art_styles_filename_arg]

    art_styles_for_destination = []
    for art_styles_filename in art_styles_filenames:
        art_style_strings = open(f"art-styles/{art_styles_filename}", "r").read().split(strings.separator)
        for art_style_string in art_style_strings:
            if destination == art_style_string.split("\n")[0].split(" ")[-1]:
                print(f"found an art style for destination {destination} in {art_styles_filename}")
                # remove the first four lines, e.g.: "location: tokyo\nLOCATION: Tokyo, Japan\n\n"
                art_style_explanation_and_description_string = "\n".join(art_style_string.split("\n")[4:])
                art_styles_for_destination.append(art_style_explanation_and_description_string)
    
    if len(art_styles_for_destination) == 0:
        if art_styles_filename_arg:
            raise Exception(f"no art style for the destination {destination} was found in {art_styles_filename_arg}")
        else:
            raise Exception(f"no art styles were found (in _any_ of the art-styles files) for the destination {destination}")
    
    art_style = art_styles_for_destination[-1]

    system_prompt_for_dalle_prompts = strings.system_prompt_for_dalle_prompts(destination_fullname, art_style)
    system_message_for_dalle_prompts = {"role": "system", "content": system_prompt_for_dalle_prompts}
    print(f"\nsystem_prompt_for_dalle_prompts is:\n\n{system_prompt_for_dalle_prompts}\n")
    message_list = [system_message_for_dalle_prompts]

    cues_string = open(f"cues/{cues_filename}", "r").read()
    chunks_as_cues_strings = cues_string.split(strings.separator)
    chunks_as_lists_of_cues = [chunk_as_cues_string.split("\n") for chunk_as_cues_string in chunks_as_cues_strings]

    dalle_prompts = []
    for (index, chunk_as_list_of_cues) in enumerate(chunks_as_lists_of_cues[: 2]):
        chunk = chunks_as_cues_strings[index]
        for cue in chunk_as_list_of_cues:
            print(f"\ngetting dalle prompt for the cue:\n\n{cue}")
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
    dalle_prompts_filename = f"dalle-prompts_for_{cues_filename[:-4]}_at_{timestamp}.txt"
    dalle_prompts_file = open(f"dalle-prompts/{dalle_prompts_filename}", "w")
    dalle_prompts_file.write(dalle_prompts_string)
    dalle_prompts_file.close()

    return None



### let's get some dalle prompts!
# get_dalle_prompts("cues_tokyo_2023-11-28_22-32-51_long.txt")
get_dalle_prompts("cues_kyoto_2023-11-28_22-32-51_long.txt")