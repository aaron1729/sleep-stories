from openai import OpenAI
client = OpenAI()

import re # regular expressions

from datetime import datetime

from os import listdir
from os.path import isfile, join

import models
import strings # so, `my_string` defined over there is accessible here as `strings.my_string`.
from inputs import * # so, the inputs defined over there are accessible here without change.

from datetime import datetime
def datetime_str_to_timestamp(str):
    return str[:10] + "_" + str[11:13] + "-" + str[14:16] + "-" + str[17:19]
start_time = str(datetime.now())
timestamp = datetime_str_to_timestamp(start_time)

################################################################################

##### text validation

# the `rewrite` function uses chatGPT to attempt to remove:
    # digits,
    # roman numerals,
    # abbreviations,
    # overused words
# from its responses. (even though we already will have requested that its responses not contain these, but it often fails at that.)
# the last is just for stylistic considerations, but the rest are to improve the likelihood that the AI voice from ElevenLabs pronounces it all correctly.

# a previous architectural choice was to search for all of the above on a first pass, but only digits on subsequent passes. but from experience, it seemed like chatGPT actually did a _pretty_ good job with all of them. so as of 2023-11-26, AMG made the decision to just check all of those one single time (by default, but max_number_of_rewritings can be changed), and then log the failure if _any_ of those trigger again, and we'll just look into it by hand.

# for abbreviations, it seems the simplest thing to do is just list out the most common ones. those are saved as



# for catching roman numerals (preceded by a space and followed by a non-word character), we previously used the regex pattern (copied from https://stackoverflow.com/a/267405/19327500):
    # pattern_for_roman_numerals = r" M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\W"
# for some reason this seemed to trigger a lot of false positives, and anyways it's rather complex. we realized that we don't need to find _valid_ roman numerals per se, so we just went with the following much simpler thing:
pattern_for_roman_numerals = r"[IVXLCDM][^a-zA-Z]"

### comments on the `rewrite` function.
# terminology: `rewrite` (a verb) refers to the function, while a `rewriting` (a noun) refers to some output of the function.
# input: a string (which for us will be an entire completion coming back from chatGPT), and a number of rewritings to attempt before moving on.
# outputs (implicitly formatted as a tuple):
    # the hopefully-fixed string
    # a boolean of whether it was modified at all
    # a list of the rewritten versions
    # a boolean of whether the final rewrite failed

def rewrite(string, max_number_of_rewritings = 3):
    any_rewritings = bool(re.search(r'\d', string)) or bool(re.search(pattern_for_roman_numerals, string))
    if not any_rewritings:
        return string, False, [], False
    rewritten_versions = [string]
    for _ in range(max_number_of_rewritings):
        system_message = {"role": "system", "content": strings.system_prompt_for_rewriting}
        user_message = {"role": "user", "content": string}
        print("asking chatGPT to rewrite text without digits")
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = [system_message, user_message]
        )
        string = completion.choices[0].message.content
        # starting here, _don't_ keep looking for roman numerals, because there _is_ the possibility that a legitimate roman numeral shows up as _not_ a roman numeral. the main thing is 'I' (first person singular), but 
        # justification: after 15 instances of this function running while writing a story, chatGPT _always_ made a passing rewrite on the first try. (these only tested removal of digits, not roman numerals, but oh well.)
        any_rewritings = bool(re.search(r'\d', string)) # or bool(re.search(pattern_for_roman_numerals, string))
        if not any_rewritings:
            return string, True, rewritten_versions, False
        rewritten_versions.append(string)
    return string, True, rewritten_versions, True

# apply the `rewrite` function, return the hopefully-correct string, and log if applicable.
def rewrite_and_log(string, rewritings):
    output, modified, rewritten_versions, failed = rewrite(string)
    if modified:
        rewritings.append({"original": rewritten_versions[0], "failed_rewrites": rewritten_versions[1: ], "final": output, "failed": failed})
    return output, rewritings

################################################################################

##### record the replacements and write files

# now that the story is finished, if any digit replacements were made, then:
    # write them to a replacement_log file;
    # store just the individual sentences at the end of the story file (for compilation into kotlin code -- perhaps at the top, commented-out);
    # regardless, also save the replacement stats.

def log_replacements_and_write_files(input, story, length, rewritings, timestamp, stops_filename):
        
    ### record replacement stats.

    nums_of_attempts = []
    any_failures = False
    # the rewritings list will have been created through the process of writing the story.
    for rewriting in rewritings:
        nums_of_attempts.append(len(rewriting['failed_rewrites']) + 1)
        if rewriting['failed']:
            any_failures = True
    replacement_stats_string = f"{input['destination']}_{timestamp}_{length}.txt\nattempts per rewriting: " + ", ".join([str(num) for num in nums_of_attempts]) + f"\nany failures: {str(any_failures)}\n\n"
    replacement_stats_file = open("logs/replacement_stats.txt", "a")
    replacement_stats_file.write(replacement_stats_string)
    replacement_stats_file.close()

    ### if there are any failures, make a replacement_failure_log file.

    if any_failures:
        replacement_failure_log_file = open(f"logs/replacement_failure_logs/replacement-failure-log_{input['destination']}_{timestamp}_{length}.txt", "w")
        replacement_failure_log_file.write("FAILED! SAD!")
        replacement_failure_log_file.close()

    ### if there were any replacements, save each pair -- the old and new sentences -- together in a single object. (these get used just below.)
    ### the full replacements -- the old and new chunks -- get written to a replacement_log file.

    sentence_replacement_pairs = []

    if len(rewritings) > 0:
        replacement_log = "\n==========\n\n"
        for rewriting in rewritings:

            # write some replacement_log material.

            replacement_log += f"REPLACEMENT FAILED: {str(rewriting['failed'])} \n\n=====\n\n"
            if rewriting["failed"]:
                replacement_log = "WARNING: A REPLACEMENT HEREIN HATH FAILED\n\n" + replacement_log
            replacement_log += f"ORIGINAL TEXT:\n\n{rewriting['original']}\n\n=====\n\n"
            replacement_log += "\n\n=====\n\n".join(["FAILED REWRITES:"] + rewriting['failed_rewrites'] + [""])
            replacement_log += f"FINAL VERSION:\n\n{rewriting['final']}\n\n==========\n\n"

            # store replaced sentences and their replacements.

            original_sentences = rewriting['original'].split(".")
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
        
        # write the replacement_log file (assuming there were any rewritings).

        replacement_log_file = open(f"logs/replacement_logs/replacement-logs_{input['destination']}_{timestamp}_{length}.txt", "w")
        replacement_log_file.write(replacement_log)
        replacement_log_file.close()
    
    ### save the replacement metadata as a string.

    replacements_string = "REPLACED_SENTENCES:"
    for sentence_replacement_object in sentence_replacement_pairs:
        replacements_string += f"\n\nOLD SENTENCE: {sentence_replacement_object['old']}\nNEW SENTENCE: {sentence_replacement_object['new']}"

    ### save the stops file as a string.
    stops_filename_string = f"this story was written based on the stops file: {stops_filename}"
    
    ### append the metadata to the story string
    
    metadata = stops_filename + replacements_string

    story += f"\n\n=====\n\n{stops_filename_string}\n\n{replacements_string}"

    ### write the story file.

    story_file = open(f"stories/story_{input['destination']}_{timestamp}_{length}.txt", "w")
    story_file.write(story)
    story_file.close()

    story_end_time = datetime_str_to_timestamp(str(datetime.now()))
    print(f"finished writing {length} story set in {input['destination_fullname']} with timestamp {timestamp} at", story_end_time)

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

