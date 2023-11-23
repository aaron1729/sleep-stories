from openai import OpenAI
client = OpenAI()

import re # regular expressions

import models
import strings # so, `my_string` defined over there is accessible here as `strings.my_string`.
from inputs import * # so, the inputs defined over there are accessible here without change.

from datetime import datetime
def datetime_str_to_timestamp(str):
    return str[:10] + "_" + str[11:13] + "-" + str[14:16] + "-" + str[17:19]

start_time = str(datetime.now())
timestamp = datetime_str_to_timestamp(start_time)



##### PARAMETERS

num_stops = 3

write_long_story = True
write_short_story = False

################################################################################

##### dedigitization
##### ##### UPDATE: throughout this code, "digit" also refers to roman numerals.

##### ##### ##### ##### UPDATE 2023-11-22: call this "text validation", and re-check here for the SAT words ("tapestry, etc.").
















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
        system_message = {"role": "system", "content": strings.system_prompt_for_dedigitization}
        user_message = {"role": "user", "content": string}
        print("asking chatGPT to rewrite text without digits")
        completion = client.chat.completions.create(
            model = models.gpt_model,
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
#             model = models.gpt_model,
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

    user_message_for_stops = {"role": "user", "content": strings.user_prompt_for_stops(input['destination'], num_stops, input['transport_method'], input['requested_sightseeing_stops'])}
    messages_for_getting_stops = [user_message_for_stops]

    print(f"getting list of {num_stops} stops\n")
    completion = client.chat.completions.create(
        model = models.gpt_model,
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
            model = models.gpt_model,
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

    system_message_for_tidbits = {"role": "system", "content": strings.system_prompt_for_tidbits(input['destination_fullname'])}

    print("\ngetting list of stops with tidbits\n")

    stops_with_tidbits = []
    stops_with_tidbits_file = open(f"stops_with_tidbits/{input['destination']}_{timestamp}.txt", "a")
    for stop in stops:
        user_message_for_tidbit = {"role": "user", "content": stop}
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = [system_message_for_tidbits, user_message_for_tidbit]
        )
        stop_with_tidbit = stop + "\n\n" + completion.choices[0].message.content
        stops_with_tidbits.append(stop_with_tidbit)
        stops_with_tidbits_file.write(stop_with_tidbit + "\n\n=====\n\n")
    stops_with_tidbits_file.close()

    print("done getting tidbits")

    ##### GET LONG STORY

    if write_long_story:

        print("writing a long story")

        dedigitizations = []

        system_message = {"role": "system", "content": strings.system_prompt_for_story("long", num_stops)}

        user_message_for_setting_scene = {"role": "user", "content": strings.user_prompt_for_setting_scene("long", input['destination_fullname'], input['transport_method'], input['tour_guide'], input['season'])}

        message_list = [system_message, user_message_for_setting_scene]

        story = ""

        print("fetching story chunk number 0 (setting the scene)")
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = message_list
        )
        assistant_prompt_with_scene_setting_undedigitized = completion.choices[0].message.content
        assistant_prompt_with_scene_setting = dedigitize_and_log(assistant_prompt_with_scene_setting_undedigitized)
        story += assistant_prompt_with_scene_setting
        assistant_message_with_scene_setting = {"role": "assistant", "content": assistant_prompt_with_scene_setting}
        message_list.append(assistant_message_with_scene_setting)

        stop_messages = []
        for (index, stop_with_tidbits) in enumerate(stops_with_tidbits):
            stop_prompt = f"Great, thank you! Here is the next sightseeing location:\n\n {stop_with_tidbits}{strings.no_numbers_plz}{strings.no_overused_words_plz}{strings.no_section_titles_via_only_complete_sentences_plz}{strings.no_ending_summary_plz}"
            if index == len(stops_with_tidbits) - 1:
                stop_prompt += strings.no_starting_transition_plz
            stop_message = {"role": "user", "content": stop_prompt}
            stop_messages.append(stop_message)

        i = 0
        for user_message_for_stop in stop_messages:
            print("fetching story chunk number", i+1)
            print("and the user prompt is:\n\n", user_message_for_stop["content"])
            message_list.append(user_message_for_stop)
            completion = client.chat.completions.create(
                model = models.gpt_model,
                messages = message_list
            )
            assistant_prompt_with_story_undedigitized = completion.choices[0].message.content
            assistant_prompt_with_story = dedigitize_and_log(assistant_prompt_with_story_undedigitized)           
            story += "\n\n=====\n\n" + assistant_prompt_with_story
            assistant_message_with_story = {"role": "assistant", "content": assistant_prompt_with_story}
            message_list.append(assistant_message_with_story)
            i += 1

        print(f"fetching story chunk number {i+1} (the ending)")
        user_message_for_ending_story = {"role": "user", "content": strings.user_prompt_for_ending_long_story(input['destination_fullname'], input['transport_method'])}
        message_list.append(user_message_for_ending_story)
        completion = client.chat.completions.create(
            model = models.gpt_model,
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

        system_message = {"role": "system", "content": strings.system_prompt_for_story("short", num_stops)}

        # this evades the following stupid error, which otherwise occurs below:
            # Escape sequence (backslash) not allowed in expression portion of f-string prior to Python 3.12
        # so, here just append "\n\n" to the stop prompts now, rather than joining them with separator "\n\n" inside of the f-string.
        stops_with_tidbits = [stop_with_tidbits + "\n\n" for stop_with_tidbits in stops_with_tidbits]

        initial_user_prompt_for_short_story = f"""{strings.user_prompt_for_setting_scene(
            "short",
            input['destination_fullname'],
            input['transport_method'],
            input['tour_guide'],
            input['season']
            )}\n\nThen, here {'are' if a>1 else 'is'} the first {str(a) if a>1 else ''} sightseeing location{'s' if a>1 else ''} to visit.\n\n{''.join(stops_with_tidbits[:a])}"""#{strings.no_numbers_plz + strings.no_overused_words_plz + strings.no_section_titles_via_only_complete_sentences_plz + strings.no_ending_summary_plz + strings.no_separator_in_intro_plz}"
        initial_user_message = {"role": "user", "content": initial_user_prompt_for_short_story}

        message_list = [system_message, initial_user_message]

        print("fetching short story completion (not necessarily chunk!) number 0")
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = message_list
        )
        story_start_undedigitized = completion.choices[0].message.content
        story = dedigitize_and_log(story_start_undedigitized)
        initial_assistant_message = {"role": "assistant", "content": story}
        message_list.append(initial_assistant_message)

        for j in range(c):
            print(f"fetching short story completion (not necessarily chunk!) number", j+1)
            # on 2023-11-21 at ~5pm, removed from the following: length_plz(200, 300)
            user_prompt = f"Great, thank you! Here {'are' if n>1 else 'is'} the next {str(n) if n>1 else ''} sightseeing location{'s' if n>1 else ''}:\n\n{''.join(stops_with_tidbits[a+n*j:a+n*(j+1)])}{strings.no_numbers_plz + strings.no_overused_words_plz + strings.no_section_titles_via_only_complete_sentences_plz + strings.no_ending_summary_plz + strings.split_with_asterisks_plz}"
            print("the next user prompt is:\n", user_prompt)
            user_message = {"role": "user", "content": user_prompt}
            message_list.append(user_message)
            completion = client.chat.completions.create(
                model = models.gpt_model,
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

        print(f"fetching short story completion (not necessarily chunk!) number {c+1} (the last chunk)")
        user_prompt = strings.user_prompt_for_ending_short_story(input['destination_fullname'], input['transport_method'], stops_with_tidbits[a+c*n:a+c*n+z], z)
        # user_prompt = f"Great, thank you! Now, please conclude our story. First, here {'are' if z>1 else 'is'} the concluding {str(z) if z>1 else ''} sightseeing location{'s' if z>1 else ''} to visit.\n\n{''.join(stops_with_tidbits[a+c*n:a+c*n+z])}{strings.no_starting_transition_plz} {strings.no_separator_in_conclusion_plz}"
        print("the concluding user prompt is:\n", user_prompt)
        user_message = {"role": "user", "content": user_prompt}
        message_list.append(user_message)
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = message_list
        )
        final_assistant_prompt_undedigitized = completion.choices[0].message.content
        final_assistant_prompt = dedigitize_and_log(final_assistant_prompt_undedigitized)
        story += "\n\n=====\n\n" + final_assistant_prompt

        log_replacements_and_write_files(story, "short")