##### here are collected miscellaneous strings (and simple functions that return strings) that are used elsewhere.

from os import listdir
from os.path import isfile, join

def get_all_unhidden_files(directory):
    # make sure it's the name of a _file_, and make sure it's not a _hidden_file.
    return [filename for filename in listdir(directory + "/") if isfile(join(directory + "/", filename)) and filename[0] != "."]

# destination is e.g. "amalfi"
# directory is e.g. "story" or "stops"
# length is either "long" or "short"
    # example: executing get_latest_filename("algarve", "stories", "short") on 2023-11-24 returns:
    # story_algarve_2023-11-23_01-25-49_short.txt
def get_latest_filename(destination, directory, length = None):
    all_filenames = get_all_unhidden_files(directory)
    destination_filenames = [filename for filename in all_filenames if filename.split("_")[1] == destination]
    if length:
        destination_filenames = [filename for filename in destination_filenames if filename.split("_")[-1][:-4] == length]
    if len(destination_filenames) == 0:
        raise Exception(f"there are no files in `{directory}/` corresponding to the destination `{destination}`{' of length `' + length + '`' if length else ''}")
    destination_filenames.sort()
    return destination_filenames[-1]

#####

from datetime import datetime
def time_now():
    datetime_string = str(datetime.now())
    return datetime_string[:10] + "_" + datetime_string[11:13] + "-" + datetime_string[14:16] + "-" + datetime_string[17:19]

#####

# MISC SHORT STRINGS

# annoyingly, in python <3.12 you can't put a backslash in the expression portion of an f-string (and the virtual environment is stuck at python 3.11.6). so here's a workaround to allow for joining a list of strings with single or double newlines inside of an f-string.
n = "\n"
nn = "\n\n"

### below are a bunch of requests to chatGPT (indicated by `_plz` in the variable name), as well as related material.

## here are requests that get used for _every_ completion of _every_ story, as well as related material. at the end, they're wrapped into a single multi-line prompt string.

no_numbers_plz = "Please spell out any numbers in words. For instance, write 'nineteen eighty-seven' instead of '1987', and 'four thousand seven hundred and thirty three' instead of '4,733', and 'eighteen-sixties' instead of '1860s' (referring to the decade), and 'nineties' instead of '90s' (also referring to the decade)."

overused_words = [
    "tapestry",
    "testament",
    "grandeur",
    "symphony",
    "tribute",
    "serve",
    "homage",
    "tranquil",
    "chariot",
]
no_overused_words_plz = f"Please don't use any of the following words: {', '.join(overused_words)}."

# without this, chatGPT occasionally began each stop with a sort of "section title".
complete_sentences_plz = "Everything you write should be in complete sentences."

