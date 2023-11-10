# hard-coded variables
destination = "istanbul"
timestamp = "2023-11-09_21-07-06"
min_stops = 1 # this does NOT include the last stop, which is stitched together with the ending material.

# generated variables
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
    list_old = string.split("\n\n")
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
middle = ",\n".join(processed_chunks[min_stops+1:-2])
end = " /\n".join(processed_chunks[-2:])

output = f"""// this story has timestamp {timestamp}

package com.downdogapp.cue

object {object_name} : SleepPoseCues {{

override fun Config.start() =
{start}

override fun Config.middle() = listOf(
{middle}
)

override fun Config.end() =
{end}
}}"""

output_file = open("code/" + file_name, "w")
output_file.write(output)
output_file.close()