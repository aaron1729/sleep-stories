##### this only runs if in the stories (saved in 'stories/') come in long/short pairs!

import re # regular expressions
from os import listdir # operating system; list the files in a directory
from os.path import isfile, join
txt_file_names_incl_hidden = [f for f in listdir("stories/") if isfile(join("stories/", f))]
txt_file_names = [file_name for file_name in txt_file_names_incl_hidden if file_name[0] != "."]
txt_file_names.sort() # make alphabetical, for reproduceability.

# this is a dict, whose keys are destinations.
    # the value is itself a dict, with the keys "short" and "long".
        # the values of those are _also_ dicts, each of which has keys:
            # "timestamp"
            # "stops_with_tidbits"
            # "start"
            # "middle"
            # "end"
destinations = {}

min_stops_for_long_story = 1

for txt_file_name in txt_file_names:

    [destination, date, time, length] = txt_file_name[:-4].split("_")
    if not destination in destinations:
        destinations[destination] = {}
    destinations[destination][length] = {}
    timestamp = date + "_" + time
    destinations[destination][length]["timestamp"] = timestamp
    
    #####

    story_file = open("stories/" + destination + "_" + timestamp + "_" + length + ".txt", "r").read()
    
    destinations[destination][length]["stops_with_tidbits"] = open("prompts/" + destination + "_" + timestamp + ".txt", "r").read()
    
    # this is a list of strings. each string is a single full response from chatGPT, except for the last one which is just a record of the strings that used to contain digits but were (hopefully) replaced with ones that do not.
    chunks = story_file.split("=====")

    dedigitization_string = chunks[-1]
    chunks = chunks[: -1]

    # this function takes a chunk and breaks it into paragraphs, and then organizes those into a single (but generally multi-line) string like the following (with two tabs before each paragraph, to conform to linting style):
        # "1st paragraph of the 3-paragraph chunk" /
        # "2nd paragraph of the 3-paragraph chunk" /
        # "3rd paragraph of the 3-paragraph chunk"
    def process_chunk(string):
        string = string.strip()
        # chunks consist of paragraphs. usually the paragraphs are separated by "\n\n", but occasionally chatGPT separates them with "\n \n", or possibly even "\n  \n" (with two spaces).
        string_with_fixed_paragraph_separations = re.sub(r'\n *\n', '\n\n', string)
        list_old = string_with_fixed_paragraph_separations.split("\n\n")
        list_new = []
        for paragraph in list_old:
            paragraph_replaced = paragraph.replace("\"", "'")
            paragraph_stripped = paragraph_replaced.strip()
            paragraph_with_quotes = "\"" + paragraph_stripped + "\""
            list_new.append("       " + paragraph_with_quotes)
        return " /\n".join(list_new)

    processed_chunks = []
    for chunk in chunks:
        processed_chunk = process_chunk(chunk)
        processed_chunks.append(processed_chunk)

    if length == "short":
        destinations[destination][length]["start"] = " /\n".join(processed_chunks[: 1])
        destinations[destination][length]["middle"] = ",\n\n".join(processed_chunks[1: -1])
        destinations[destination][length]["end"] = " /\n".join(processed_chunks[-1: ])

    if length == "long":
        destinations[destination][length]["start"] = " /\n".join(processed_chunks[: min_stops_for_long_story+1])
        destinations[destination][length]["middle"] = ",\n\n".join(processed_chunks[min_stops_for_long_story+1: -2])
        destinations[destination][length]["end"] = " /\n".join(processed_chunks[-2: ])

#####




for destination in destinations:
    Destination = destination[:1].upper() + destination[1:]
    object_name = "SleepStoryTravel" + Destination + "Cues"
    file_name = object_name + ".kt"

    output = f"""// this code is generated from the story files {destination}_{destinations[destination]['short']['timestamp']}_short.txt and {destination}_{destinations[destination]['long']['timestamp']}_long.txt.
// the stops-with-tidbits that went into the user prompts for both of these stories are copied at the bottom as comments -- first those for the short story, then those for the long story -- separated by a bunch of slashes.
// min_stops_for_long_story is set to {min_stops_for_long_story}.



package com.downdogapp.cue

object {object_name} : SleepStoryPoseCues {{

    override val startShort =
{destinations[destination]["short"]["start"]}

    override val middleShort = listOf(
{destinations[destination]["short"]["middle"]}
)

    override val endShort =
{destinations[destination]["short"]["end"]}

    override val start =
{destinations[destination]["long"]["start"]}

    override val middle = listOf(
{destinations[destination]["long"]["middle"]}
)

    override val end =
{destinations[destination]["long"]["end"]}

/*
////////////////////////////////////////////////////////////////////////////////

{destinations[destination]["short"]["stops_with_tidbits"]}

////////////////////////////////////////////////////////////////////////////////

{destinations[destination]["long"]["stops_with_tidbits"]}
*/
}}"""

    output_file = open("code/" + file_name, "w")
    output_file.write(output)
    output_file.close()