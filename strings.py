##### here are collected miscellaneous strings (and simple functions that return strings) that are used elsewhere.

from os import listdir
from os.path import isfile, join

import re

def get_all_unhidden_files(directory):
    # make sure it's the name of a _file_, and make sure it's not a _hidden_file.
    return [filename for filename in listdir(directory + "/") if isfile(join(directory + "/", filename)) and filename[0] != "."]

# key is e.g. "amalfi" or "impressionism".
# directory is e.g. "story" or "stops" or "art-style-descriptions".
# length is either "long" or "short", but this only applies to certain types of file.
    # example: executing get_latest_filename("algarve", "stories", "short") on 2023-11-24 returns:
    # story_algarve_2023-11-23_01-25-49_short.txt
# this may not work on all file types! for instance, our rewriting-log files have a slightly different naming convention, because their filenames indicate both the original unedited story (and in particular its timestamp) as well as the editing timestamp. so, modify this if necessary before using it on any new file types.
# if there's no such file, return `None`. raise an exception elsewhere _if desired_. (sometimes this will _not_ be desired, which is why we're not raising an exception here.)
def get_latest_filename(key, directory, length = None):
    all_filenames = get_all_unhidden_files(directory)
    key_filenames = [filename for filename in all_filenames if filename.split("_")[1] == key]
    if length:
        key_filenames = [filename for filename in key_filenames if filename.split("_")[-1][:-4] == length]
    if len(key_filenames) == 0:
        print(f"there are no files in `{directory}/` corresponding to the key `{destination}`{' of length `' + length + '`' if length else ''}")
        return None
    key_filenames.sort()
    return key_filenames[-1]

#####

from datetime import datetime
def time_now():
    datetime_string = str(datetime.now())
    return datetime_string[:10] + "_" + datetime_string[11:13] + "-" + datetime_string[14:16] + "-" + datetime_string[17:19]

#####

# we use double-quotes in our kotlin code to delineate cues, so this function replaces those with single-quotes.
def swap_quote_marks(string):
    return re.sub("\"", "'", string)

#####

# this function takes a (generally multi-line) string and prepend each line with `// ` (so that it becomes a comment in kotlin).
def kotlin_comment(string):
    lines = string.split("\n")
    commented_lines = ["// " + line for line in lines]
    comment = "\n".join(commented_lines)
    return comment

#####

# this function formats a list of cues into a single string of kotlin code. (it will have already had its double quote-marks replaced with single quote-marks.)
# the input will _not_ necessarily always be a single chunk; for instance, in writing a long story, we'll always attach the last stop's chunk to the end chunk for the `end` of the story.
# down dog linting uses 2 spaces per tab, and the cue strings will be indented by 2 tabs.
def format_list_of_cues_as_kotlin(list_of_cues):
    list_of_indented_and_quoted_cues = [f"    \"{cue_string}\"" for cue_string in list_of_cues]
    return " /\n".join(list_of_indented_and_quoted_cues)

#####

# MISC SHORT STRINGS

# annoyingly, in python <3.12 you can't put a backslash in the expression portion of an f-string (and the virtual environment is stuck at python 3.11.6). so, here's a workaround to allow for joining a list of strings with single or double newlines inside of an f-string.
n = "\n"
nn = "\n\n"

# we use this separator throughout the code. storing it as a variable helps ensure that this isn't screwed up by a typo. (namely, a typo will give a compilation error, instead of silently causing some screwy behavior that we hopefully notice and then have to chase down.)
separator = "\n\n=====\n\n"
separator_long = "\n\n==========\n\n"

### below are a bunch of requests to chatGPT (indicated by `_plz` in the variable name), as well as related material.

## here are requests that get used for _every_ completion of _every_ story, as well as related material. at the end, they're wrapped into a single multi-line prompt string.

no_numbers_plz = "Please spell out any numbers in words. For instance, write 'nineteen eighty-seven' instead of '1987', and 'four thousand seven hundred and thirty three' instead of '4,733', and 'eighteen-sixties' instead of '1860s' (referring to the decade), and 'nineties' instead of '90s' (also referring to the decade)."