requests_for_every_completion_plz = "\n\n".join([
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

# SYSTEM PROMPTS

system_prompt_for_rewriting = f"""The user will give you text. Please rewrite the text so that all numbers are written out in words. This includes Roman numerals. So, the result should not have any digits or any Roman numerals. Please make sure that years are written out in the usual way that they're spoken. Please only respond with the rewritten text, and nothing else.

EXAMPLE: '1842' should be written out as 'eighteen forty-two' (and not 'one thousand eight hundred and forty-two').

EXAMPLE: '1906', when it is functioning as a year, should be written out as 'nineteen oh-six' (and not 'one thousand nine hundred and six' or 'nineteen hundred and six').

EXAMPLE: In the context of a vacation in Italy, '5Terre' (which is the name of a gelateria) should be written out as 'Cinque Terre' (which is the name of the region where the gelateria is located).

EXAMPLE: 'Louis XIV' should be written out as 'Louis the Fourteenth'.

EXAMPLE: 'Henry I' should be written out as 'Henry the First'.

EXAMPLE: 'Super Bowl XLII' should be written out as 'Super Bowl Forty Two'.

EXAMPLE: 'Star Wars Episode IV' should be written out as 'Star Wars Episode Four'.

EXAMPLE: 'Calculus I' should be written out as 'Calculus One' (this is the name of a math course).

EXAMPLE: 'I Gusti Nyoman Lempad' should actually NOT BE CHANGED, because this is a person's name. Please do not be confused by the fact that his first name is also a Roman numeral."""

#####

def user_prompt_for_stops(destination_fullname, num_stops, transport_method, requested_sightseeing_stops):
    return f"""I love traveling. I'm going on a trip to {destination_fullname}. Please name {num_stops} popular sightseeing locations there that I could visit by {transport_method}. {f"Please try to include {requested_sightseeing_stops} among these sightseeing locations." if requested_sightseeing_stops else ""}

Please list the sightseeing locations in an order so that no two adjacent sightseeing locations are too similar; for example, if one is a museum, the next would ideally be something like an outdoor market. Please only choose sightseeing locations that are calm and not even remotely controversial. For example, a beautiful park, a rose garden, a Buddhist temple, or a textiles museum would be a great choice of sightseeing location. A bullfight or a Holocaust museum would be a bad choice of sightseeing location.

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

#####

# USER PROMPTS FOR WRITING STORIES

def initial_user_prompt_for_story(length, destination_fullname, transport_method, tour_guide, season, stops, a):
    filler_length = ""
    filler_stops = ""
    if length == "long":
        filler_length = "Keep this short -- just three or four paragraphs. Please don't end your response with a summary, though, because we will be continuing the story!"
    elif length == "short":
        filler_length = "Keep this part short -- just a paragraph will do."
        filler_stops = f"Then, here {'are' if a>1 else 'is'} the first{' ' + str(a) if a>1 else ''} sightseeing location{'s' if a>1 else ''} for us to visit.{nn}{nn.join(stops[: a])}"
    filler_tour_guide = ""
    if tour_guide:
        filler_tour_guide = f"The tour guide is {tour_guide}. However, please don't give the tour guide a specific name; refer to them instead simply as 'our guide' (or similar)."
    return f"""Please begin by setting the scene.

We are traveling in {destination_fullname}; the season is {season}. We are taking a sightseeing tour by {transport_method}, although we may also walk around some as well. {filler_tour_guide} However, JUST set the scene; don't begin the sightseeing tour just yet. Make me excited about my trip overall, and about the upcoming tour. {filler_length}

{requests_for_every_completion_plz}

{no_ending_summary_plz}

{no_separator_in_intro_plz if length == 'short' else ''}

{filler_stops if length == 'short' else ''}"""

def middle_user_prompts_for_story(length, stops, a, c, n):
    middle_user_prompts = []
    if length == "long":
        for (index, stop) in enumerate(stops):
            middle_user_prompt = f"""Great, thank you! Here is the next sightseeing location:

{stop}

{requests_for_every_completion_plz}

{no_ending_summary_plz}"""
            if index == len(stops) - 1:
                middle_user_prompt += "\n\n" + no_starting_transition_plz
            middle_user_prompts.append(middle_user_prompt)
    elif length == "short":
        for j in range(c):
            middle_user_prompt = f"""Great, thank you! Here {'are' if n>1 else 'is'} the next{' ' + str(n) if n>1 else ''} sightseeing location{'s' if n>1 else ''}:

{nn.join(stops[a+n*j: a+n*(j+1)])}

{requests_for_every_completion_plz}

{no_ending_summary_plz}

{split_with_asterisks_plz if n>1 else ''}"""
            middle_user_prompts.append(middle_user_prompt)
    return middle_user_prompts

def final_user_prompt_for_story(length, destination_fullname, transport_method, stops, a, c, n, z):
    if length == "long":
        return f"Great, thank you! Please conclude the story about our sightseeing tour by {transport_method} in {destination_fullname}. Please keep it upbeat, gentle, and inspiring."
    elif length == "short":
        return f"""Great, thank you! Let's now conclude the story about our sightseeing tour by {transport_method} in {destination_fullname}. Please keep it upbeat, gentle, and inspiring. The remaining sightseeing location{'s are' if z>1 else ' is'} listed below.

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



