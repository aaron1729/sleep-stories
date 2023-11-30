from openai import OpenAI
client = OpenAI()

import re

import models
import strings
from inputs import *

timestamp = strings.time_now()

################################################################################

def get_stops(destination, num_stops = 20):

    input = inputs[destination]

    print(f"\ngetting stops with tidbits for {input['destination_fullname']} with timestamp {timestamp} at {strings.time_now()}\n")

    ##### GET LIST OF STOPS

    user_message_for_stops = {"role": "user", "content": strings.user_prompt_for_stops(input['destination_fullname'], num_stops, input['transport_method'], input['requested_sightseeing_stops'])}
    messages_for_getting_stops = [user_message_for_stops]

    print(f"\ngetting list of {num_stops} stops\n")
    completion = client.chat.completions.create(
        model = models.gpt_model,
        messages = messages_for_getting_stops
    )
    assistant_prompt_with_stops = completion.choices[0].message.content
    assistant_message_with_stops = {"role": "assistant", "content": assistant_prompt_with_stops}
    messages_for_getting_stops.append(assistant_message_with_stops)
    stops = [string.replace("*", "").strip() for string in assistant_prompt_with_stops.split("***") if len(string.replace("*", "").strip()) > 3]
    print(f"\nthere are {len(stops)} stops, and they are:\n")
    for stop in stops:
        print(stop + "\n")
    
    while len(stops) < num_stops:
        print("\nnot enough stops! getting more...\n")
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
        print(f"\nthere are {len(stops)} stops, and they are:\n")
        for stop in stops:
            print(stop + "\n")
        
    ##### GET TIDBITS FOR EACH STOP

    system_message_for_tidbits = {"role": "system", "content": strings.system_prompt_for_tidbits(input['destination_fullname'])}

    print("\ngetting list of stops with tidbits\n")

    stops_with_tidbits = []
    for stop in stops:
        user_message_for_tidbit = {"role": "user", "content": stop}
        completion = client.chat.completions.create(
            model = models.gpt_model,
            messages = [system_message_for_tidbits, user_message_for_tidbit]
        )
        stop_with_tidbit = stop + "\n\n" + completion.choices[0].message.content
        stops_with_tidbits.append(stop_with_tidbit)
    
    stops_with_tidbits_file = open(f"stops/stops_{input['destination']}_{timestamp}.txt", "w")
    stops_with_tidbits_file.write(strings.separator.join(stops_with_tidbits))
    stops_with_tidbits_file.close()

    print("\ndone getting tidbits\n")

    return None

################################################################################

### let's get some stops!

for input in inputs:
    get_stops(input)

# get_stops("berkeley")