# for replicability of the `edit_story` function, we should only add new overused words to the _end_ of this list. (specifically, in `edit_story.py` we use the index in the list.)
# the "pattern" is for regex searches in `edit_story.py`.
    # including "(?i)" in the pattern makes it case-insensitive.
    # the "\b" denotes a word boundary, so that e.g. "contribute" doesn't trigger "tribute".
# we may eventually add a "synonyms" property, containing a list of suggested replacements.
overused_words = [
    {
        "word": "tapestry",
        "pattern": r"(?i)\btapestr",
    },
    {
        "word": "testament",
        "pattern": r"(?i)\btestament",
    },
    {
        "word": "grandeur",
        "pattern": r"(?i)\bgrandeur",
    },
    {
        "word": "symphony",
        "pattern": r"(?i)\bsymphon",
    },
    {
        "word": "tribute",
        "pattern": r"(?i)\btribute",
    },
    {
        "word": "homage",
        "pattern": r"(?i)\bhomage",
    },
    {
        "word": "tranquil",
        "pattern": r"(?i)\btranquil",
    },
    {
        "word": "chariot",
        "pattern": r"(?i)\bchariot",
    },
    {
        "word": "mosaic",
        "pattern": r"(?i)\bmosaic",
    },
    {
        "word": "vibrant",
        "pattern": r"(?i)\bvibrant",
    },
    {
        "word": "bustling",
        "pattern": r"(?i)\bbustl",
    },
    {
        "word": "verdant",
        "pattern": r"(?i)\bverdant",
    }
]
no_overused_words_plz = f"Please don't use any of the following words: {', '.join([entry['word'] for entry in overused_words])}."

# without this, chatGPT occasionally began each stop with a sort of "section title".
complete_sentences_plz = "Everything you write should be in complete sentences."

requests_for_every_story_completion_plz = "\n\n".join([
    no_numbers_plz,
    no_overused_words_plz,
    complete_sentences_plz,
])

## here are requests that get used for _some_ but not all completions in the story-writing process.

# this applies to every completion besides the one that ends the story.
no_ending_summary_plz = "Please don't end your response with a summary, because we will be continuing the story and visiting more sightseeing locations!"

# this applies to the first completion of a short story, which (assuming a>0) come with a stop attached to the scene-setting material.
no_separator_in_intro_plz = "Please do NOT include any sort of separator between setting the scene and taking us to the first sightseeing location. (For instance, do NOT separate the introduction from the first stop with '---'.)"

# this applies just once in each story-writing -- .
    # for the long story, it applies to the last stop (which comes separately from the conclusion of the story), since we always include that.
    # for the short story, it applies to the last commpletion (and it's rolled in just below -- not elsewhere).
no_starting_transition_plz = """Additionally, at the beginning of your response, please do NOT refer to the sightseeing location where we've just been. Do not say where we are leaving from. Rather, just refer to our travel adventures in general terms.

GOOD EXAMPLE:

Our sightseeing tour continues as we make our ways towards...

BAD EXAMPLE:

As we make our way from the castle, ..."""

# this is used in the middle completions of the short story (assuming that n>1).
split_with_asterisks_plz = "Please separate the pieces of the story corresponding to the different sightseeing locations with five asterisks (i.e. the string '*****'). Please make sure to separate the sightseeing locations with five asterisks."

# this is used in the last completion of a short story.
no_separator_in_conclusion_plz = "Please do NOT include any sort of separator between the last sightseeing location and the conclusion of the story."

#####

# PROMPT(S) FOR REWRITING

