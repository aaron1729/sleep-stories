from openai import OpenAI
client = OpenAI()
gpt_model = "gpt-4-1106-preview" # was "gpt-4-32k", replaced 2023-11-16

import re # regular expressions

from datetime import datetime
def datetime_str_to_timestamp(str):
    return str[:10] + "_" + str[11:13] + "-" + str[14:16] + "-" + str[17:19]

start_time = str(datetime.now())
timestamp = datetime_str_to_timestamp(start_time)



##### PARAMETERS

num_stops = 2

write_long_story = True
write_short_story = False



# these are organized alphabetically by destination name.
inputs = [
    # {
    #     "destination": "algarve",
    #     "destination_fullname": "The Algarve, Portugal",
    #     "transport_method": "rental car for coastal drives",
    #     "requested_sightseeing_stops": "a boat trip to explore sea caves with an amiable captain",
    #     "tour_guide": None,
    #     "season": "spring",
    # },
    # {
    #     "destination": "amalfi",
    #     "destination_fullname": "Amalfi Coast, Italy",
    #     "transport_method": "Vespa scooter",
    #     "requested_sightseeing_stops": "coastal boat tour with a friendly captain",
    #     "tour_guide": None,
    #     "season": "spring",
    # },
    # {
    #     "destination": "bali",
    #     "destination_fullname": "Bali, Indonesia",
    #     "transport_method": "car with a young woman driver who is also a tour guide and also rental scooters",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": None,
    #     "season": "spring",
    # },
    {
        "destination": "bangkok",
        "destination_fullname": "Bangkok, Thailand",
        "transport_method": "tuk-tuk (i.e. a rickshaw)",
        "requested_sightseeing_stops": "Chatuchak weekend market",
        "tour_guide": "our tuk-tuk driver",
        "season": "winter",
    },
    # {
    #     "destination": "barcelona",
    #     "destination_fullname": "Barcelona, Spain",
    #     "transport_method": "guided bike tour",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": "an affable university student who double-majors in art and history as a tour guide",
    #     "season": "early fall",
    # },
    # {
    #     "destination": "berkeley",
    #     "destination_fullname": "Berkeley, California",
    #     "transport_method": "a Toyota Prius",
    #     "requested_sightseeing_stops": "a hike in Tilden Park",
    #     "tour_guide": None,
    #     "season": "spring",
    # },
    # {
    #     "destination": "chiangmai",
    #     "destination_fullname": "Chiang Mai, Thailand",
    #     "transport_method": "tuk-tuk (i.e. rickshaw)",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": None,
    #     "season": "winter",
    # },
    # {
    #     "destination": "cinqueterre",
    #     "destination_fullname": "Cinque Terre, Italy",
    #     "transport_method": "a leisurely boat trip",
    #     "requested_sightseeing_stops": "hiking the trails between the villages",
    #     "tour_guide": None,
    #     "season": "spring",
    # },
    # {
    #     "destination": "costarica",
    #     "destination_fullname": "Costa Rica",
    #     "transport_method": "camper van",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": None,
    #     "season": "dry season",
    # },
    # {
    #     "destination": "dubai",
    #     "destination_fullname": "Dubai, United Arab Emirates",
    #     "transport_method": "private limousine",
    #     "requested_sightseeing_stops": "a ride in an abra (i.e. a traditional boat) on Dubai Creek",
    #     "tour_guide": None,
    #     "season": "winter",
    # },
    # {
    #     "destination": "greece",
    #     "destination_fullname": "Greece",
    #     "transport_method": "catamaran",
    #     "requested_sightseeing_stops": "a donkey ride on Santorini",
    #     "tour_guide": "catamaran captain",
    #     "season": "spring",
    # },
    # {
    #     "destination": "istanbul",
    #     "destination_fullname": "Istanbul, Turkey",
    #     "transport_method": "ferry ride on the Bosphorous",
    #     "requested_sightseeing_stops": "riding the historic tram on Istiklal Avenue",
    #     "tour_guide": None,
    #     "season": "spring",
    # },
    # {
    #     "destination": "kyoto",
    #     "destination_fullname": "Kyoto, Japan",
    #     "transport_method": "rickshaw",
    #     "requested_sightseeing_stops": "bicycling from Kyoto Station to the Kyoto Botanical Gardens along the Kamo-gawa River",
    #     "tour_guide": "our rickshaw driver, a jovial middle-aged man",
    #     "season": "spring",
    # },
    # {
    #     "destination": "london",
    #     "destination_fullname": "London, England",
    #     "transport_method": "the Tube subway, and also a double-decker bus",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": "the driver of our double-decker bus, a middle-aged British man with an attention to detail that rivals Sherlock Holmes",
    #     "season": "spring",
    # },
    # {
    #     "destination": "napa",
    #     "destination_fullname": "Napa Valley, California",
    #     "transport_method": "wine train",
    #     "requested_sightseeing_stops": "a ride in a hot air balloon",
    #     "tour_guide": None,
    #     "season": "fall",
    # },
    # {
    #     "destination": "newyorkcity",
    #     "destination_fullname": "New York, New York",
    #     "transport_method": "open-top bus tour and Metro",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": "a middle-aged man with a thick Brooklyn accent whose family has been in New York City for many generations",
    #     "season": "fall",
    # },
    # {
    #     "destination": "paris",
    #     "destination_fullname": "Paris, France",
    #     "transport_method": "Seine river cruise and Paris Metro",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": "a man in his early 40s who wears a beret and neckerchief and speaks with just a slight French accent",
    #     "season": "spring",
    # },
    # {
    #     "destination": "queenstown",
    #     "destination_fullname": "Queenstown, New Zealand",
    #     "transport_method": "water taxis",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": None,
    #     "season": "summer",
    # },
    # {
    #     "destination": "rio",
    #     "destination_fullname": "Rio de Janeiro, Brazil",
    #     "transport_method": "limousine",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": "our limousine driver, a quiet but friendly man in his early 50s who is aging gracefully",
    #     "season": "late spring",
    # },
    # {
    #     "destination": "shanghai",
    #     "destination_fullname": "Shanghai, China",
    #     "transport_method": "Shanghai Metro",
    #     "requested_sightseeing_stops": "a Huangpu River cruise",
    #     "tour_guide": None,
    #     "season": "fall",
    # },
    # {
    #     "destination": "tokyo",
    #     "destination_fullname": "Tokyo, Japan",
    #     "transport_method": "Tokyo metro train and Toei subway system",
    #     "requested_sightseeing_stops": None,
    #     "tour_guide": "a gregarious but soft-spoken young woman",
    #     "season": "spring",
    # },
]

