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

    artistic_style = "Victorian art"

    artistic_style_description = """Victorian art, which flourished during the reign of Queen Victoria from 1837 to 1901, encompasses a diverse range of artistic styles and movements. However, it is characterized by several overarching features and themes that reflect the cultural and social milieu of the time:

Historicism: Victorian art often drew inspiration from past artistic periods and styles. There was a revival of Gothic, Renaissance, and Classical motifs, reflecting a nostalgic fascination with history. This historicism was partly a response to the rapid changes and advancements of the Industrial Revolution.

Moral and Social Themes: Many Victorian artworks conveyed moral, social, or religious messages. They often depicted scenes of idealized virtue, the sanctity of family and home, or the consequences of vice and immorality. This reflects the era's strong moralizing tendency and its emphasis on social conformity and propriety.

Attention to Detail: Victorian artists were known for their meticulous attention to detail. This was evident in their elaborate and ornate representations of subjects, whether in painting, sculpture, or architecture. The detail-oriented approach was a reflection of the Victorian era's fascination with the natural world, as well as its broader cultural values of diligence and thoroughness.

Romanticism and Sentimentality: Early Victorian art was influenced by Romanticism, emphasizing emotion, nature, and the sublime. As the era progressed, there was also a trend towards sentimentality, with an emphasis on emotion and nostalgia, often expressed through idealized landscapes and scenes of domestic bliss.

Realism and Social Realism: In the latter half of the Victorian era, there was a move towards realism, partly influenced by the Pre-Raphaelite Brotherhood who sought to depict the world with great accuracy and detail. Artists began to address social issues and the realities of life in an industrial society, marking the beginnings of social realism.

Exoticism and Orientalism: Victorian art often featured exotic and oriental themes, reflecting the expansion of the British Empire and the increasing global connections of the time. Artworks frequently depicted scenes from the colonies, sometimes idealizing these cultures while at other times portraying them as mysterious and otherworldly.

Portraiture and the Cult of Celebrity: The Victorian era saw a boom in portraiture, fueled by the rising middle class and advancements in photography. There was also a fascination with celebrity culture, and many artists gained fame through their portraits of notable figures of the time.

Technological Influence: The Industrial Revolution had a significant impact on Victorian art. New technologies and materials influenced the production and distribution of art. Photography, in particular, emerged as a significant new medium, influencing both the subject matter and techniques of traditional art forms.

In summary, Victorian art is a rich tapestry of styles and themes, reflecting the complex social, cultural, and technological landscape of the 19th century. It ranges from historicism and romanticism to realism and social commentary, with a strong emphasis on detail, moral messages, and an engagement with both the past and the contemporary world."""

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

    for cue in cues:
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