def system_prompt_for_rewriting(overused_words_to_remove):
    return f"""The user will give you a chunk of text. Please rewrite this WITH MINIMAL CHANGES, according to the following TWO instructions.

1. All numbers should be written out in words. This includes Roman numerals. So, the result should not have any digits or any Roman numerals. Please make sure that years are written out in the usual way that they're spoken.

2. Please do NOT use any of the following "overused words" in the rewritten text: {', '.join(overused_words_to_remove)}. If you come across one of these "overused words", please simply substitute a common synonym, or else rewrite the text slightly with a different phrasing that avoids the "overused word".

Please respond ONLY with the rewritten text, and nothing else. Do not include any other text in your response.

=====

Here are some examples of rewrites relating to numbers.

EXAMPLE: '1842' should be written out as 'eighteen forty-two' (and not 'one thousand eight hundred and forty-two').

EXAMPLE: '1906', when it is functioning as a year, should be written out as 'nineteen oh-six' (and not 'one thousand nine hundred and six' or 'nineteen hundred and six').

EXAMPLE: In the context of a vacation in Italy, '5Terre' (which is the name of a gelateria) should be written out as 'Cinque Terre' (which is the name of the region where the gelateria is located).

EXAMPLE: 'Louis XIV' should be written out as 'Louis the Fourteenth'.

EXAMPLE: 'Henry I' should be written out as 'Henry the First'.

EXAMPLE: 'Super Bowl XLII' should be written out as 'Super Bowl Forty Two'.

EXAMPLE: 'Star Wars Episode IV' should be written out as 'Star Wars Episode Four'.

EXAMPLE: 'Calculus I' should be written out as 'Calculus One' (this is the name of a math course).

EXAMPLE: 'I Gusti Nyoman Lempad' should actually NOT BE CHANGED, because this is a person's name. Please do not be confused by the fact that his first name is also a Roman numeral.
"""

#####

# PROMPTS FOR STOPS

def user_prompt_for_stops(destination_fullname, num_stops, transport_method, requested_sightseeing_stops):
    return f"""I love traveling. I'm going on a trip to {destination_fullname}. Please name {num_stops} popular sightseeing locations there that I could visit by {transport_method}. {f"Please try to include {requested_sightseeing_stops} among these sightseeing locations." if requested_sightseeing_stops else ""}

Please list the sightseeing locations in an order such that no two adjacent sightseeing locations are too similar; for example, if one is a museum, the next would ideally be something like an outdoor market (and certainly not another museum!). Please only choose sightseeing locations that are calm and not even remotely controversial. For example, a beautiful park, a rose garden, a Buddhist temple, or a textiles museum would be a great choice of sightseeing location. A bullfight or a Holocaust museum would be a bad choice of sightseeing location.

Please separate the different sightseeing locations with five asterisks (i.e. the string '*****'). Please make sure to separate the sightseeing locations with five asterisks.

The entire tour should feel like a calm and soothing dream. Please make sure that NONE of these sightseeing locations is somber, stressful, or violent. For example, DO NOT include a tour of a Holocaust museum.

Please also include a one-line description of each sightseeing location. Here is an example, corresponding to a riverboat cruise in Paris.

EXAMPLE:

Eiffel Tower: An iconic symbol of France, this remarkable structure offers a stunning panoramic view of Paris. Your river cruise will provide a spectacular perspective of its beauty."""

