from openai import OpenAI
client = OpenAI()
gpt_model = "gpt-4-1106-preview" # was "gpt-4-32k", replaced 2023-11-16

from os import listdir # operating system; list the files in a directory
from os.path import isfile, join
txt_file_names_incl_hidden = [f for f in listdir("cues/") if isfile(join("stories/", f))]
txt_file_names = [file_name for file_name in txt_file_names_incl_hidden if file_name[0] != "."]
txt_file_names.sort() # make alphabetical, for reproduceability.




for txt_file_name in txt_file_names:

    print(f"txt_file_name is: {txt_file_name}")

    print(f"now getting dall-e prompts for {txt_file_name}")

    [destination, date, time, length] = txt_file_name[:-4].split("_")

    cues_string = open(f"cues/{txt_file_name}", "r").read()
    cues = cues_string.split("\n")

    artistic_style = "pop art"

    artistic_style_description = """Pop Art is a distinctive artistic style that emerged in the late 1950s and 1960s, primarily in the United States and the United Kingdom. It is characterized by several key features that set it apart from other art movements:

Emphasis on Popular Culture: Pop Art draws its subject matter from popular and mass culture, such as advertising, comic books, celebrity culture, and consumer goods. This was a significant shift from the traditional focus on more elitist themes in art, bringing a more accessible and relatable element to the art world.

Bold, Vibrant Colors: Pop Art is known for its use of bright, vivid colors. These colors are often used in flat, large areas to create a striking, graphic look. This use of color was influenced by the advertising and comic book styles of the time, which employed similar techniques to attract attention.

Use of Ben-Day Dots: A technique borrowed from comic strips and commercial printing, Ben-Day dots were used to create shading and secondary colors in Pop Art. This process involved the use of small colored dots closely spaced, overlapped, or separated to create different hues and effects.

Irony and Satire: Many Pop Art pieces have an ironic or satirical edge, often as a critique of consumerism, mass production, and the banality of everyday objects and icons. This approach was a stark contrast to the more serious and introspective tendencies of Abstract Expressionism, which preceded Pop Art.

Incorporation of Commercial Techniques: Pop Art artists often adopted techniques from commercial art and mass production, like screen printing. This allowed them to produce art in a manner that echoed the mass-produced nature of the objects and imagery they were depicting.

Simplicity and Boldness in Design: Pop Art is characterized by simple, bold lines and a clear, straightforward composition. This clarity was a deliberate choice to mimic the directness of advertising and to make the art more approachable.

Mix of High and Low Culture: Pop Art blurred the boundaries between 'high' art (like fine art) and 'low' culture (like commercial art and advertising). This mix was revolutionary at the time and challenged the traditional hierarchy and elitism in the art world.

Iconic Imagery: Pop Art often featured iconic images from popular culture, including famous celebrities, comic book characters, and everyday consumer goods. These images were often presented in new or challenging contexts to make the viewer see them in a different light.

In summary, Pop Art is a visually bold and culturally resonant art movement that emerged as a reaction against the elitism of traditional art. It uses the techniques, styles, and themes of popular and mass culture to create works that are both accessible and critically engaging, often with a sense of irony or satire."""

    system_prompt_for_dalle_prompts = f"""The user has written a travel story, and would like to obtain illustrations from DALL-E 3. Artistic guidelines are copied below. The entire story is copied further below, for context.

Each user message will contain a snippet from the story. For each snippet, please generate a prompt for DALL-E 3 to illustrate the snippet. The prompt should be as long as possible -- close to 1,000 words.

If the snippet does not contain anything that can be illustrated, please generate a prompt that is related to other surrounding material within the context of the full story. However, each prompt should be substantively different from the previous one.

Please do not include any text besides the prompt.

=====

ARTISTIC GUIDELINES:

Please make sure that EVERY prompt is designed to generate an image IN THE ARTISTIC STYLE LISTED BELOW. It is important that ALL of the prompts generate illustrations that are in the given style.

Please do NOT generate any illustration prompts that involve meat-based foods. For example, do NOT generate an illustration prompt with a lobster in a lobster roll.

Additionally, please make sure that the pictures do NOT include any people or body parts in the foreground -- especially hands. However, people in the middleground and background are great.

Please make sure that every picture has color. Please do not include any black-and-white pictures.

The artistic style is: {artistic_style.upper()}.

Here is a description of this artistic style.

{artistic_style_description}

=====

STORY:

{cues_string}"""

    system_message = {"role": "system", "content": system_prompt_for_dalle_prompts}

    dalle_prompts = []

    for cue in cues[:10]:
        print(f"asking chatGPT for a dalle prompt for the cue:\n{cue}")
        user_message = {"role": "user", "content": cue}
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = [system_message, user_message]
        )
        dalle_prompt = completion.choices[0].message.content
        dalle_prompt = dalle_prompt.replace("\n", " ") # later we'll split by "\n", so it's important not to have any stray ones.
        dalle_prompts.append(dalle_prompt)

    dalle_prompts_file = open(f"dalle_prompts/{txt_file_name}", "w")
    dalle_prompts_file.write("\n".join(dalle_prompts))
    dalle_prompts_file.close()

print(f"finished getting dalle prompts for {txt_file_name}")