################################################################################

##### dedigitization
##### ##### UPDATE: throughout this code, "digit" also refers to roman numerals.

# regex pattern for roman numerals (preceded by a space). it's copied from here, with the ends stripped off and then preceded by a space and followed by a non-word character:
    # https://stackoverflow.com/a/267405/19327500
# pattern_for_roman_numerals = r" M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\W"
# updated version 2023-11-21: this was too complicated, and seemed to be triggering all over the place. we don't need a _valid_ roman numeral per se, we just want to catch them (and we only check once). so, do something much simpler.
pattern_for_roman_numerals = r"[IVXLCDM][^a-zA-Z]"

# input: a string (which for us will be an entire completion coming back from chatGPT), and a number of rewrites to attempt before moving on.
# outputs (implicitly formatted as a tuple):
    # the hopefully-fixed string
    # a boolean of whether it was modified at all
    # a list of the versions that contain digits
    # a boolean of whether the final rewrite failed

def dedigitize(string, rewrites=3):
    any_nums = bool(re.search(r'\d', string)) or bool(re.search(pattern_for_roman_numerals, string))
    if not any_nums:
        return string, False, [], False
    versions_with_digits = [string]
    for _ in range(rewrites):
        system_prompt = f"""The user will give you text. Please rewrite the text so that all numbers are written out in words. This includes Roman numerals. So, the result should not have any digits or any Roman numerals. Please make sure that years are written out in the usual way that they're spoken. Please only respond with the rewritten text, and nothing else.

EXAMPLE: '1842' should be written out as 'eighteen forty-two' (and not 'one thousand eight hundred and forty-two').

EXAMPLE: '1906', when it is functioning as a year, should be written out as 'nineteen oh-six' (and not 'one thousand nine hundred and six' or 'nineteen hundred and six').

EXAMPLE: In the context of a vacation in Italy, '5Terre' (which is the name of a gelateria) should be written out as 'Cinque Terre' (which is the name of the region where the gelateria is located).

EXAMPLE: 'Louis XIV' should be written out as 'Louis the Fourteenth'.

EXAMPLE: 'Henry I' should be written out as 'Henry the First'.

EXAMPLE: 'Super Bowl XLII' should be written out as 'Super Bowl Forty Two'.

EXAMPLE: 'Star Wars Episode IV' should be written out as 'Star Wars Episode Four'.

EXAMPLE: 'Calculus I' should be written out as 'Calculus One' (this is the name of a math course).

EXAMPLE: 'I Gusti Nyoman Lempad' should actually NOT BE CHANGED, because this is a person's name. Please do not be confused by the fact that his first name is also a Roman numeral."""
        system_message = {"role": "system", "content": system_prompt}
        user_message = {"role": "user", "content": string}
        print("asking chatGPT to rewrite text without digits")
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = [system_message, user_message]
        )
        string = completion.choices[0].message.content
        # starting here, _don't_ keep looking for roman numerals, because there _is_ the possibility that a legitimate roman numeral shows up as _not_ a roman numeral. the main thing is 'I' (first person singular), but 
        # justification: after 15 instances of this function running while writing a story, chatGPT _always_ made a passing rewrite on the first try. (these only tested removal of digits, not roman numerals, but oh well.)
        any_nums = bool(re.search(r'\d', string)) # or bool(re.search(pattern_for_roman_numerals, string))
        if not any_nums:
            return string, True, versions_with_digits, False
        versions_with_digits.append(string)
    return string, True, versions_with_digits, True

