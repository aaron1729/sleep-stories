from openai import OpenAI
client = OpenAI()

import re

from datetime import datetime

from os import listdir
from os.path import isfile, join

import models
import strings
from inputs import *

timestamp = strings.time_now()

################################################################################

# `length` must be either string "short" or "long".
# `destination` must be a key in the `inputs` object in `inputs.py`.
# as for `num_stops_parameter`:
    # if `length` is "short":
        # then, `num_stops_parameter` is a tuple (a, c, n, z):
            # a is the number of stops bundled into initial chunk -- assumed to be at least 1;
            # c is the number of middle completions;
            # n is the number of stops per middle completion;
            # z is the number of stops bundled into final chunk -- also assumed to be at least 1.
        # so, the total number of stops needed is a + c*n + z.
        # we went back and forth, but ultimately decided that the best values are 1, 5, 2, and 1 -- and these are the default values.
    # if `length` is "long":
        # then, `num_stops_parameter` is just num_stops, which defaults to 20.
# `stops_filename` defaults to the most recent `stops` file for the given destination, but this can be overridden. (this should include the ending ".txt" in the filename.)

def write_story(length, destination, num_stops_parameter = None, stops_filename = None):

    input = inputs[destination]

    # unpack num_stops_parameter to define a, c, n, z, and num_stops. (to avoid errors, these should be explicitly set to `None` if they don't exist.)
    if length == "short":
        if num_stops_parameter == None:
            num_stops_parameter = (1, 5, 2, 1)
        (a, c, n, z) = num_stops_parameter
        num_stops = a + c*n + z
    if length == "long":
        if num_stops_parameter == None:
            num_stops_parameter = 20
        num_stops = num_stops_parameter
        (a, c, n, z) = (None, None, None, None)

    print(f"\nwriting a {length} story set in {input['destination_fullname']} with {num_stops} stops{f' (with a={a}, c={c}, n={n}, and z={z})' if length == 'short' else ''} and with timestamp {timestamp} at {strings.time_now()}\n")

    # if the stops file is specified, ensure that it matches the destination. and if it isn't, get the most recent one.
    if stops_filename:
        if stops_filename.split("_")[1] != destination:
            raise Exception(f"writing a story set in {destination}, but the specified stops file is {stops_filename}")
    else:
        stops_filename = strings.get_latest_filename(input['destination'], "stops")
        if not stops_filename:
            raise Exception(f"writing a story set in {destination}, but there is no corresponding stops file")
    
    stops = open(f"stops/{stops_filename}", "r").read().split(strings.separator)

    if len(stops) < num_stops:
        raise Exception(f"attempting to write a long story with {num_stops} stops, but there are only {len(stops)} in the selected `stops` file.")
    
    stops = stops[: num_stops]

    system_prompt = strings.system_prompt_for_story(length, num_stops)
    system_message = {"role": "system", "content": system_prompt}

    initial_user_prompt = strings.initial_user_prompt_for_story(
        length,
        input['destination_fullname'],
        input['transport_method'],
        input['tour_guide'],
        input['season'],
        stops,
        a)
    initial_user_message = {"role": "user", "content": initial_user_prompt}

    message_list = [system_message, initial_user_message]

    story = ""

    print("\nfetching completion number 0 (the initial completion)\n")
    print(f"\nand the user prompt is:\n\n{initial_user_prompt}\n")
    completion = client.chat.completions.create(
        model = models.gpt_model,
        messages = message_list
    )
    initial_assistant_prompt = completion.choices[0].message.content
    story += initial_assistant_prompt
    initial_assistant_message = {"role": "assistant", "content": initial_assistant_prompt}
    message_list.append(initial_assistant_message)

    middle_user_prompts = strings.middle_user_prompts_for_story(
        length,
        stops,
        a, c, n)
    middle_user_messages = [{"role": "user", "content": middle_user_prompt} for middle_user_prompt in middle_user_prompts]

    splitting_failure_indices = []
    for (index, middle_user_message) in enumerate(middle_user_messages):
        print(f"\nfetching completion number {index + 1}\n")
        print(f"\nand the user prompt is:\n\n{middle_user_message['content']}\n")
        message_list.append(middle_user_message)
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = message_list
        )
        middle_assistant_prompt = completion.choices[0].message.content
        middle_assistant_message = {"role": "assistant", "content": middle_assistant_prompt}
        message_list.append(middle_assistant_message)
        if length == "long":
            story += strings.separator + middle_assistant_prompt
        elif length == "short":
            print(f"\nwriting short story, and the raw middle_assistant_prompt (with chunks hopefully separated by '*****') is:\n\n{middle_assistant_prompt}\n")
            chunks = [string.replace("*", "").strip() for string in middle_assistant_prompt.split("***") if len(string.replace("*", "").strip()) > 3]
            if len(chunks) != n:
                splitting_failure_indices.append(index)
            for (chunk_index, chunk) in enumerate(chunks):
                print(f"\nchunk number {chunk_index} is:\n{chunk}\n")
                story += strings.separator + chunk
    
    final_user_prompt = strings.final_user_prompt_for_story(
        length,
        input['destination_fullname'],
        input['transport_method'],
        stops,
        a, c, n, z)
    final_user_message = {"role": "user", "content": final_user_prompt}
    message_list.append(final_user_message)

    print(f"\nfetching completion number {str(num_stops + 1) if length == 'long' else str(c+1)} (the final completion)\n")
    print(f"\nand the user prompt is:\n{final_user_message['content']}\n")
    completion = client.chat.completions.create(
        model = models.gpt_model,
        messages = message_list
    )
    final_assistant_prompt = completion.choices[0].message.content
    story += strings.separator + final_assistant_prompt

    # add the metadata of which stops file this was based on.
    story += f"{strings.separator}this story has num_stops={num_stops}{f' with a={a}, c={c}, n={n}, and z={z}' if length == 'short' else ''} and was written based on the stops file: {stops_filename}"
    
    # write the story file.
    story_filename = f"story-unedited_{input['destination']}_{timestamp}_{length}.txt"
    story_file = strings.open_safe("stories-unedited", story_filename, "w")
    story_file.write(story)
    story_file.close()

    print(f"\nfinished writing {length} story set in {input['destination_fullname']} with timestamp {timestamp} at {strings.time_now()}\n")

    # log any splitting failures.
    if len(splitting_failure_indices) > 0:
        print("\nthere are splitting failures; logging them now\n")
        splitting_failure_log_file = strings.open_safe("logs", "splitting-failure-log.txt", "a")

        splitting_failure_string = f"{story_filename}: {', '.join([str(splitting_failure_index) for splitting_failure_index in splitting_failure_indices])}"
        splitting_failure_log_file.write(splitting_failure_string)
        splitting_failure_log_file.close()
    
    return None



### let's write some stories!
# write_story(...)