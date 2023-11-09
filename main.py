from openai import OpenAI
client = OpenAI()

from datetime import datetime
now = str(datetime.now())
timestamp = now[:10] + "_" + now[11:13] + "-" + now[14:16] + "-" + now[17:19]

##### PARAMETERS

destination_fullname = "Yosemite National Park"
destination = "yosemite"
num_stops = 10
transport_method = "long-distance trail-running"

##### GET LIST OF STOPS

user_prompt_for_stops = f"I love traveling. I'm going on a trip to {destination}. Please name {num_stops} popular sightseeing locations there that I could visit by {transport_method}."
user_message_for_stops = {"role": "user", "content": user_prompt_for_stops}

print(f"\ngetting list of {num_stops} stops\n")
completion = client.chat.completions.create(
    model = "gpt-4-32k",
    messages = [user_message_for_stops]
)

##### GET TIDBITS FOR EACH STOP

assistant_prompt_with_stops = completion.choices[0].message.content
print("assistant_prompt_with_stops is:\n\n", assistant_prompt_with_stops)
assistant_message_with_stops = {"role": "assistant", "content": assistant_prompt_with_stops}

user_prompt_for_tidbits = f"""
Wonderful, thank you!

For each of these sightseeing locations, please list some historical facts, literary references, or relevant quotes -- at least three or four of these.

If visiting the sightseeing location typically involves eating or drinking, please also include a typical dish or dining experience.

Lastly, please also describe a pleasant human experience involved in visiting this sightseeing location by {transport_method}. Some examples might be: buying a ticket; consulting a map; taking in natural beauty such as plants, animals, clouds, trees, or sunshine. Please be specific in the experience you describe.

For each sightseeing location, please format the above items as a bullet-pointed list. Additionally, please separate the lists for different sightseeing locations with five asterisks (i.e. the string '*****'). Please make sure to separate the lists with five asterisks.

HERE IS AN EXAMPLE OF WHAT I'M LOOKING FOR. (However, please note that this list only has three locations. This list is for a sightseeing tour of Berlin by subway.)

1. Berlin Television Tower (Fernsehturm)
- At 368 meters, it's the tallest structure in Germany.
- The tower's sphere features a revolving restaurant.
- Constructed between 1965 and 1969 by the government of the German Democratic Republic (GDR).
- When you exit the adjacent subway stop, you suddenly see the Fernsehturm reaching towards the sunny sky.
*****
2. East Side Gallery
- It's the longest remaining part of the Berlin Wall.
- Features over 100 murals by artists from all over the world.
- The most famous painting is the "Fraternal Kiss" between Brezhnev and Honecker.
- Next to the gallery is a world-famous currywurst stand.
*****
3. Brandenburg Gate
- Built in the 18th century as a symbol of peace.
- Napoleon once marched through the gate's arches to take the city.
- Ronald Reagan famously said, "Mr. Gorbachev, tear down this wall!" near this site.
- People love to feed the birds that congregate around the Brandenburg Gate.
"""
user_message_for_tidbits = {"role": "user", "content": user_prompt_for_tidbits}

print("\ngetting list of stops with tidbits\n")
completion = client.chat.completions.create(
    model = "gpt-4-32k",
    messages = [user_message_for_stops, assistant_message_with_stops, user_message_for_tidbits]
)
stops_with_tidbits = completion.choices[0].message.content

stops_with_tidbits_file = open("prompts/" + destination + "_" + timestamp + ".txt", "w")
stops_with_tidbits_file.write(stops_with_tidbits)
stops_with_tidbits_file.close()

stop_list = stops_with_tidbits.split("***")

##### GET STORY

example_story = open("prompts/example_story.txt", "r").read()

system_prompt = """I'm going to give you a tourist destination, a mode of transportation, and a bunch of sightseeing locations there, one at a time. Please write me a story like the example below.

As I name each sightseeing location, I'm also going to give you some tidbits about it: historical facts, literary references, relevant quotes, typical dining experiences, and possibly also human experiences involved in visiting this sightseeing location by the chosen mode of transportation. Please try to include these. However, don't include more than THREE food experiences.

Please also include little moments describing our feelings as we take in these sights. These should all be pleasant and inspiring feelings.

Please don't include anything dark. Keep the tone happy, warm, uplifting, and relaxing.

As we go from spot to spot, please transition us between them through pleasant tourist activities such as walking, buying a ticket, looking at the map to find our way, etc. You can also refer to activities related to our chosen mode of transportation, such as getting on or off of a rickshaw.

Don't end the story until I tell you to. Don't reference the passing of time or the time of day. Please don't use the word "tapestry" or "testament."
""" + "\n\n=====\n\n" + example_story

user_prompt_for_setting_scene = f"Please begin by setting the scene. We are traveling in {destination_fullname}. We are taking a sightseeing tour by {transport_method}. However, JUST set the scene; don't begin the sightseeing tour just yet. Make me excited about my trip overall, and about the upcoming tour. Please don't end your response with a summary, though, because we will continuing the story!"

system_message = {"role": "system", "content": system_prompt}
user_message_for_setting_scene = {"role": "user", "content": user_prompt_for_setting_scene}

message_list = [system_message, user_message_for_setting_scene]

story = ""

print("fetching story chunk number 0 (setting the scene)")
completion = client.chat.completions.create(
    model = "gpt-4-32k",
    messages = message_list
)
assistant_prompt_with_scene_setting = completion.choices[0].message.content
story += assistant_prompt_with_scene_setting
assistant_message_with_scene_setting = {"role": "assistant", "content": assistant_prompt_with_scene_setting}
message_list.append(assistant_message_with_scene_setting)

stop_messages = []
for stop_prompt in stop_list:
    stop_prompt += "\n\n Please don't end your response with a summary, though, because we will continuing the story!"
    stop_message = {"role": "user", "content": stop_prompt}
    stop_messages.append(stop_message)

i = 0
for user_message_for_stop in stop_messages:
    print("fetching story chunk number", i+1)
    message_list.append(user_message_for_stop)
    completion = client.chat.completions.create(
        model = "gpt-4-32k",
        messages = message_list
    )
    assistant_prompt_with_story = completion.choices[0].message.content
    story += "\n\n=====\n\n" + assistant_prompt_with_story
    assistant_message_with_story = {"role": "assistant", "content": assistant_prompt_with_story}
    message_list.append(assistant_message_with_story)
    i += 1

print(f"fetching story chunk number {i} (the ending)")
user_prompt_for_ending_story = f"Please conclude the story about our sightseeing tour by {transport_method} in {destination_fullname}. Keep it upbeat, gentle, and inspiring."
user_message_for_ending_story = {"role": "user", "content": user_prompt_for_ending_story}
message_list.append(user_message_for_ending_story)
completion = client.chat.completions.create(
    model = "gpt-4-32k",
    messages = message_list
)
assistant_prompt_with_story_ending = completion.choices[0].message.content
story += "\n\n=====\n\n" + assistant_prompt_with_story_ending

story_file = open("stories/" + destination + "_" + timestamp + ".txt", "w")
story_file.write(story)
story_file.close()