from openai import OpenAI
client = OpenAI()

import re

import hashlib

import models
import strings

timestamp = strings.time_now()

################################################################################

# a typical input for unedited_story_filename is "unedited_story_berkeley_2023-11-24_17-25-36_short.txt".
    # if unedited_story_filename is left as `None`, then we edit _all_ the unedited stories in `stories-unedited/`.
# max_number_of_attempts dictates how many times we run each chunk through our regex patterns to see if it catches. (at the end of the function, we run one more time and record whether we ultimately succeeded.)
# B (for "base") is one more than the maximum number of instances of an overused word that we allow. (so if B = 2 then we only allow 0 or 1 instances of each.)
def edit_story(unedited_story_filename = None, max_number_of_attempts = 3, B = 3):
    
    if not unedited_story_filename:
        unedited_story_filenames = strings.get_all_unhidden_files("stories-unedited")
        unedited_story_filenames.sort()
    else:
        unedited_story_filenames = [unedited_story_filename]
    
    for unedited_story_filename in unedited_story_filenames:

        print(f"\nstarting to edit the story {unedited_story_filename} at {strings.time_now()}\n")
        
        # make a local copy of the dictionary `strings.overused_words`, and add counters based on a base-B hash of unedited_story_filename. specifically, go from right to left in there (since these always start as nonzero on the left), assigning the bits to the overused words in the order that they appear in this list. (this is better than assigning these values randomly, since it's replicable.)
        overused_words = strings.overused_words
        # convert the string to bytes.
        filename_encoded = unedited_story_filename.encode()
        # compute the SHA-256 hash.
        sha_256_hash = hashlib.sha256(filename_encoded)
        # put this in hexadecimal format.
        hex_hash = sha_256_hash.hexdigest()
        # this function converts a nonnegative integer to a _string_ in base B (so there can be 0, 1, ..., B-1 appearances of each overused word).
        def convert_int_to_base_b(num, base):
            if num < base:
                return str(num)
            else:
                return convert_int_to_base_b(num // base, base) + str(num % base)
        base_B_hash_string = convert_int_to_base_b(int(hex_hash, 16), B)
        print(f"\nbase_B_hash_string is:\n{base_B_hash_string}\n")
        # assign the counters, and record them (before they change!) into a string for metadata.
        overused_word_allowances_string_list = []
        for (index, entry) in enumerate(overused_words):
            backwards_index = -(index + 1)
            overused_words[entry]["counter"] = int(base_B_hash_string[backwards_index])
            overused_word_allowances_string_list.append(f"{overused_words[entry]['word']}: {str(overused_words[entry]['counter'])}")
        # this appears both in the metadata of the story as well as in the rewriting-log.
        overused_word_allowances_string = f"OVERUSED WORD ALLOWANCES (computed with B={B}):\n{strings.n.join(overused_word_allowances_string_list)}"
        print(f"\noverused_word_allowances_string is:\n{overused_word_allowances_string}")
        
        # make some regex patterns.
        # recall that in regex, parentheses are used to create a capture group (which is e.g. what's returned by `re.findall`). but it's _also_ used to simply group alternatives, as in `(a|b)`. if used in this way, it automatically also functions as a capture grouping. to disentangle those, use `(?: ... )` to group alternatives _without_ forming them into a capture group.
        # it seems like roman numerals are essentially always just referring to people (e.g. Henry IV), so let's just catch 1-30. (actually things are regularish up until 39, but then 40 is XL.) we begin with a space, and end with anything that's _not_ a letter.
        pattern_for_low_roman_numerals = r" (X{0,2}(?:I?X|IV|VI{0,3}|I{1,3}))[^A-Za-z]"
        # this catches numbers, including those with comma separations.
        pattern_for_numbers = r"(\d+(?:,?\d+)*)"

        # now, edit the unedited story, chunk by chunk.

        unedited_story_chunks = open(f"stories-unedited/{unedited_story_filename}", "r").read().split(strings.separator)
        story_metadata = unedited_story_chunks.pop()
        story_metadata += f"\n\nthis story was edited at: {timestamp}\n\n{overused_word_allowances_string}"
        
        chunks_editing_data = []
        # each entry of the chunks_editing_data will be an instance of chunk_editing_data, which is itself a list of "version objects" that corresponds to the iterative edits of a given chunk. in turn, a "version object" has:
            # text: a string
            # any_numbers: bool
            # numbers_appearing: list of strings (e.g. one could be "1,005")
            # any_roman_numerals: bool
            # roman_numerals_appearing: list of strings (e.g. one could be "XIV")
            # overused_words_data: an object of objects, e.g.
                # tapestry:
                    # num_allowed: int (coming from the counter)
                    # num_appearing: int (coming from the regex count)
                    # try_to_remove: bool, namely: num_allowed-num_appearing < 0
                #... and we update the counter at "tapestry" if num_allowed - num_appearing >= 0
            # overused_words_to_try_to_remove: a list of strings (e.g. one could be "tapestry")
            # any_overused_words_to_try_to_remove: bool, namely: the `any` of the above `try_to_remove` bools
            # any_triggers: a bool, namely: the `any` the above three "any" bools
        # given a "version object", assuming we haven't run through max_number_of_attempts already, if any_triggers is True then we ask for a rewrite.
            # in that rewrite, we _always_ say "no numbers -- and say years correctly!" and also "no roman numerals -- and use 'the' if it's a person!".
            # as for overused words, we _only_ list the ones where try_to_remove is True. however, we _always_ say: "don't replace it with any words in the list: [all overused words]."

        for unedited_story_chunk in unedited_story_chunks:

            # initialize the chunk_editing_data, a list of version objects, which will be appended to chunks_editing_data later.
            chunk_editing_data = []

            # initialize chunk_to_check as the original version of the chunk (but this will change later).
            chunk_to_check = unedited_story_chunk

            # initialize overused_words_to_check as the original list of overused words (but this will hopefully be whittled down as words are successfully removed).
            overused_words_to_check = overused_words.keys()

            # the following `for` loop has two parts:
                # always, construct a `version_object` and append it to `chunk_editing_data`.
                # assuming we're not on the last pass, if there are any triggers, ask chatGPT for a rewrite.
            # this organization is just so that the code for creating the version_object is recycled. that is, anytime we ask chatGPT for a rewrite, we will assuredly be returning to the top of the `for` loop, and so we will construct an associated `version_object`.

            for index in range(max_number_of_attempts + 1):

                # initialize a new version-object, and then slowly fill in its properties.

                version_object = {
                    "text": chunk_to_check,
                    # the following property will be populated in a `for` loop below. it will be an object, whose keys are overused words and whose values are objects.
                    "overused_words_data": {},
                }

                numbers_appearing = re.findall(pattern_for_numbers, chunk_to_check)
                version_object["numbers_appearing"] = numbers_appearing
                version_object["any_numbers"] = bool(numbers_appearing)
                
                roman_numerals_appearing = re.findall(pattern_for_low_roman_numerals, chunk_to_check)
                version_object["roman_numerals_appearing"] = roman_numerals_appearing
                version_object["any_roman_numerals"] = bool(roman_numerals_appearing)
                
                for entry in overused_words_to_check:
                    num_allowed = overused_words[entry]["counter"]
                    num_appearances = len(re.findall(overused_words[entry]["pattern"], chunk_to_check))
                    # for simplicity, we will try to remove _all_ instances of the word in this chunk if they overshoot the counter (and in that case we'll leave the counter fixed).
                    try_to_remove = (num_allowed - num_appearances < 0)
                    overused_word_object = {
                        "num_allowed": num_allowed,
                        "num_appearances": num_appearances,
                        "try_to_remove": try_to_remove
                    }
                    version_object["overused_words_data"][entry] = overused_word_object
                    # decrement the counter, but only on the initial pass.
                    if (not try_to_remove) and (index == 0):
                        overused_words[entry]["counter"] -= num_appearances
                
                overused_words_to_try_to_remove = [overused_word for overused_word in version_object["overused_words_data"] if version_object["overused_words_data"][overused_word]["try_to_remove"]]
                version_object["overused_words_to_try_to_remove"] = overused_words_to_try_to_remove
                version_object["any_overused_words_to_try_to_remove"] = (len(overused_words_to_try_to_remove) > 0)                

                # now, modify the list overused_words_to_check so that on a future pass we only "check our work".
                overused_words_to_check = version_object["overused_words_to_try_to_remove"]
                
                any_triggers = any([version_object["any_numbers"], version_object["any_roman_numerals"], version_object["any_overused_words_to_try_to_remove"]])
                version_object["any_triggers"] = any_triggers

                # append the version object to chunk_editing_data.
                chunk_editing_data.append(version_object)

                if any_triggers:
                    if index < max_number_of_attempts:
                        
                        # ask chatGPT for a rewrite.
                        print(f"""asking chatGPT for a rewrite, and `version_object` has:
numbers_appearing: {version_object['numbers_appearing']}
roman_numerals_appearing: {version_object['roman_numerals_appearing']}
overused_words_to_try_to_remove: {version_object['overused_words_to_try_to_remove']}""")
                        
                        system_prompt_for_rewriting = strings.system_prompt_for_rewriting(version_object["overused_words_to_try_to_remove"])
                        system_message_for_rewriting = {"role": "system", "content": system_prompt_for_rewriting}
                        # print(f"\nsystem_prompt_for_rewriting is:\n\n{system_prompt_for_rewriting}\n")

                        user_prompt_for_rewriting = version_object["text"]
                        user_message_for_rewriting = {"role": "user", "content": user_prompt_for_rewriting}
                        print(f"\nasking chatGPT to rewrite the chunk:\n\n{user_prompt_for_rewriting}\n")

                        completion = client.chat.completions.create(
                            model = models.gpt_model,
                            messages = [system_message_for_rewriting, user_message_for_rewriting]
                        )
                        chunk_to_check = strings.swap_quote_marks(completion.choices[0].message.content)
                        print(f"after the rewrite, the chunk is:\n\n{chunk_to_check}")
                        
                    else:
                        print("any_triggers is True and index = max_number_of_attempts, which means we have FAILED! do some failure logging here.")
                else:
                    print("\nhooray, any_triggers is false! (so, no longer editing this chunk.)\n")
                    break
            
            # here, we've finished with `for` loop (creating version objects and requesting rewrites) associated to a given chunk.
            chunks_editing_data.append(chunk_editing_data)
        
        # here, we've finished with attempted rewrites of _all_ chunks.

        # first and foremost, save the edited version of the story (and its metadata)!
        edited_story_chunks = [chunk_editing_data[-1]["text"] for chunk_editing_data in chunks_editing_data]
        edited_story_chunks.append(story_metadata)
        edited_story_string = strings.separator.join(edited_story_chunks)
        edited_story_filename = "story_" + "_".join(unedited_story_filename.split("_")[1:])
        edited_story_file = strings.open_safe("stories", edited_story_filename, "w")
        edited_story_file.write(edited_story_string)
        edited_story_file.close()
        print(f"\nfinished editing {unedited_story_filename}, and wrote {edited_story_filename} at {strings.time_now()}")

        # now, do some logging...

        ## first, do the relevant computations (since these will be shared between various logs).

        ### record how many rewrites each chunk underwent.

        num_rewrites_of_chunks_as_strings = [str(len(chunk_editing_data) - 1) for chunk_editing_data in chunks_editing_data]

        ### record whether each chunk was _successfully_ edited.

        def chunk_editing_data_to_success(chunk_editing_data):
            if len(chunk_editing_data) < max_number_of_attempts:
                return True
            elif not chunk_editing_data[-1]["any_triggers"]:
                return True
            else:
                return False
        successes_of_rewriting_chunks = [chunk_editing_data_to_success(chunk_editing_data) for chunk_editing_data in chunks_editing_data]

        ### record the indices of chunks that failed to be rewritten.

        indices_of_rewriting_failures_as_strings = [str(index) for (index, bool) in enumerate(successes_of_rewriting_chunks) if not bool]

        ### record whether all chunks were rewritten successfully.

        all_rewriting_successes = all(successes_of_rewriting_chunks)

        # write a (rather verbose) log file.

        def chunk_editing_data_to_rewriting_log_file_string(chunk_editing_data):
            
            if len(chunk_editing_data) == 1:
                return ""
            
            rewriting_success = not chunk_editing_data[-1]["any_triggers"]

            def version_object_to_log_file_string(version_object):
                version_output = f"any triggers for rewrite: {version_object['any_triggers']}"
                if version_object['any_triggers']:
                    version_output += f"""
numbers_appearing: {', '.join(version_object['numbers_appearing'])}
roman_numerals_appearing: {', '.join(version_object['roman_numerals_appearing'])}
overused_words_data:"""
                    for (overused_word, overused_word_object) in version_object["overused_words_data"].items():
                        version_output += f"""
    {overused_word}
        num_allowed: {overused_word_object["num_allowed"]}
        num_appearances: {overused_word_object["num_appearances"]}
        try_to_remove: {overused_word_object["try_to_remove"]}"""
                version_output += f"\n\n{version_object['text']}"
                return version_output
            
            chunk_output = f"""REWRITING SUCCESS: {rewriting_success}

ORIGINAL VERSION:

{version_object_to_log_file_string(chunk_editing_data[0])}

{strings.separator}

INTERMEDIATE VERSION(S):

{strings.separator_alt.join([version_object_to_log_file_string(intermediate_version_object) for intermediate_version_object in chunk_editing_data[1: -1]])}

{strings.separator}

FINAL VERSION:

{version_object_to_log_file_string(chunk_editing_data[-1])}"""
            
            return chunk_output
        
        log_file_metadata_string = f"""this rewriting log contains a record of all rewrites from:
unedited story: {unedited_story_filename}
editing timestamp: {timestamp}

the chunks were respectively rewritten the following numbers of times: {', '.join(num_rewrites_of_chunks_as_strings)}
(note: chunks that were untouched are not written out below.)

INDICES OF REWRITING FAILURES: {', '.join(indices_of_rewriting_failures_as_strings) if len(indices_of_rewriting_failures_as_strings) > 0 else '[none]'}

{overused_word_allowances_string}"""

        strings_to_join_for_rewriting_log_file_string = [log_file_metadata_string]

        for (index, chunk_editing_data) in enumerate(chunks_editing_data):
            if len(chunk_editing_data) > 1:
                strings_to_join_for_rewriting_log_file_string.append(f"INDEX OF CHUNK: {index}\n\n" + chunk_editing_data_to_rewriting_log_file_string(chunk_editing_data))
        
        rewriting_log_file_string = strings.separator_long.join(strings_to_join_for_rewriting_log_file_string)
        
        rewriting_log_filename = f"rewriting-log-{unedited_story_filename[:-4]}_edited-at_{timestamp}.txt"
        rewriting_log_file = strings.open_safe("logs/rewriting-logs", rewriting_log_filename, "w")
        rewriting_log_file.write(rewriting_log_file_string)
        rewriting_log_file.close()

        # append an entry to `logs/rewriting-stats.txt`.

        rewriting_stats_string = f"""

{unedited_story_filename}
editing timestamp: {timestamp}
number of rewrites per chunk: {', '.join(num_rewrites_of_chunks_as_strings)}
rewriting success: {str(all_rewriting_successes)}"""
        if not all_rewriting_successes:
            rewriting_stats_string += f"""
indices of failed chunks: {', '.join(indices_of_rewriting_failures_as_strings)}
for more information, check the verbose log file: {rewriting_log_filename}"""
        rewriting_stats_file = strings.open_safe("logs", "rewriting-stats.txt", "a")
        rewriting_stats_file.write(rewriting_stats_string)
        rewriting_stats_file.close()

        # if there were any rewriting failures, write a special failure log file.

        if not all_rewriting_successes:
            rewriting_failure_log_string = f"""a rewrite failed when editing: {unedited_story_filename}

editing timestamp: {timestamp}

for more information, check the verbose rewriting-log file: logs/rewriting-logs/{rewriting_log_filename}"""
            rewriting_failure_log_filename = f"rewriting-failure-log-{unedited_story_filename[:-4]}_edited-at_{timestamp}.txt"
            
            rewriting_failure_file = strings.open_safe("logs/rewriting-failure-logs", rewriting_failure_log_filename, "w")
            rewriting_failure_file.write(rewriting_failure_log_string)
            rewriting_failure_file.close()

    return None



### let's edit some stories!

# edit_story(...)