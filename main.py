from openai import OpenAI
client = OpenAI()

from datetime import datetime
def datetime_str_to_timestamp(str):
    return str[:10] + "_" + str[11:13] + "-" + str[14:16] + "-" + str[17:19]

start_time = str(datetime.now())
timestamp = datetime_str_to_timestamp(start_time)



##### PARAMETERS

num_stops = 20

inputs = [
    # {
    #     "destination": "mexico-city",
    #     "destination_fullname": "Mexico City, Mexico",
    #     "transport_method": "private limousine"
    # },
    # {
    #     "destination": "thailand",
    #     "destination_fullname": "Thailand",
    #     "transport_method": "tuk tuk (i.e. rickshaw)"
    # },
    # {
    #     "destination": "barcelona",
    #     "destination_fullname": "Barcelona, Spain",
    #     "transport_method": "guided bike tour"
    # },
    # {
    #     "destination": "lisbon",
    #     "destination_fullname": "Lisbon, Portugal",
    #     "transport_method": "tram ride"
    # },
    # {
    #     "destination": "seoul",
    #     "destination_fullname": "Seoul, South Korea",
    #     "transport_method": "subway"
    # },
    {
        "destination": "miami",
        "destination_fullname": "Miami, Florida",
        "transport_method": "flashy red convertible sports car"
    },
    # {
    #     "destination": "venice",
    #     "destination_fullname": "Venice, Italy",
    #     "transport_method": "gondola"
    # },
    # {
    #     "destination": "paris",
    #     "destination_fullname": "Paris, France",
    #     "transport_method": "river boat cruise"
    # },
    # {
    #     "destination": "galapagos-islands",
    #     "destination_fullname": "Galapagos Islands",
    #     "transport_method": "private yacht with a captain who also serves as a tour guide"
    # },
    # {
    #     "destination": "greece",
    #     "destination_fullname": "Greece",
    #     "transport_method": "mostly catamaran, but also donkey ride on Santorini"
    # },
    # {
    #     "destination": "italy",
    #     "destination_fullname": "Italy",
    #     "transport_method": "Vespa motor scooter"
    # },
    # {
    #     "destination": "berlin",
    #     "destination_fullname": "Berlin, Germany",
    #     "transport_method": "subway"
    # },
]


