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
    
    stops_with_tidbits_filename = f"stops_{input['destination']}_{timestamp}.txt"
    stops_with_tidbits_file = strings.open_safe("stops", stops_with_tidbits_filename, "w")
    stops_with_tidbits_file.write(strings.separator.join(stops_with_tidbits))
    stops_with_tidbits_file.close()

    print(f"\nfinished writing {stops_with_tidbits_filename} at {strings.time_now()}\n")

    return None

################################################################################

### let's get some stops!
# get_stops(...)


### monday 1/15/2024

# ~11:30am
# get_stops("seattle")

# ~1pm
# get_stops("arizona")
# get_stops("yucatan")
# get_stops("vienna")
# get_stops("budapest")
# get_stops("nepal")
# get_stops("hawaii")
# get_stops("iceland")
# get_stops("montreal")

# 1:49pm
# get_stops("taipei")
# get_stops("losangeles")
# get_stops("normandy")
# get_stops("amsterdam")
# get_stops("puertorico")
# get_stops("patagonia")
# get_stops("prague")

# 1:50pm
# get_stops("mumbai")
# get_stops("goa")
# get_stops("yellowstone")
# get_stops("rome")
# get_stops("marrakech")
# get_stops("accra")
# get_stops("addisababa")

# 1:51pm
# get_stops("madagascar")
# get_stops("seoul")
# get_stops("beijing")
# get_stops("vancouver")
# get_stops("norway")
# get_stops("dubrovnik")