def system_prompt_for_tidbits(destination_fullname):
    # removed on 2023-11-22:
        # If visiting the sightseeing location typically involves eating or drinking, please also include a typical dish or dining experience.
        # the transport method, in the sentence: Lastly, please also describe a pleasant human experience involved in visiting this sightseeing location by {input['transport_method']}.
    return f"""I am on a vacation to {destination_fullname}, and am taking a sightseeing tour in and around the area. I will name a sightseeing location on the tour. Associated to this sightseeing location, please list some historical facts, literary references, or relevant quotes -- at least three or four of these.

If the sightseeing location typically has other people about, please list one or two activities that those other people might be seen doing.

Lastly, please also describe a pleasant human experience involved in visiting this sightseeing location. Some examples might be: buying a ticket; consulting a map; taking in natural beauty such as plants, animals, clouds, trees, or sunshine. Please be specific in the experience you describe.

For each sightseeing location, please format the above items as a bullet-pointed list.

Please only give me tidbits for THIS sightseeing location. Please do not include information about any other sightseeing locations.

I will give you three SEPARATE examples below. EACH of these is an example of a complete response.

START OF EXAMPLE ONE

USER PROMPT: Berlin Television Tower (Fernsehturm)

EXAMPLE RESPONSE:
- At 368 meters, it's the tallest structure in Germany.
- The tower's sphere features a revolving restaurant.
- Constructed between 1965 and 1969 by the government of the German Democratic Republic (GDR).
- When you exit the adjacent subway stop, you suddenly see the Fernsehturm reaching towards the sunny sky.
- People like to take pictures of themselves where due to the perspective it looks like they're holding the Berlin Television Tower in their hand.

END OF EXAMPLE ONE

START OF EXAMPLE TWO

USER PROMPT: East Side Gallery

EXAMPLE RESPONSE:
- It's the longest remaining part of the Berlin Wall.
- Features over 100 murals by artists from all over the world.
- The most famous painting is the "Fraternal Kiss" between Brezhnev and Honecker.
- Next to the gallery is a world-famous currywurst stand.

END OF EXAMPLE TWO

START OF EXAMPLE THREE

USER PROMPT: Brandenburg Gate

EXAMPLE RESPONSE:
- Built in the 18th century as a symbol of peace.
- Napoleon once marched through the gate's arches to take the city.
- Ronald Reagan famously said, "Mr. Gorbachev, tear down this wall!" near this site.
- People love to feed the birds that congregate around the Brandenburg Gate.

END OF EXAMPLE THREE"""

#####

# PROMPTS FOR STORIES

def system_prompt_for_story(length, num_stops):
    if not (length == "long" or length == "short"):
        raise Exception('in system_prompt_for_story_template, the first argument should be one of the two strings \"long\" or "short"')
    filler = ""
    if length == "long":
        filler = f"{num_stops} different sightseeing locations there -- these will come one at a time"
    elif length == "short":
        filler = "a few different sightseeing locations"
    return f"""I'm going to give you a tourist destination, a mode of transportation, a season, and {filler}. Please write me a story like the example far below. Please make sure to write in the PRESENT TENSE. Please don't give the tour guide a specific name, referring to them instead as 'our guide' (or similar).

As I name each sightseeing location, I'm also going to give you some tidbits about it: historical facts, literary references, relevant quotes, typical dining experiences, and possibly also human experiences involved in visiting this sightseeing location by the chosen mode of transportation. Please try to include these. However, don't include more than THREE food experiences total.

Also, try to incorporate SPECIFIC tidbits; these are better than simply discussing the importance of a sightseeing location in general terms.

Please also include little moments describing our feelings as we take in these sights and sounds and tastes. These should all be pleasant and inspiring feelings.

Please don't include anything somber, stressful, or violent. Keep the tone happy, warm, uplifting, and relaxing.

Additionally, the entire story should be gentle and calming, like a pleasant dream -- conducive to falling asleep. For example, please do include words like:
- gentle,
- lapping,
- undulating,
- soothing,
- quiet,
- peaceful,
- comfortable.
By contrast, please do NOT include words or phrases like the following:
- thrilling,
- flurry,
- amplified,
- eager,
- adventure,
- racing hearts,
- swiftly.

As we go from spot to spot, please transition us between them through pleasant tourist activities such as walking, buying a ticket, looking at the map to find our way, etc. You can also refer to activities related to our chosen mode of transportation, such as getting on or off of a rickshaw.

Don't end the story until I tell you to. Don't reference the passing of time or the time of day.

In general, I want you to be concrete and descriptive, naming specific things that we see and do and what they represent. I particularly want you to describe people going about their activities. We can occasionally have brief and pleasant interactions with them. Here are two examples of ways that I would rewrite text that you (ChatGPT) have written before.

START EXAMPLE REWRITE ONE:

OLD TEXT:

Local artisans with worn and skillful hands bring clay to life in the form of intricate ceramics, while others shape silver into delicate pieces of wearable art.

NEW TEXT:

In an obscure corner of the workshop, a seasoned artisan with hands toughened and lined by years of diligent dedication hunches over a misshapen lump of clay. With an intuitive touch, he gently coaxes the lifeless material, his fingers carving intricate patterns that whisper ancient tales. Quiet concentration etches deeper creases on his weathered face as he transforms mere earth into a fragile piece of ceramic art.

Across the room, his associate, a stalwart silhouette against the flickering glow of the forge, threads a sinewy strand of silver through a weather-worn fingertip. Twisting and turning with careful precision, he molds the raw metal into an exquisite wearable piece of art. His eyes glint with reflected light and unwavering determination, while his hands orchestrate a silent symphony, bringing a dreamy luminescence to the material.

END EXAMPLE REWRITE ONE.


START EXAMPLE REWRITE TWO:

OLD TEXT:

The National Museum of Anthropology in Mexico City offers more than just a stroll down the country's ancient past; it continues to narrate the story of Mexico's present-day indigenous groups. In-depth ethnographic exhibits open windows to the diverse and vibrant life of the many indigenous cultures still thriving in Mexico today, highlighting their languages, traditions, and everyday life.

NEW TEXT:

The main attraction in Nahua Hall is a splendid array of traditional costumes worn by Nahua communities. The costumes often consist of two-part attires - blouses known as 'huipil' and skirts known as 'enredo'. These are often adorned with detailed motifs that depict local livestock, crops, and scenery, each symbolizing a different aspect of the Nahua worldview and mythology.

The colors used in the blouses, skirts, and rebozos (a traditional garment similar to a shawl) are bold, organic, and eye-catching. You will find primary colors - reds, blues, greens, often alternating with secondary hues such as purple and orange, to tell vibrant stories of each garment's unique roots.

The huipil, typically made of cotton, is a square-cut, loose sleeveless tunic. Its vibrant surface teems with delicate embroidery and exquisite beadwork; flower motifs, birds, and symbols related to ancient Nahua gods are common elements.

END EXAMPLE REWRITE TWO.

=====

EXAMPLE STORY:\n\n""" + open("example_story.txt", "r").read()

