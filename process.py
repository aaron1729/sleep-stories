##### this code only runs if in the stories (saved in 'stories/') come in long/short pairs!

import re # regular expressions
from os import listdir # operating system; list the files in a directory
from os.path import isfile, join
txt_file_names_incl_hidden = [f for f in listdir("stories/") if isfile(join("stories/", f))]
txt_file_names = [file_name for file_name in txt_file_names_incl_hidden if file_name[0] != "."]
txt_file_names.sort() # make alphabetical, for reproduceability.

# this is a dict, whose keys are destinations.
    # the value of each destination is itself a dict, with the keys "short" and "long".
        # the values of those are _also_ dicts, each of which has keys:
            # "timestamp"
            # "stops_with_tidbits"
            # "dedigitization_comment_string"
            # "start"
            # "middle"
            # "end"
destinations = {}

min_stops_for_long_story = 1

for txt_file_name in txt_file_names:

    print(f"now processing {txt_file_name}")

    [destination, date, time, length] = txt_file_name[:-4].split("_")
    if not destination in destinations:
        destinations[destination] = {}
    destinations[destination][length] = {}
    timestamp = f"{date}_{time}"
    destinations[destination][length]["timestamp"] = timestamp
    
    #####

    story_string = open(f"stories/{destination}_{timestamp}_{length}.txt", "r").read()
    
    # retrieve the "stops with tidbits" info; this gets saved as comments at the bottom of the kotlin file, for easy reference.
    destinations[destination][length]["stops_with_tidbits"] = open(f"stops_with_tidbits/{destination}_{timestamp}.txt", "r").read()
    
    # this is a list of strings. each string is a single full response from chatGPT, except for the last one which is just a record of the strings that used to contain digits but were (hopefully) replaced with ones that do not.
    chunks = story_string.split("=====")

    # the last entry of the `chunks` list contains the dedigitization metadata. peel this off and save it.
    dedigitization_string = chunks[-1]
    dedigitization_string = f"{length.upper()}_STORY_{dedigitization_string.strip()}"
    dedigitization_lines = dedigitization_string.split("\n")
    dedigitization_lines_with_slashes = [f"// {dedigitization_line}" for dedigitization_line in dedigitization_lines]
    dedigitization_comment_string = "\n".join(dedigitization_lines_with_slashes)
    destinations[destination][length]["dedigitization_comment_string"] = dedigitization_comment_string
    chunks = chunks[: -1]

    ##### COMMENTS ON THE FUNCTION process_chunk BELOW...

    ##### FURTHER UPDATE (2023-11-20): a "minibatch" here is what's later in the pipeline called a "cue" (as in "yoga cue"). we'll be associating a dall-e prompt, and thereafter an image, to each minibatch. so to do that, we'll want to save the raw minibatches (without quote-marks) in a file, in `cues`. these are separated by `\n`.
    
    ##### NEW VERSION (2023-11-15): split each _paragraph_ into minibatches -- two sentences each, and if there are an odd number then the last one on its own. so for a 3-sentence paragraph followed by a 4-sentence paragraph, we want:
        # "pgh1 minibatch 1" /
        # "pgh1 minibatch 2" /
        # "pgh2 minibatch 1" / ....
    # the commas will _only_ be in the same spot: separating the `listOf` arguments in the middle val thingy.

    ##### ORIGINAL VERSION: this function takes a chunk and breaks it into paragraphs, and then organizes those into a single (but generally multi-line) string like the following (with two tabs before each paragraph, to conform to linting style):
        # "1st paragraph of the 3-paragraph chunk" /
        # "2nd paragraph of the 3-paragraph chunk" /
        # "3rd paragraph of the 3-paragraph chunk"
        
    def process_chunk(string):
        string = string.strip()
        # chunks consist of paragraphs. usually the paragraphs are separated by "\n\n", but occasionally chatGPT separates them with "\n \n", or possibly even "\n  \n" (with two spaces). so, fix this.
        string_with_fixed_paragraph_separations = re.sub(r'\n *\n', '\n\n', string)
        paragraphs = string_with_fixed_paragraph_separations.split("\n\n")
        minibatches = []
        minibatches_raw = []
        for paragraph in paragraphs:
            # we'll later wrap minibatches in double-quotes, so first replace these.
            paragraph_replaced = paragraph.replace("\"", "'")
            # split into sentences. beware that these can end with a period, exclamation point, or question mark. there can be a quote-mark or two, too.
            pattern_for_sentence_ending = r"([!\.\?]{1,4}'{0,2})\s+"
            paragraph_stripped = paragraph_replaced.strip()
            sentences_and_punctuations = re.split(pattern_for_sentence_ending, paragraph_stripped)
            # for whatever reason, the above seems to split _some_ periods away from their preceding sentences, but not all. so, put them together manually.
            sentences = []
            for shortstring in sentences_and_punctuations:
                # the check that `len(shortstring) > 4` is supposed to ensure that we're looking at an actual sentence, instead of just e.g. some funky punctuation in and around a period at the end of a sentence (e.g. some quotation marks).
                # however, there was an error in processing `queenstown_2023-11-21_18-59-20_short.txt` since an entire paragraph starts with `Mt. Nicholas Station, a historic icon` and so there was nowhere for the `Mt.` to get appended to in the `else` block. so if there are no sentences yet, then we'll just kick things off with `shortstring` no matter how short it is.
                if len(shortstring) > 4 or len(sentences) == 0:
                    sentences.append(shortstring)
                else:
                    sentences[len(sentences)-1] += shortstring
            num_full_minibatches = len(sentences) // 2
            # use 4 spaces here -- down dog linting is 2 spaces per tab, and this is indented by 2 tabs.
            for i in range(num_full_minibatches):
                minibatch = f"    \"{sentences[2*i]} {sentences[2*i+1]}\""
                minibatch_raw = sentences[2*i] + " " + sentences[2*i+1]
                minibatches.append(minibatch)
                minibatches_raw.append(minibatch_raw)
            if len(sentences) % 2 == 1:
                minibatch = f"    \"{sentences[-1]}\""
                minibatch_raw = sentences[-1]
                minibatches.append(minibatch)
                minibatches_raw.append(minibatch_raw)
        return " /\n".join(minibatches), "\n".join(minibatches_raw)

    processed_chunks = []
    processed_chunks_raw = []
    for chunk in chunks:
        processed_chunk, processed_chunk_raw = process_chunk(chunk)
        processed_chunks.append(processed_chunk)
        processed_chunks_raw.append(processed_chunk_raw)

    # store the processed_chunks for later integration into a single kt file containing both a short story and a long story.

    if length == "short":
        destinations[destination][length]["start"] = " /\n".join(processed_chunks[: 1])
        destinations[destination][length]["middle"] = ",\n\n".join(processed_chunks[1: -1])
        destinations[destination][length]["end"] = " /\n".join(processed_chunks[-1: ])

    if length == "long":
        destinations[destination][length]["start"] = " /\n".join(processed_chunks[: min_stops_for_long_story+1])
        destinations[destination][length]["middle"] = ",\n\n".join(processed_chunks[min_stops_for_long_story+1: -2])
        destinations[destination][length]["end"] = " /\n".join(processed_chunks[-2: ])

    # write the processed_chunks_raw to a file.
    cue_file = open(f"cues/{txt_file_name}", "w")
    cue_file.write("\n".join(processed_chunks_raw))

#####




for destination in destinations:
    Destination = destination[:1].upper() + destination[1:]
    object_name = f"SleepStoryTravel{Destination}Cues"
    kt_file_name = f"{object_name}.kt"

    output = f"""// this code is generated from the story files {destination}_{destinations[destination]['short']['timestamp']}_short.txt and {destination}_{destinations[destination]['long']['timestamp']}_long.txt.

// the stops-with-tidbits that went into the user prompts for both of these stories are copied at the bottom as comments -- first those for the short story, then those for the long story -- separated by a bunch of slashes.

// min_stops_for_long_story is set to {min_stops_for_long_story}.

{destinations[destination]["short"]["dedigitization_comment_string"]}

{destinations[destination]["long"]["dedigitization_comment_string"]}

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

    output_file = open(f"code/{kt_file_name}", "w")
    output_file.write(output)
    output_file.close()