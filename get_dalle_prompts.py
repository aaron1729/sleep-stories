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
    for (index, chunk_as_list_of_cues) in enumerate(chunks_as_lists_of_cues[: 2]):
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
    dalle_prompts_file = open(f"dalle-prompts/{dalle_prompts_filename}", "w")
    dalle_prompts_file.write(dalle_prompts_string)
    dalle_prompts_file.close()

    return None



### let's get some dalle prompts!

# get_dalle_prompts("cues_algarve_2023-11-28_22-12-12_short.txt", "fauvism")
# get_dalle_prompts("cues_napa_2023-11-28_22-32-51_long.txt", "cubism")
# get_dalle_prompts("cues_rio_2023-11-28_22-32-51_long.txt", "victorian")
# get_dalle_prompts("cues_chiangmai_2023-11-28_22-32-51_long.txt", "sepia-pencil")
# get_dalle_prompts("cues_bali_2023-11-28_22-32-51_short.txt", "manga")
# get_dalle_prompts("cues_costarica_2023-11-28_22-32-51_short.txt", "pop")
# get_dalle_prompts("cues_newyorkcity_2023-11-28_22-32-51_long.txt", "psychedelic")
# get_dalle_prompts("cues_queenstown_2023-11-28_22-32-51_short.txt","thai-temple")
# get_dalle_prompts("cues_paris_2023-11-28_22-32-51_short.txt", "islamic-geometric")
# get_dalle_prompts("cues_istanbul_2023-11-28_22-32-51_long.txt", "turkish-marbling")
# get_dalle_prompts("cues_greece_2023-11-28_22-32-51_short.txt", "pointillism")
# get_dalle_prompts("cues_london_2023-11-28_22-32-51_short.txt", "abstract")
# get_dalle_prompts("cues_shanghai_2023-11-28_22-32-51_short.txt", "surrealism")
# get_dalle_prompts("cues_barcelona_2023-11-28_22-32-51_short.txt", "neoexpressionism")
# get_dalle_prompts("cues_algarve_2023-11-28_22-12-12_long.txt", "cave")


# at 6:30pm:
# get_dalle_prompts("cues_amalfi_2023-11-28_22-32-51_short.txt", "magical-realism")



# 11/30/2023 at 5pm:
# get_dalle_prompts("cues_costarica_2023-11-28_22-32-51_long.txt", "chinese-cubism")
# at 10pm:
# get_dalle_prompts("cues_chiangmai_2023-11-28_22-32-51_short.txt", "mishe")

# get_dalle_prompts("cues_chiangmai_2023-11-28_22-32-51_short.txt", "pollock")
# get_dalle_prompts("cues_berkeley_2023-11-28_22-32-51_short.txt", "basquiat")

# for art_style in [
#     "midcentury-modern",
#     "art-nouveau",
#     "japanese-woodblock",
#     "japanese-ink-wash",
#     "batik",
#     "lanna",
#     "neobaroque"]:
    # get_dalle_prompts("cues_berkeley_2023-11-28_22-32-51_short.txt", art_style)

# get_dalle_prompts("cues_kyoto_2023-11-28_22-32-51_long.txt", "hopper")
# get_dalle_prompts("cues_kyoto_2023-11-28_22-32-51_long.txt", "italian-futurism")
# get_dalle_prompts("cues_newyorkcity_2023-11-28_22-32-51_short.txt", "new-yorker")
# get_dalle_prompts("cues_kyoto_2023-11-28_22-32-51_long.txt", "miro")
# get_dalle_prompts("cues_kyoto_2023-11-28_22-32-51_long.txt", "tomine")
get_dalle_prompts("cues_kyoto_2023-11-28_22-32-51_long.txt", "hopper")