# apply the `dedigitize` function, return the hopefully-correct string, and log if applicable.
def dedigitize_and_log(string):
    output, modified, versions_with_digits, failed = dedigitize(string)
    if modified:
        dedigitizations.append({"original": versions_with_digits[0], "failed_rewrites": versions_with_digits[1: ], "final": output, "failed": failed})
    return output

################################################################################

##### record the replacements and write files

# now that the story is finished, if any digit replacements were made, then:
    # write them to a replacement_log file;
    # store just the individual sentences at the end of the story file (for compilation into kotlin code -- perhaps at the top, commented-out);
    # regardless, also save the replacement stats.

def log_replacements_and_write_files(story, length):
        
    ### record replacement stats.

    nums_of_attempts = []
    any_failures = False
    # the dedigitizations list will have been created through the process of writing the story.
    for dedigitization in dedigitizations:
        nums_of_attempts.append(len(dedigitization['failed_rewrites']) + 1)
        if dedigitization['failed']:
            any_failures = True
    replacement_stats_string = f"{input['destination']}_{timestamp}_{length}.txt\nattempts per dedigitization: " + ", ".join([str(num) for num in nums_of_attempts]) + f"\nany failures: {str(any_failures)}\n\n"
    replacement_stats_file = open("logs/replacement_stats.txt", "a")
    replacement_stats_file.write(replacement_stats_string)
    replacement_stats_file.close()

    ### if there are any failures, make a replacement_failure_log file.

    if any_failures:
        replacement_failure_log_file = open(f"logs/replacement_failure_logs/{input['destination']}_{timestamp}_{length}.txt", "w")
        replacement_failure_log_file.write("FAILED! SAD!")
        replacement_failure_log_file.close()

    ### if there were any replacements, save each pair -- the old and new sentences -- together in a single object. (these get used just below.)
    ### the full replacements -- the old and new chunks -- get written to a replacement_log file.

    sentence_replacement_pairs = []

    if len(dedigitizations) > 0:
        replacement_log = "\n==========\n\n"
        for dedigitization in dedigitizations:

            # write some replacement_log material.

            replacement_log += f"REPLACEMENT FAILED: {str(dedigitization['failed'])} \n\n=====\n\n"
            if dedigitization["failed"]:
                replacement_log = "WARNING: A REPLACEMENT HEREIN HATH FAILED\n\n" + replacement_log
            replacement_log += f"ORIGINAL TEXT:\n\n{dedigitization['original']}\n\n=====\n\n"
            replacement_log += "\n\n=====\n\n".join(["FAILED REWRITES:"] + dedigitization['failed_rewrites'] + [""])
            replacement_log += f"FINAL VERSION:\n\n{dedigitization['final']}\n\n==========\n\n"

            # store replaced sentences and their replacements.

            original_sentences = dedigitization['original'].split(".")
            original_sentences_with_digits = [sentence for sentence in original_sentences if bool(re.search(r'\d', sentence)) or bool(re.search(pattern_for_roman_numerals, sentence))]
            new_sentences_with_digits_removed = []

            for sentence in original_sentences_with_digits:

                # do a regex search for a cleaned-up version of the sentence.
                sentence_split = re.split(r'\W', sentence)
                sentence_split_filtered = []
                for word in sentence_split:
                    if len(word) > 3 and not bool(re.search(r'\d', word)) and not bool(re.search(pattern_for_roman_numerals, word)):
                        sentence_split_filtered.append(word)
                pattern_for_replacing_sentence = r".*".join(sentence_split_filtered)
                match_obj = re.search(pattern_for_replacing_sentence, story)

                # this pattern _might_ not actually match, e.g. if chatGPT changes a word or two around. so, just handle that separately.
                    # real-life example:
                        # regex pattern: Stepping.*guide.*leads.*engaging.*journey.*from.*Street.*subway.*stop.*museum.*entrance
                        # would-be match: Stepping off the bus, our guide takes us on a captivating journey from the Eighty-sixth Street subway stop to the museum's entrance.
                    # note: "leads" became "takes", and also "engaging" became "captivating".
                if match_obj:
                    start, end = match_obj.span()
                    match_string = story[start: end]
                    # in case the original sentence actually started or ended with a number, go catch some extra characters at the front and back (assuming they exist). however, don't include any "\n" in this, just to keep things looking nice and pretty in the .kt file comments.
                    pad_size = 10
                    pad_left_index = max(start - pad_size, 0)
                    pad_left_string = story[pad_left_index: start]
                    pad_left_string_trimmed = re.split("\n", pad_left_string)[-1]
                    pad_right_index = min(end + pad_size, len(story))
                    pad_right_string = story[end: pad_right_index]
                    pad_right_string_trimmed = re.split("\n", pad_right_string)[0]
                    new_sentence_with_digits_removed = pad_left_string_trimmed + match_string + pad_right_string_trimmed
                    new_sentences_with_digits_removed.append(new_sentence_with_digits_removed)
                else:
                    new_sentences_with_digits_removed.append(f"match not found! please search for the replacement manually. fyi, the regex pattern is: {str(pattern_for_replacing_sentence)}")
            
            # the strict=True here checks that these lists have the same length (and throws an error if they don't).
            for old_sentence, new_sentence in zip(original_sentences_with_digits, new_sentences_with_digits_removed, strict=True):
                sentence_replacement_pairs.append({"old": old_sentence, "new": new_sentence})
        
        # write the replacement_log file (assuming there were any dedigitizations).

        replacement_log_file = open(f"logs/replacement_logs/{input['destination']}_{timestamp}_{length}.txt", "w")
        replacement_log_file.write(replacement_log)
        replacement_log_file.close()
    
    ### write the individual sentence replacements to the end of the story file.

    replacements_string = "\n\n=====\n\nREPLACED_SENTENCES:"
    for sentence_replacement_object in sentence_replacement_pairs:
        replacements_string += f"\n\nOLD SENTENCE: {sentence_replacement_object['old']}\nNEW SENTENCE: {sentence_replacement_object['new']}"

    story += replacements_string

    ### write the story file.

    story_file = open(f"stories/{input['destination']}_{timestamp}_{length}.txt", "w")
    story_file.write(story)
    story_file.close()

    story_end_time = datetime_str_to_timestamp(str(datetime.now()))
    print(f"finished writing {length} story set in {input['destination_fullname']} with timestamp {timestamp} at:", story_end_time)

    return None