for input in inputs:

    print(f"\nwriting a sleep story set in: {input['destination_fullname']} ({timestamp})\n")



    ##### GET LIST OF STOPS

    user_prompt_for_stops = f"""
    I love traveling. I'm going on a trip to {input['destination']}. Please name {num_stops} popular sightseeing locations there that I could visit by {input['transport_method']}. List these in an order so that no two adjacent sightseeing locations are too similar; for example, if one is a museum, the next would ideally be something like an outdoor market. 
    
    Please separate the different sightseeing locations with five asterisks (i.e. the string '*****'). Please make sure to separate the sightseeing locations with five asterisks.

    The entire tour should feel like a calm and soothing dream. Please make sure that NONE of these sightseeing locations is dark, stressful, or violent. For example, DO NOT include a tour of a Holocaust museum.
    
    Please also include a one-line description of each sightseeing location. Here is an example, corresponding to a riverboat cruise in Paris.

    EXAMPLE:

    Eiffel Tower: An iconic symbol of France, this remarkable structure offers a stunning panoramic view of Paris. Your river cruise will provide a spectacular perspective of its beauty.
    
    """
    user_message_for_stops = {"role": "user", "content": user_prompt_for_stops}

    print(f"getting list of {num_stops} stops\n")
    completion = client.chat.completions.create(
        model = "gpt-4-32k",
        messages = [user_message_for_stops]
    )

    stops = [string.replace("*", "").strip() for string in completion.choices[0].message.content.split("***") if len(string.replace("*", "").strip()) > 3]
    print("here are the stops:")
    for stop in stops:
        print(stop)
    assert len(stops) == num_stops



    ##### GET TIDBITS FOR EACH STOP

    system_prompt_for_tidbits = f"""
    I am on a vacation to {input['destination_fullname']}, and am taking a sightseeing tour in and around the area. I will name a sightseeing location on the tour. Associated to this sightseeing location, please list some historical facts, literary references, or relevant quotes -- at least three or four of these.

    If visiting the sightseeing location typically involves eating or drinking, please also include a typical dish or dining experience.

    Lastly, please also describe a pleasant human experience involved in visiting this sightseeing location by {input['transport_method']}. Some examples might be: buying a ticket; consulting a map; taking in natural beauty such as plants, animals, clouds, trees, or sunshine. Please be specific in the experience you describe.

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
    stops_with_tidbits_file = open("prompts/" + input['destination'] + "_" + timestamp + ".txt", "a")
    for stop in stops:
        user_message_for_tidbit = {"role": "user", "content": stop}
        completion = client.chat.completions.create(
            model = "gpt-4-32k",
            messages = [system_message_for_tidbits, user_message_for_tidbit]
        )
        stop_with_tidbit = stop + "\n\n" + completion.choices[0].message.content
        stops_with_tidbits.append(stop_with_tidbit)
        stops_with_tidbits_file.write(stop_with_tidbit + "\n\n=====\n\n")
    stops_with_tidbits_file.close()

    print("done getting tidbits")



    ##### GET STORY

    example_story = open("prompts/example_story.txt", "r").read()

    system_prompt_for_story = """
    I'm going to give you a tourist destination, a mode of transportation, and a bunch of sightseeing locations there, one at a time. Please write me a story like the example far below. Please make sure to write in the PRESENT TENSE.

    As I name each sightseeing location, I'm also going to give you some tidbits about it: historical facts, literary references, relevant quotes, typical dining experiences, and possibly also human experiences involved in visiting this sightseeing location by the chosen mode of transportation. Please try to include these. However, don't include more than THREE food experiences total.

    Also, try to incorporate SPECIFIC tidbits; these are better than simply discussing the importance of a sightseeing location in general terms.

    Please also include little moments describing our feelings as we take in these sights and sounds and tastes. These should all be pleasant and inspiring feelings.

    Please don't include anything somber. Keep the tone happy, warm, uplifting, and relaxing.
    
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

    Across the room, his associate, a stalwart silhouette against the flickering glow of the forge, threads a sinewy strand of silver through a weather-worn fingertip. Twisting and turning with careful precision, he molds the raw metal into an exquisite wearable piece of art. His eyes glint with reflected light and unwavering determination, while his hands orchestrate a silent symphony, bringing an unearthly luminescence to the once somber material.

    END EXAMPLE REWRITE ONE:


    START EXAMPLE REWRITE TWO:

    OLD TEXT:

    The National Museum of Anthropology in Mexico City offers more than just a stroll down the country's ancient past; it continues to narrate the story of Mexico's present-day indigenous groups. In-depth ethnographic exhibits open windows to the diverse and vibrant life of the many indigenous cultures still thriving in Mexico today, highlighting their languages, traditions, and everyday life.

    NEW TEXT:

    The main attraction in Nahua Hall is a splendid array of traditional costumes worn by Nahua communities. The costumes often consist of two-part attires - blouses known as 'huipil' and skirts known as 'enredo'. These are often adorned with detailed motifs that depict local livestock, crops, and scenery, each symbolizing a different aspect of the Nahua worldview and mythology.

    The colors used in the blouses, skirts, and rebozos (a traditional garment similar to a shawl) are bold, organic, and eye-catching. You will find primary colors - reds, blues, greens, often alternating with secondary hues such as purple and orange, to tell vibrant stories of each garment's unique roots.

    The huipil, typically made of cotton, is a square-cut, loose sleeveless tunic. Its vibrant surface teems with delicate embroidery and exquisite beadwork; flower motifs, birds, and symbols related to ancient Nahua gods are common elements.

    END EXAMPLE REWRITE TWO:


    """ + "\n\n=====\n\n" + example_story
    system_message = {"role": "system", "content": system_prompt_for_story}

    user_prompt_for_setting_scene = f"Please begin by setting the scene. We are traveling in {input['destination_fullname']}. We are taking a sightseeing tour by {input['transport_method']}. However, JUST set the scene; don't begin the sightseeing tour just yet. Make me excited about my trip overall, and about the upcoming tour. Keep this short -- just three or four paragraphs. Please don't end your response with a summary, though, because we will continuing the story!"
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
    for (index, stop_prompt) in stops_with_tidbits:
        stop_prompt += "\n\n Please don't end your response with a summary, though, because we will continuing the story!"
        if index == len(stops_with_tidbits) - 1:
            stop_prompt += "\n\n Additionally, at the beginning of your response, please do NOT refer to the sightseeing location where we've just been."
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

    print(f"fetching story chunk number {i+1} (the ending)")
    user_prompt_for_ending_story = f"Please conclude the story about our sightseeing tour by {input['transport_method']} in {input['destination_fullname']}. Keep it upbeat, gentle, and inspiring."
    user_message_for_ending_story = {"role": "user", "content": user_prompt_for_ending_story}
    message_list.append(user_message_for_ending_story)
    completion = client.chat.completions.create(
        model = "gpt-4-32k",
        messages = message_list
    )
    assistant_prompt_with_story_ending = completion.choices[0].message.content
    story += "\n\n=====\n\n" + assistant_prompt_with_story_ending

    story_file = open("stories/" + input['destination'] + "_" + timestamp + ".txt", "w")
    story_file.write(story)
    story_file.close()

    story_end_time = datetime_str_to_timestamp(str(datetime.now()))
    print("finished writing story at:", story_end_time)