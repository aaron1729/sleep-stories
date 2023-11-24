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

################################################################################

def get_stops(destination, num_stops = 20):

    input = inputs[destination]

    print(f"\ngetting stops with tidbits for {input['destination_fullname']} with timestamp {timestamp} at {datetime_str_to_timestamp(str(datetime.now()))}\n")

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
    stops_with_tidbits_file.write("\n\n=====\n\n".join(stops_with_tidbits))
    stops_with_tidbits_file.close()

    print("\ndone getting tidbits\n")

    return None

################################################################################

### let's get some stops!

for input in inputs:
    get_stops(input)

# get_stops("berkeley")