def initial_user_prompt_for_story(length, destination_fullname, transport_method, tour_guide, season, stops, a):
    filler_length = ""
    filler_stops = ""
    if length == "long":
        filler_length = "Keep this to just TWO PARAGRAPHS. Please don't end your response with a summary, because we will be continuing the story!"
    elif length == "short":
        filler_length = "Keep this part short -- just a paragraph or two."
        filler_stops = f"Then, here {'are' if a>1 else 'is'} the first{' ' + str(a) if a>1 else ''} sightseeing location{'s' if a>1 else ''} for us to visit.{nn}{nn.join(stops[: a])}"
    filler_tour_guide = ""
    if tour_guide:
        filler_tour_guide = f"The tour guide is {tour_guide}. However, please don't give the tour guide a specific name; refer to them instead simply as 'our guide' (or similar)."
    return f"""Please begin by setting the scene.

We are traveling in {destination_fullname}; the season is {season}. We are taking a sightseeing tour by {transport_method}, although we may also walk around some as well. {filler_tour_guide} However, JUST set the scene; don't begin the sightseeing tour just yet. Make me excited about my trip overall, and about the upcoming tour. {filler_length}

{requests_for_every_story_completion_plz}

{no_ending_summary_plz}

{no_separator_in_intro_plz if length == 'short' else ''}

{filler_stops if length == 'short' else ''}"""

