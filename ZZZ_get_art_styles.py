from openai import OpenAI
client = OpenAI()

import models
import strings

from inputs import *

timestamp = strings.time_now()



# input: a list of `destination` strings, e.g. ["berkeley", "amalfi", "bali"].
# if it's left empty, we get _all_ destinations stored in inputs.
def get_art_styles_OLD(destinations):

    if not destinations:
        destinations = [input["destination"] for input in inputs]
    
    destination_fullnames = [inputs[destination]["destination_fullname"] for destination in destinations]

    print(f"\nat {strings.time_now()}, getting art styles with descriptions for the destinations:\n{strings.n.join(destination_fullnames)}\n")

    ##### GET LIST OF ART STYLES

    system_message_for_art_styles = {"role": "system", "content": strings.system_prompt_for_art_styles}
    message_list = [system_message_for_art_styles]

    destinations_and_art_styles = []
    for destination_fullname in destination_fullnames:
        user_message_for_art_style = {"role": "user", "content": destination_fullname}
        message_list.append(user_message_for_art_style)
        print(f"\ngetting an art style for {destination_fullname}\n")
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = message_list
        )
        assistant_prompt_with_art_style = completion.choices[0].message.content
        assistant_message_with_art_style = {"role": "assistant", "content": assistant_prompt_with_art_style}
        message_list.append(assistant_message_with_art_style)
        destinations_and_art_styles.append(f"LOCATION: {destination_fullname}\n\n" + assistant_prompt_with_art_style)
        print(f"\nthe destination_fullname is {destination_fullname}, and the art_style is:\n\n{assistant_prompt_with_art_style}")

    system_message_for_extended_art_style_description = {"role": "system", "content": strings.system_prompt_for_art_style_description}
    
    extended_art_styles_descriptions = []
    for destination_and_art_style in destinations_and_art_styles:
        user_message_for_art_style = {"role": "user", "content": destination_and_art_style}
        print(f"\ngetting an extended description of an art style, with input:\n\n{destination_and_art_style}\n")
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = [system_message_for_extended_art_style_description, user_message_for_art_style]
        )
        assistant_prompt_with_extended_art_style_description = completion.choices[0].message.content
        extended_art_styles_descriptions.append(assistant_prompt_with_extended_art_style_description)
        print(f"\nthe extended art style description is:\n\n{assistant_prompt_with_extended_art_style_description}\n")

    art_styles_and_extended_descriptions = [f"location: {destination}\n\n" + destination_and_art_style + "\n\nDESCRIPTION:\n\n" + extended_art_style_description for (destination, destination_and_art_style, extended_art_style_description) in zip(destinations, destinations_and_art_styles, extended_art_styles_descriptions, strict = True)]

    art_styles_string = strings.separator.join(art_styles_and_extended_descriptions)
    art_styles_file = open(f"art-styles/art-styles_{timestamp}.txt", "w")
    art_styles_file.write(art_styles_string)
    art_styles_file.close()

    return None



### let's get some art styles!
get_art_styles_OLD(["tokyo", "kyoto", "cinqueterre"])