################################################################################

##### enforce length constraints. written on 2023-11-21, but later trashed. it kinda sucks: it can take a _lot_ of runs through the `while` loop for chatGPT to get the length right, and e.g. sometimes it even goes in the wrong direction (i.e. more words instead of FEWER (let alone less) when it's trying to cut the word count). of course, a safer version would cap the number of attempts and log errors.

# def length_plz(min, max):
#     return f"\n\nPlease ensure that your response is between {min} and {max} words."

# def validate_length(string, min, max):
#     print("inside validate_length")
#     word_count = len(re.findall(r"\w+", string))
#     print(f"current word count is {word_count}")
#     while word_count < min or word_count > max:
#         print(f"asking chatGPT to fix word count: current is {word_count}, whereas target is between {min} and {max}")
#         system_prompt = f"""The user will provide you with a block of text, which has {word_count} words. Please rewrite it to have between {min} and {max} words.

# {"Since the given block of text is too short, please feel free to add further embellishments to achieve this goal." if word_count < min else ""}{"Since the given block of text is too long, please feel free to remove minor details to achieve this goal." if word_count > max else ""}

# Please do not respond with anything besides the rewritten text itself."""
#         system_message = {"role": "system", "content": system_prompt}
#         user_message = {"role": "user", "content": string}
#         completion = client.chat.completions.create(
#             model = gpt_model,
#             messages = [user_message]
#         )
#         string = completion.choices[0].message.content
#         word_count = len(re.findall(r"\w+", string))
#         print(f"the new string returned from chatGPT is:\n{string}")
#         print(f"and its word count is {word_count}")
#     print("string passes length validation")
#     return string

