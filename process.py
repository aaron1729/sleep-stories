import re # regular expressions
from os import listdir # operating system; list the files in a directory
from os.path import isfile, join
txt_file_names_incl_hidden = [f for f in listdir("stories/") if isfile(join("stories/", f))]
txt_file_names = [file_name for file_name in txt_file_names_incl_hidden if file_name[0] != "."]
txt_file_names.sort() # make alphabetical, for reproduceability.

for txt_file_name in txt_file_names:

    [destination, date, time] = txt_file_name.split("_")
    timestamp = date + "_" + time[:8]
    min_stops = 1 # this does NOT include the last stop, which is stitched together with the ending material.
    Destination = destination[:1].upper() + destination[1:]
    object_name = "SleepStoryTravel" + Destination + "Cues"
    file_name = object_name + ".kt"

    #####

    file = open("stories/" + destination + "_" + timestamp + ".txt", "r").read()

    # this is a list of strings. each one is a single full response from chat GPT.
    chunks = file.split("=====")

    # this takes a chunk (a string corresponding to a single stop) and breaks it into paragraphs, and then organizes those into a single (but generally multi-line) string like the following:
        # "1st paragraph of the 3-paragraph chunk" /
        # "2nd paragraph of the 3-paragraph chunk" /
        # "3rd paragraph of the 3-paragraph chunk"
    def process_chunk(string):
        string = string.strip()
        # chunks consist of paragraphs. usually the paragraphs are separated by "\n\n", but occasionally GPT separates them with "\n \n", or even "\n  \n" (with two spaces).
        string_with_fixed_paragraph_separations = re.sub(r'\n *\n', '\n\n', string)
        list_old = string_with_fixed_paragraph_separations.split("\n\n")
        list_new = []
        for paragraph in list_old:
            paragraph_replaced = paragraph.replace("\"", "'")
            paragraph_stripped = paragraph_replaced.strip()
            paragraph_with_quotes = "\"" + paragraph_stripped + "\""
            list_new.append(paragraph_with_quotes)
        return " /\n".join(list_new)

    processed_chunks = []
    for chunk in chunks:
        processed_chunk = process_chunk(chunk)
        processed_chunks.append(processed_chunk)

    start = " /\n".join(processed_chunks[:min_stops+1])
    middle = ",\n\n".join(processed_chunks[min_stops+1:-2])
    end = " /\n".join(processed_chunks[-2:])

    output = f"""// this code is generated from the story file {destination}_{timestamp}.txt
    // min_stops is set to {min_stops}

    package com.downdogapp.cue

    object {object_name} : SleepStoryPoseCues {{

    override val start =
    {start}

    override val middle = listOf(
    {middle}
    )

    override val end =
    {end}
    }}"""

    output_file = open("code/" + file_name, "w")
    output_file.write(output)
    output_file.close()

    print(f"finished processing {destination}_{timestamp}.txt")