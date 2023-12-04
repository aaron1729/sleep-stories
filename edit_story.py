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

        print(f"\nstart editing the story {unedited_story_filename} at {strings.time_now()}\n")
        
        # make a local copy of the list `strings.overused_words`, and add counters based on a base-B hash of unedited_story_filename. specifically, go from right to left in there (since these always start as nonzero on the left), assigning the bits to the overused words in the order that they appear in this list. (this is better than assigning these values randomly, since it's replicable.)
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
            entry["counter"] = int(base_B_hash_string[backwards_index])
            overused_word_allowances_string_list.append(f"{entry['word']}: {str(entry['counter'])}")
        overused_word_allowances_string = f"OVERUSED WORD ALLOWANCES (computed with B={B}):\n{strings.n.join(overused_word_allowances_string_list)}"
        print(f"\noverused_word_allowances_string is:\n{overused_word_allowances_string}")
        
        
        # make some regex patterns.
        # it seems like roman numerals are essentially always just referring to people (e.g. Henry IV), so let's just catch 1-30. (actually things are regularish up until 39, but then 40 is XL.) we begin with a space, and end with anything that's _not_ a letter.
        pattern_for_low_roman_numerals = r" X{0,2}(I?X|IV|V?I{0,3})[^a-zA-Z]"
        # this catches numbers, including those with comma separations.
        pattern_for_numbers = r"\d+(,?\d+)*"

        # now, edit the unedited story, chunk by chunk.

        unedited_story_chunks = open(f"stories-unedited/{unedited_story_filename}", "r").read().split(strings.separator)
        story_metadata = unedited_story_chunks.pop()
        story_metadata += f"\n\nthis story was edited at: {timestamp}\n\n{overused_word_allowances_string}"
        
        chunks_editing_data = []
        # each entry of the chunks_editing_data will be an instance of chunk_editing_data, which is itself a list (corresponding to a chunk) . specifically, each entry is a list of "version objects". a "version object" has:
            # text: a string
            # triggers: an object:
                # any_numbers: bool
                # any_roman_numerals: bool
                # overused_words: an object of objects, e.g.
                    # tapestry:
                        # num_allowed: int (coming from the counter)
                        # num_appearing: int (coming from the regex count)
                        # try_to_remove: bool, namely: num_allowed-num_appearing < 0
                    #... and we update the counter at "tapestry" if num_allowed - num_appearing >= 0
                # any_overused_words_to_remove: bool, the `any` of all the above
                # any_triggers: a boolean, reducing the above three
        # given a "version object", assuming we haven't run through max_number_of_attempts already, if any_triggers is True then we ask for a rewrite.
            # in that rewrite, we _always_ say "no numbers -- and say years correctly!" and "no roman numerals -- and use 'the' if it's a person!".
            # as for overused words, we _only_ list the ones where try_to_remove is True. however, we _always_ say: "don't replace it with any words in the list: [all overused words]."
        
        for unedited_story_chunk in unedited_story_chunks:

            # initialize chunk_to_check to the original version of the chunk.
            chunk_to_check = unedited_story_chunk
            chunk_editing_data = []

            for index in range(max_number_of_attempts + 1):

                # create a new version-object.
                version_object = {
                    "text": chunk_to_check,
                    "any_numbers": bool(re.search(pattern_for_numbers, chunk_to_check)),
                    "any_roman_numerals": bool(re.search(pattern_for_low_roman_numerals, chunk_to_check)),
                    "overused_words_data": {},
                }
                for entry in overused_words:
                    num_allowed = overused_words[entry]["counter"]
                    num_appearances = len(re.findall(entry['pattern'], chunk_to_check))
                    try_to_remove = (num_allowed - num_appearances < 0)
                    overused_word_object = {
                        "num_allowed": num_allowed,
                        "num_appearances": num_appearances,
                        "try_to_remove": try_to_remove
                    }
                    version_object["overused_words_data"][entry["word"]] = overused_word_object
                    # only decrement the counter on the initial pass.
                    if (num_allowed - num_appearances >= 0) and (index == 0):
                        overused_words[entry]["counter"] -= num_appearances












        
        
        
        
        versions_of_story_chunks = []
        triggers_for_rewriting_chunks = []
        failure_rewriting_chunks = []
        for chunk in unedited_story_chunks:
            versions_of_story_chunk = [chunk]
            # initialize a list of triggers for rewriting the chunk (but it'll stay empty if there are no rewrites).
            triggers_for_rewriting_chunk = []
            # the last iteration of the following `for` loop is just to check if there are any hits; we don't ask for a rewrite that time.
            for index in range(max_number_of_attempts + 1):

                # check if there are any hits.
                    # always try to remove numbers.
                    # always try to remove roman numerals.
                    # for each overused word, try to remove it _unless_ we're going to let this one instance [or "these instances", if we ever change this tolerance to be >1] slide (and decrement the counter).
                match_for_numbers = re.search(pattern_for_numbers, chunk)
                any_numbers = bool(match_for_numbers)
                match_for_roman_numerals = re.search(pattern_for_low_roman_numerals, chunk)
                any_roman_numerals = bool(match_for_roman_numerals)
                overused_words_to_avoid = [] # entries are overused_words; these are when the counter is down to 0.
                overused_words_to_allow = [] # entries are overused_words; these are when the counter hasn't run down yet.
                overused_word_appearances = [] # entries are tuples of (0) an overused_word, (1) a count, and (2) a counter, but only if this appearance triggers a rewrite (i.e. the count is positive and greater than the counter).
                any_overused_words_used_overmuch = False
                for entry in overused_words:
                    num_appearances = len(re.findall(entry['pattern'], chunk))
                    if num_appearances == 0:
                        overused_words_to_avoid.append(entry['word'])
                    else:
                        # entry['counter'] can be any of: 0, 1, ..., B-1.
                        if num_appearances <= entry['counter']:
                            entry['counter'] -= num_appearances
                        else:
                            overused_words_to_avoid.append(entry['word'])
                            overused_word_appearances.append((entry['word'], num_appearances, entry['counter']))
                            any_overused_words_used_overmuch = True
                any_hits = any_numbers or any_roman_numerals or any_overused_words_used_overmuch

                # if we're on the last pass, record whether we're still getting any hits (i.e. whether we've failed to rewrite the chunk).
                


                ### NO, this should _always_ append something! including if we succeed earlier too.
                





                if index == max_number_of_attempts:
                    failure_rewriting_chunks.append(any_hits)

                # if we're on the initial pass, record the trigger(s) for the rewrite, if any.
                if index == 0 and any_hits:
                    if any_numbers:
                        triggers_for_rewriting_chunk.append("numbers")
                    # if any_roman_numerals:
                        # triggers_for_rewriting_chunk.append("roman numerals")
                    if any_overused_words_used_overmuch > 0:
                        triggers_for_rewriting_chunk += [str(overused_word_and_count_and_counter_tuple) for overused_word_and_count_and_counter_tuple in overused_word_appearances]

                # if there are any hits and we're not on the last pass:
                    # record the triggers if we're on the initial pass,
                    # ask for a rewrite,
                    # save this as `chunk`, and
                    # append it to `versions_of_story_chunk`.
                # and then, in any case, go back to the top of the `for` loop.
                if any_hits and index < max_number_of_attempts:
                    
                    # on 11/29 at 8pm, removed: \nany_roman_numerals = {any_roman_numerals}
                    print(f"\nasking chatGPT for a rewrite, with:\nany_numbers = {any_numbers}\noverused_words_to_avoid = {overused_words_to_avoid}\noverused_word_appearances = {overused_word_appearances}")
                    print(f"\nbefore the rewrite, the chunk is:\n\n{chunk}")
                    
                    system_message = {"role": "system", "content": strings.system_prompt_for_rewriting(overused_words_to_avoid)}
                    user_message = {"role": "user", "content": chunk}
                    completion = client.chat.completions.create(
                        model = models.gpt_model,
                        messages = [system_message, user_message]
                    )
                    chunk = completion.choices[0].message.content
                    chunk = strings.swap_quote_marks(chunk)
                    print(f"\nafter the rewrite, the chunk is:\n\n{chunk}\n")
                    versions_of_story_chunk.append(chunk)
            
            # after the inner `for` loop (running through the rewrite attempts) but still referring to a fixed chunk:
                # save the `versions_of_story_chunk` list to the `versions_of_story_chunks` list;
                # save the `triggers_for_rewriting_chunk` list to the `triggers_for_rewriting_chunks` list.
            versions_of_story_chunks.append(versions_of_story_chunk)
            triggers_for_rewriting_chunks.append(triggers_for_rewriting_chunk)
            
            # then, continue on to the next chunk.

        # first and foremost, write the edited version of the story!

        # grab the final version of each chunk, and add the metadata too.
        edited_story_chunks = [versions_of_story_chunk[-1] for versions_of_story_chunk in versions_of_story_chunks] + [story_metadata]
        # record the edited story, including its metadata.
        edited_story_string = strings.separator.join(edited_story_chunks)
        # write the story to a file.
        # for the filename, turn "story-unedited" into just "story".
        edited_story_filename = "story_" + "_".join(unedited_story_filename.split("_")[1:])
        edited_story_file = open(f"stories/{edited_story_filename}", "w")
        edited_story_file.write(edited_story_string)
        edited_story_file.close()
        print(f"\nfinish editing {unedited_story_filename} at {strings.time_now()}\n")

        # now, do some logging...

        # record how many rewrites each chunk underwent.
        num_rewrites_of_chunks = [len(versions_of_story_chunk) - 1 for versions_of_story_chunk in versions_of_story_chunks]
        
        # based on this, record whether there were any rewrites at all.
        any_rewrites = any([num_rewrites_of_chunk > 0 for num_rewrites_of_chunk in num_rewrites_of_chunks])

        # record whether there were any rewriting failures. (of course, this can only be `True` if at least one chunk was rewritten `max_number_of_attempts` times, although even then it could still go either way.)
        any_failures = any(failure_rewriting_chunks)

        # add an entry to `logs/rewriting-stats.txt`.
        replacement_stats_string = f"{unedited_story_filename}\nediting timestamp: {timestamp}\nrewriting attempts per chunk: {', '.join([str(num_rewrites_of_chunk) for num_rewrites_of_chunk in num_rewrites_of_chunks])}\nany failures: {str(any_failures)}\n\n"
        print(f"\nnum_rewrites_of_chunks is: {num_rewrites_of_chunks}\n")
        rewriting_stats_file = open("logs/rewriting-stats.txt", "a")
        rewriting_stats_file.write(replacement_stats_string)
        rewriting_stats_file.close()

        # if there were any rewriting failures, make a special failure log file.
        if any_failures:
            rewriting_failure_log_file = open(f"logs/rewriting-failure-logs/rewriting-failure-log-{unedited_story_filename[:-4]}_edited-at_{timestamp}", "w")
            rewriting_failure_log_file.write(f"a rewrite failed when attempting to edit {unedited_story_filename}\nediting timestamp: {timestamp}\ncheck the verbose rewriting-log file logs/rewriting-logs/rewriting-log-{unedited_story_filename}_edited-at_{timestamp}.txt")

        # if there were any rewrites, make a verbose log of them.
        # (in a previous version of this code (when we were only removing digits), we did some annoyingly tricksy regex stuff to try and find the old sentence and match it with its replacement. but now that we're replacing the overused words too, this is an unreasonably onerous operation. so we'll just be sure to check the verbose log files (as well as the failure logs), and leave it at that.)
        if any_rewrites:
            rewriting_log_file = open(f"logs/rewriting-logs/rewriting-log-{unedited_story_filename[:-4]}_edited-at_{timestamp}.txt", "w")
            rewriting_log_strings = []
            for (index, versions_of_story_chunk) in enumerate(versions_of_story_chunks):
                if len(versions_of_story_chunk) > 1:
                    original_version_of_chunk = versions_of_story_chunk[0]
                    intermediate_versions_of_chunk = versions_of_story_chunk[1: -1]
                    final_version_of_chunk = versions_of_story_chunk[-1]
                    # note that these log files are _only_ meant for human reading, so we can be fast-and-loose with our separators.
                    rewriting_log_string_for_chunk = f"""REWRITING SUCCESS: {not failure_rewriting_chunks[index]}

triggers for initial rewrite (overused words are listed as tuples (word, num_apperances, num_allowed)): {', '.join(triggers_for_rewriting_chunks[index])}

number of rewrites: {num_rewrites_of_chunks[index]}

{strings.separator}

ORIGINAL TEXT:

{original_version_of_chunk}

{strings.separator}

INTERMEDIATE REWRITES:

{(strings.nn + '-----' + strings.nn).join(intermediate_versions_of_chunk)}

{strings.separator}

FINAL VERSION (appearing in edited version of story):

{final_version_of_chunk}"""
                    rewriting_log_strings.append(rewriting_log_string_for_chunk)
            rewriting_log_string = strings.separator_long.join([overused_word_allowances_string] + rewriting_log_strings)
            rewriting_log_file.write(rewriting_log_string)
            rewriting_log_file.close()

    return None



### let's edit some stories!

# doing these on wed 11/29 at ~8pm.
# edit_story("story-unedited_berkeley_2023-11-28_22-32-51_long.txt")
# edit_story("story-unedited_berkeley_2023-11-28_22-32-51_short.txt")
# edit_story("story-unedited_paris_2023-11-28_22-32-51_long.txt")
# edit_story("story-unedited_paris_2023-11-28_22-32-51_short.txt")
# edit_story("story-unedited_paris_2023-11-28_22-32-51_long.txt")