################################################################################

for input in inputs:

    print(f"\nwriting a sleep story set in {input['destination_fullname']} with timestamp {timestamp} at {datetime_str_to_timestamp(str(datetime.now()))}\n")

    ##### GET LIST OF STOPS

    user_prompt_for_stops = f"""
I love traveling. I'm going on a trip to {input['destination']}. Please name {num_stops} popular sightseeing locations there that I could visit by {input['transport_method']}. {f"Please try to include {input['requested_sightseeing_stops']} among these sightseeing locations." if input['requested_sightseeing_stops'] else ""}

Please list the sightseeing locations in an order so that no two adjacent sightseeing locations are too similar; for example, if one is a museum, the next would ideally be something like an outdoor market. Please only choose sightseeing locations that are calm and not even remotely controversial. For example, a beautiful park, a rose garden, a Buddhist temple, or a textiles museum would be a great choice of sightseeing location. A bullfight or a Holocaust museum would be a bad choice of sightseeing location.

Please separate the different sightseeing locations with five asterisks (i.e. the string '*****'). Please make sure to separate the sightseeing locations with five asterisks.

The entire tour should feel like a calm and soothing dream. Please make sure that NONE of these sightseeing locations is somber, stressful, or violent. For example, DO NOT include a tour of a Holocaust museum.

Please also include a one-line description of each sightseeing location. Here is an example, corresponding to a riverboat cruise in Paris.

EXAMPLE:

Eiffel Tower: An iconic symbol of France, this remarkable structure offers a stunning panoramic view of Paris. Your river cruise will provide a spectacular perspective of its beauty.
    """
    user_message_for_stops = {"role": "user", "content": user_prompt_for_stops}
    messages_for_getting_stops = [user_message_for_stops]

    print(f"getting list of {num_stops} stops\n")
    completion = client.chat.completions.create(
        model = gpt_model,
        messages = messages_for_getting_stops
    )
    assistant_prompt_with_stops = completion.choices[0].message.content
    assistant_message_with_stops = {"role": "assistant", "content": assistant_prompt_with_stops}
    messages_for_getting_stops.append(assistant_message_with_stops)
    stops = [string.replace("*", "").strip() for string in assistant_prompt_with_stops.split("***") if len(string.replace("*", "").strip()) > 3]
    print(f"there are {len(stops)} stops, and they are:")
    for stop in stops:
        print(stop)
    
    while len(stops) < num_stops:
        print("not enough stops! getting more...")
        user_prompt_to_get_correct_number_of_stops = f"I'm sorry, but I asked for {num_stops} popular sightseeing locations, and you only gave me {len(stops)} of them. Could you please try again?"
        user_message_to_get_correct_number_of_stops = {"role": "user", "content": user_prompt_to_get_correct_number_of_stops}
        messages_for_getting_stops.append(user_message_to_get_correct_number_of_stops)
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = messages_for_getting_stops
        )
        assistant_prompt_with_stops = completion.choices[0].message.content
        assistant_message_with_stops = {"role": "assistant", "content": assistant_prompt_with_stops}
        messages_for_getting_stops.append(assistant_message_with_stops)
        stops = [string.replace("*", "").strip() for string in assistant_prompt_with_stops.split("***") if len(string.replace("*", "").strip()) > 3]
        print(f"there are {len(stops)} stops, and they are:")
        for stop in stops:
            print(stop)
        




    ##### GET TIDBITS FOR EACH STOP

    # removed on 2023-11-22:
        # If visiting the sightseeing location typically involves eating or drinking, please also include a typical dish or dining experience.
        # the transport method, in the sentence: Lastly, please also describe a pleasant human experience involved in visiting this sightseeing location by {input['transport_method']}.


    system_prompt_for_tidbits = f"""
I am on a vacation to {input['destination_fullname']}, and am taking a sightseeing tour in and around the area. I will name a sightseeing location on the tour. Associated to this sightseeing location, please list some historical facts, literary references, or relevant quotes -- at least three or four of these.

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

END OF EXAMPLE THREE
    """
    system_message_for_tidbits = {"role": "system", "content": system_prompt_for_tidbits}

    print("\ngetting list of stops with tidbits\n")

    stops_with_tidbits = []
    stops_with_tidbits_file = open(f"stops_with_tidbits/{input['destination']}_{timestamp}.txt", "a")
    for stop in stops:
        user_message_for_tidbit = {"role": "user", "content": stop}
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = [system_message_for_tidbits, user_message_for_tidbit]
        )
        stop_with_tidbit = stop + "\n\n" + completion.choices[0].message.content
        stops_with_tidbits.append(stop_with_tidbit)
        stops_with_tidbits_file.write(stop_with_tidbit + "\n\n=====\n\n")
    stops_with_tidbits_file.close()

    print("done getting tidbits")



    ##### GET LONG AND/OR SHORT STORY

    example_story = open("example_story.txt", "r").read()

    long_story_system_prompt_template_filler = "{num_stops} different sightseeing locations there -- these will come one at a time"
    short_story_system_prompt_template_filler = "a few different sightseeing locations"

    system_prompt_for_story_template = f"""
I'm going to give you a tourist destination, a mode of transportation, a season, and REPLACE_WITH_FILLER. Please write me a story like the example far below. Please make sure to write in the PRESENT TENSE. Please don't give the tour guide a specific name, referring to them instead as 'our guide' (or similar).

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

END EXAMPLE REWRITE ONE:


START EXAMPLE REWRITE TWO:

OLD TEXT:

The National Museum of Anthropology in Mexico City offers more than just a stroll down the country's ancient past; it continues to narrate the story of Mexico's present-day indigenous groups. In-depth ethnographic exhibits open windows to the diverse and vibrant life of the many indigenous cultures still thriving in Mexico today, highlighting their languages, traditions, and everyday life.

NEW TEXT:

The main attraction in Nahua Hall is a splendid array of traditional costumes worn by Nahua communities. The costumes often consist of two-part attires - blouses known as 'huipil' and skirts known as 'enredo'. These are often adorned with detailed motifs that depict local livestock, crops, and scenery, each symbolizing a different aspect of the Nahua worldview and mythology.

The colors used in the blouses, skirts, and rebozos (a traditional garment similar to a shawl) are bold, organic, and eye-catching. You will find primary colors - reds, blues, greens, often alternating with secondary hues such as purple and orange, to tell vibrant stories of each garment's unique roots.

The huipil, typically made of cotton, is a square-cut, loose sleeveless tunic. Its vibrant surface teems with delicate embroidery and exquisite beadwork; flower motifs, birds, and symbols related to ancient Nahua gods are common elements.

END EXAMPLE REWRITE TWO:""" + "\n\n=====\n\n" + example_story

    system_prompt_for_long_story = system_prompt_for_story_template.replace("REPLACE_WITH_FILLER", long_story_system_prompt_template_filler)
    system_prompt_for_short_story = system_prompt_for_story_template.replace("REPLACE_WITH_FILLER", short_story_system_prompt_template_filler)

    long_story_user_prompt_for_setting_scene_filler = "Keep this short -- just three or four paragraphs. Please don't end your response with a summary, though, because we will be continuing the story!"
    short_story_user_prompt_for_setting_scene_filler = "Keep this part short -- just a paragraph will do."


    # {f"The tour guide is {input["tour_guide"]}. However, Please don't give the tour guide a specific name, referring to them instead as 'our guide' (or similar)." if input["tour_guide"] else ""}
    # + input['tour_guide'] + "." 
    user_prompt_for_setting_scene_template = f"Please begin by setting the scene. We are traveling in {input['destination_fullname']}; the season in {input['season']}. We are taking a sightseeing tour by {input['transport_method']}, although we may also walk around some as well. {'The tour guide is ' + input['tour_guide'] + '.' if input['tour_guide'] else ''} However, JUST set the scene; don't begin the sightseeing tour just yet. Make me excited about my trip overall, and about the upcoming tour. REPLACE_WITH_FILLER"

    user_prompt_for_setting_scene_for_long_story = user_prompt_for_setting_scene_template.replace("REPLACE_WITH_FILLER", long_story_user_prompt_for_setting_scene_filler)
    user_prompt_for_setting_scene_for_short_story = user_prompt_for_setting_scene_template.replace("REPLACE_WITH_FILLER", short_story_user_prompt_for_setting_scene_filler)

    user_prompt_for_ending_story = f"Please conclude the story about our sightseeing tour by {input['transport_method']} in {input['destination_fullname']}. Keep it upbeat, gentle, and inspiring."

    no_numbers_plz = "\n\nPlease spell out any numbers in words. For instance, write 'nineteen eighty-seven' instead of '1987', and 'four thousand seven hundred and thirty three' instead of '4,733', and 'eighteen-sixties' instead of '1860s' (referring to the decade), and 'nineties' instead of '90s' (also referring to the decade)."

    no_overused_words_plz = "\n\nPlease don't use any of the following words: tapestry, testament, grandeur, symphony, ethereal, tribute, serve, homage, tranquil."

    no_ending_summary_plz = "\n\nPlease don't end your response with a summary, though, because we will be continuing the story and visiting more sightseeing locations!"

    no_section_titles_via_only_complete_sentences_plz = "\n\nEverything you write should be in complete sentences."

    no_starting_transition_plz = """\n
Additionally, at the beginning of your response, please do NOT refer to the sightseeing location where we've just been. Do not say where we are leaving from. Rather, just refer to our travel adventures in general terms.

GOOD EXAMPLE:

Our sightseeing tour continues as we make our ways towards...

BAD EXAMPLE:

As we make our way from the castle, ..."""



    ##### GET LONG STORY

    if write_long_story:

        print("writing a long story")

        dedigitizations = []

        system_message = {"role": "system", "content": system_prompt_for_long_story}

        user_message_for_setting_scene = {"role": "user", "content": user_prompt_for_setting_scene_for_long_story}

        message_list = [system_message, user_message_for_setting_scene]

        story = ""

        print("fetching story chunk number 0 (setting the scene)")
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = message_list
        )
        assistant_prompt_with_scene_setting_undedigitized = completion.choices[0].message.content
        assistant_prompt_with_scene_setting = dedigitize_and_log(assistant_prompt_with_scene_setting_undedigitized)
        story += assistant_prompt_with_scene_setting
        assistant_message_with_scene_setting = {"role": "assistant", "content": assistant_prompt_with_scene_setting}
        message_list.append(assistant_message_with_scene_setting)

        stop_messages = []
        for (index, stop_with_tidbits) in enumerate(stops_with_tidbits):
            stop_prompt = f"Great, thank you! Here is the next sightseeing location:\n\n {stop_with_tidbits}{no_numbers_plz}{no_overused_words_plz}{no_section_titles_via_only_complete_sentences_plz}{no_ending_summary_plz}"
            if index == len(stops_with_tidbits) - 1:
                stop_prompt += no_starting_transition_plz
            stop_message = {"role": "user", "content": stop_prompt}
            stop_messages.append(stop_message)

        i = 0
        for user_message_for_stop in stop_messages:
            print("fetching story chunk number", i+1)
            print("and the user prompt is:\n\n", user_message_for_stop["content"])
            message_list.append(user_message_for_stop)
            completion = client.chat.completions.create(
                model = gpt_model,
                messages = message_list
            )
            assistant_prompt_with_story_undedigitized = completion.choices[0].message.content
            assistant_prompt_with_story = dedigitize_and_log(assistant_prompt_with_story_undedigitized)           
            story += "\n\n=====\n\n" + assistant_prompt_with_story
            assistant_message_with_story = {"role": "assistant", "content": assistant_prompt_with_story}
            message_list.append(assistant_message_with_story)
            i += 1

        print(f"fetching story chunk number {i+1} (the ending)")
        user_message_for_ending_story = {"role": "user", "content": user_prompt_for_ending_story}
        message_list.append(user_message_for_ending_story)
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = message_list
        )
        assistant_prompt_with_story_ending_undedigitized = completion.choices[0].message.content
        assistant_prompt_with_story_ending = dedigitize_and_log(assistant_prompt_with_story_ending_undedigitized)
        story += "\n\n=====\n\n" + assistant_prompt_with_story_ending


        log_replacements_and_write_files(story, "long")



    ##### GET SHORT STORY

    if write_short_story:

        a = 1 # number of stops bundled into initial chunk -- assumed to be at least 1
        c = 5 # number of middle completions
        n = 2 # number of stops per middle completion
        z = 1 # number of stops bundled into final chunk
        # total number of stops needed is a + c*n + z
        # by around 2023-11-14, we decided that these should be: a=1, c=5, n=2, z=1.
        # on 2023-11-20, we decided to actually drop n down to 1, so that we could get more fine-grained with the lengths of stories served. we'll aim for each middle chunk to only be 200-300 words, using the validate_length function defined above.
        # on 2023-11-21: yes, change back to the above: 1,5,2,1.

        print(f"writing a short story")

        dedigitizations = []

        system_message = {"role": "system", "content": system_prompt_for_short_story}

        # this evades the following stupid error, which otherwise occurs below:
            # Escape sequence (backslash) not allowed in expression portion of f-string prior to Python 3.12
        # so, here just append "\n\n" to the stop prompts now, rather than joining them with separator "\n\n" inside of the f-string.
        stops_with_tidbits = [stop_with_tidbits + "\n\n" for stop_with_tidbits in stops_with_tidbits]

        no_separator_in_intro_plz = "\n\nPlease do NOT include any sort of separator between setting the scene and taking us to the first sightseeing location."
        initial_user_prompt_for_short_story = f"{user_prompt_for_setting_scene_for_short_story}\n\nThen, here {'are' if a>1 else 'is'} the first{f' {str(a)}' if a>1 else ''} sightseeing location{'s' if a>1 else ''} to visit.\n\n{''.join(stops_with_tidbits[:a])}{no_numbers_plz + no_overused_words_plz + no_section_titles_via_only_complete_sentences_plz + no_ending_summary_plz + no_separator_in_intro_plz}"
        print("the initial user prompt is:\n", initial_user_prompt_for_short_story)
        initial_user_message = {"role": "user", "content": initial_user_prompt_for_short_story}

        message_list = [system_message, initial_user_message]

        print("fetching short story completion (not necessarily chunk!) number 0")
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = message_list
        )
        story_start_undedigitized = completion.choices[0].message.content
        story = dedigitize_and_log(story_start_undedigitized)
        initial_assistant_message = {"role": "assistant", "content": story}
        message_list.append(initial_assistant_message)

        split_with_asterisks_plz = "\n\nPlease separate the pieces of the story corresponding to the different sightseeing locations with five asterisks (i.e. the string '*****'). Please make sure to separate the sightseeing locations with five asterisks."
        for j in range(c):
            print(f"fetching short story completion (not necessarily chunk!) number", j+1)
            # on 2023-11-21 at ~5pm, removed from the following: length_plz(200, 300)
            user_prompt = f"Great, thank you! Here {'are' if n>1 else 'is'} the next {str(n) if n>1 else ''} sightseeing location{'s' if n>1 else ''}:\n\n{''.join(stops_with_tidbits[a+n*j:a+n*(j+1)])}{no_numbers_plz + no_overused_words_plz + no_section_titles_via_only_complete_sentences_plz + no_ending_summary_plz + split_with_asterisks_plz}"
            print("the next user prompt is:\n", user_prompt)
            user_message = {"role": "user", "content": user_prompt}
            message_list.append(user_message)
            completion = client.chat.completions.create(
                model = gpt_model,
                messages = message_list
            )
            assistant_prompt_with_story_undedigitized = completion.choices[0].message.content
            # 2023-11-21 at ~5pm: remove this next line, and instead just have chatGPT split the text apart into chunks as it's writing it.
            # assistant_prompt_with_story_undedigitized_with_length_validation = validate_length(assistant_prompt_with_story_undedigitized, 200, 300)
            assistant_prompt_with_story = dedigitize_and_log(assistant_prompt_with_story_undedigitized)

            print(f"writing short story, and the raw assistant_prompt_with_story (with stops hopefully separated by '*****') is:\n{assistant_prompt_with_story}")

            new_chunks = [string.replace("*", "").strip() for string in assistant_prompt_with_story.split("***") if len(string.replace("*", "").strip()) > 3]
            for index, new_chunk in enumerate(new_chunks):
                print(f"new_chunk number {index} is:\n{new_chunk}")
                story += "\n\n=====\n\n" + new_chunk
            assistant_message_with_story = {"role": "assistant", "content": assistant_prompt_with_story}
            message_list.append(assistant_message_with_story)

        no_separator_in_conclusion_plz = "\n\nPlease do NOT include any sort of separator between the last sightseeing location and the conclusion of the story."
        print(f"fetching short story completion (not necessarily chunk!) number {c+1} (the last chunk)")
        user_prompt = f"Great, thank you! Now, please conclude our story. First, here {'are' if z>1 else 'is'} the concluding {str(z) if z>1 else ''} sightseeing location{'s' if z>1 else ''} to visit.\n\n{''.join(stops_with_tidbits[a+c*n:a+c*n+z])}{no_starting_transition_plz} {no_separator_in_conclusion_plz}"
        print("the concluding user prompt is:\n", user_prompt)
        user_message = {"role": "user", "content": user_prompt}
        message_list.append(user_message)
        completion = client.chat.completions.create(
            model = gpt_model,
            messages = message_list
        )
        final_assistant_prompt_undedigitized = completion.choices[0].message.content
        final_assistant_prompt = dedigitize_and_log(final_assistant_prompt_undedigitized)
        story += "\n\n=====\n\n" + final_assistant_prompt

        log_replacements_and_write_files(story, "short")