def middle_user_prompts_for_story(length, stops, a, c, n):
    middle_user_prompts = []
    if length == "long":
        for (index, stop) in enumerate(stops):
            middle_user_prompt = f"""Great, thank you! Here is the next sightseeing location:

{stop}

{requests_for_every_story_completion_plz}

{no_ending_summary_plz}"""
            if index == len(stops) - 1:
                middle_user_prompt += "\n\n" + no_starting_transition_plz
            middle_user_prompts.append(middle_user_prompt)
    elif length == "short":
        for j in range(c):
            middle_user_prompt = f"""Great, thank you! Here {'are' if n>1 else 'is'} the next{' ' + str(n) if n>1 else ''} sightseeing location{'s' if n>1 else ''}:

{nn.join(stops[a+n*j: a+n*(j+1)])}

{requests_for_every_story_completion_plz}

{no_ending_summary_plz}

{split_with_asterisks_plz if n>1 else ''}"""
            middle_user_prompts.append(middle_user_prompt)
    return middle_user_prompts

def final_user_prompt_for_story(length, destination_fullname, transport_method, stops, a, c, n, z):
    if length == "long":
        return f"Great, thank you! Please conclude the story about our sightseeing tour by {transport_method} in {destination_fullname}. Please keep it upbeat, gentle, and inspiring. Keep the ending to just TWO PARAGRAPHS."
    elif length == "short":
        return f"""Great, thank you! Let's now conclude the story about our sightseeing tour by {transport_method} in {destination_fullname}. Please keep it upbeat, gentle, and inspiring. The remaining sightseeing location{'s are' if z>1 else ' is'} listed below. After we finish visiting those locations, please keep the concluding material to AT MOST TWO PARAGRAPHS.

{no_separator_in_conclusion_plz}

{no_starting_transition_plz}

=====

REMAINING SIGHTSEEING LOCATION{'S' if z>1 else ''}:

{nn.join(stops[a+c*n:a+c*n+z])}"""

def user_prompt_for_ending_long_story(destination_fullname, transport_method):
    return f"Great, thank you! Please conclude the story about our sightseeing tour by {transport_method} in {destination_fullname}. Keep it upbeat, gentle, and inspiring."

def user_prompt_for_ending_short_story(destination_fullname, transport_method, remaining_stops, z):
    return f"""Great, thank you! Let's now conclude the story about our sightseeing tour by {transport_method} in {destination_fullname}. The remaining sightseeing location{'s are' if z>1 else ' is'} listed below.

{no_separator_in_conclusion_plz}

{no_starting_transition_plz}

=====

REMAINING SIGHTSEEING LOCATION{'S' if z>1 else ''}:

{''.join(remaining_stops)}"""

#####

# PROMPTS FOR ART STYLE DESCRIPTIONS

def user_prompt_for_art_style_description(art_style):
    
    return f"""I am writing a travel story, and I want to include illustrations made by DALL-E that consistently conform to the following style of art:

{art_style}

Please give me an extended description of this art style that is SPECIFICALLY TAILORED TO help create DALL-E prompts that are in this art style.

=====

EXAMPLE INPUT:

pop art

EXAMPLE OUTPUT:

Pop Art is a distinctive artistic style that emerged in the late 1950s and 1960s, primarily in the United States and the United Kingdom. It is characterized by several key features that set it apart from other art movements:

Emphasis on Popular Culture: Pop Art draws its subject matter from popular and mass culture, such as advertising, comic books, celebrity culture, and consumer goods. This was a significant shift from the traditional focus on more elitist themes in art, bringing a more accessible and relatable element to the art world.

Bold, Vibrant Colors: Pop Art is known for its use of bright, vivid colors. These colors are often used in flat, large areas to create a striking, graphic look. This use of color was influenced by the advertising and comic book styles of the time, which employed similar techniques to attract attention.

Use of Ben-Day Dots: A technique borrowed from comic strips and commercial printing, Ben-Day dots were used to create shading and secondary colors in Pop Art. This process involved the use of small colored dots closely spaced, overlapped, or separated to create different hues and effects.

Irony and Satire: Many Pop Art pieces have an ironic or satirical edge, often as a critique of consumerism, mass production, and the banality of everyday objects and icons. This approach was a stark contrast to the more serious and introspective tendencies of Abstract Expressionism, which preceded Pop Art.

Incorporation of Commercial Techniques: Pop Art artists often adopted techniques from commercial art and mass production, like screen printing. This allowed them to produce art in a manner that echoed the mass-produced nature of the objects and imagery they were depicting.

Simplicity and Boldness in Design: Pop Art is characterized by simple, bold lines and a clear, straightforward composition. This clarity was a deliberate choice to mimic the directness of advertising and to make the art more approachable.

Mix of High and Low Culture: Pop Art blurred the boundaries between 'high' art (like fine art) and 'low' culture (like commercial art and advertising). This mix was revolutionary at the time and challenged the traditional hierarchy and elitism in the art world.

Iconic Imagery: Pop Art often featured iconic images from popular culture, including famous celebrities, comic book characters, and everyday consumer goods. These images were often presented in new or challenging contexts to make the viewer see them in a different light.

In summary, Pop Art is a visually bold and culturally resonant art movement that emerged as a reaction against the elitism of traditional art. It uses the techniques, styles, and themes of popular and mass culture to create works that are both accessible and critically engaging, often with a sense of irony or satire."""

#####

# PROMPTS FOR DALLE PROMPTS

def system_prompt_for_dalle_prompts(destination_fullname, art_style_fullname, art_style_description):
    return f"""The user has written a travel story set in {destination_fullname}, and would like to obtain illustrations from DALL-E 3. Your job will be to write illustration prompts. Artistic guidelines are copied below. Please make sure that ALL the prompts that you write adhere to the artistic guidelines.

Each user message will contain a short snippet from the story, as well as the larger context from which the snippet is taken. For each short snippet, please generate a prompt for a DALL-E 3 illustration. Ideally this will illustrate the snippet itself, but if this is not easy then it can also illustrate some nearby text from the larger context. Also, ideally each illustration prompt will be substantively different from the previous one.

Please do not respond with any text besides the illustration prompt. The illustration prompt should be as long as possible -- close to 1,000 characters (which is the length limit for DALL-E 3 prompts).

=====

ARTISTIC GUIDELINES:

Please make sure that EVERY illustration prompt is designed to generate an image IN THE ARTISTIC STYLE LISTED BELOW. It is important that ALL of the illustration prompts generate illustrations that are in the given style.

Please do NOT generate any illustration prompts that involve meat-based foods. For example, do NOT generate an illustration prompt for a picture of a lobster in a lobster roll.

Additionally, please make sure that the prompts do NOT describe illustrations that have any people or body parts in the foreground -- especially hands. However, please DO include people in the middleground and background when possible.

Please make sure that every picture has color. Please do not include any black-and-white pictures.

These prompts will be for images of size 1024x1792. Please make sure that every picture fills the ENTIRE frame, rather than having blank space at the top or bottom. Here are some tips to help with this.

* Explicit Orientation Description: Clearly state in your prompt that the scene or subject should be vertical or portrait-oriented. For example, "A portrait-oriented scene of a tall building against a cloudy sky" emphasizes the vertical alignment.

* Specify Full-Body or Vertical Elements: Since 1024x1792 is a vertical format, ensure your prompt describes a scene or subject that naturally fits this shape. For instance, full-body portraits, tall structures, or vertical landscapes work well.

* Detail the Foreground and Background: Provide details about what should be in the foreground and the background. This helps fill up the vertical space more effectively.

* Use Vertical Composition: Encourage a vertical composition in your prompt. For example, if you're asking for a character, describe them in a standing pose, or if it's a landscape, focus on elements like tall trees or a waterfall.

* Mention the Entire Scene: Describe the entire scene from the bottom to the top. This could include the ground, middle elements, and the sky or ceiling in indoor scenes.

* Avoid Broad or Ambiguous Descriptions: Vague descriptions can lead to simpler or less filled-in images. Be as specific as possible about what you want to see throughout the entire image.

* Request Detailed Elements: Adding details like intricate clothing on characters, detailed foliage in nature scenes, or ornate elements in architectural designs can help utilize the space better.

=====

LOCATION: {destination_fullname}

ART STYLE: {art_style_fullname}

DESCRIPTION:

{art_style_description}"""
