##### this code only runs if in the stories (saved in 'stories/') come in long/short pairs!

import re # regular expressions

# this NLP tool detects sentence boundaries.
import spacy
nlp = spacy.load("en_core_web_sm")

import strings # so, `my_string` defined over there is accessible here as `strings.my_string`.



#### IS THIS STUFF STILL USED HERE???
from os import listdir # operating system; list the files in a directory
from os.path import isfile, join
txt_file_names_incl_hidden = [f for f in listdir("stories/") if isfile(join("stories/", f))]
txt_file_names = [file_name for file_name in txt_file_names_incl_hidden if file_name[0] != "."]
txt_file_names.sort() # make alphabetical, for reproduceability.



# take a (generally multi-line) string and prepend each line with `// ` (so that it becomes a comment in kotlin).
def kotlin_comment(string):
    lines = string.split("\n")
    commented_lines = ["// " + line for line in lines]
    comment = "\n".join(commented_lines)
    return comment




# destination is e.g. "costarica"
# long_story_filename is e.g. "story_berkeley_2023-11-24_17-05-55_long.txt", and similar for short_story_filename; if either of these is left as `None`, we automatically retrieve the most recent long/short story set in `destination`.
# when writing a long story, we _always_ roll the last stop into the `end` of the story. so, min_stops_for_long_story is one more than the number of stops rolled into the `start` of the story.
def process_story_pair(destination, long_story_filename = None, short_story_filename = None, min_stops_for_long_story = 1):

    print(f"processing a pair of stories with destination: {destination}")

    ###### DEFINE AUXILIARY FUNCTIONS

    ### here we split a chunk into cues. the hierarchy is:
        # story
            # chunk
                # paragraph
                    # cue
                        # sentence
    ### (we will have already split the story into chunks in order to pop off the last one, which contains its metadata.)
    ### however, the order of operations will not be purely outwards-to-inwards, because we must break a paragraph into sentences in order to construct its list of cues.
    ### note too that we ultimately _won't_ care about the breakdown of chunks into paragraphs: these are only relevant for breaking a chunk into cues. (namely, we _don't_ allow a cue to span multiple paragraphs.)

    # this function takes in a chunk string (which is split into paragraphs by chatGPT) and returns a list of paragraphs.
    def chunk_to_paragraphs(chunk_string):
        # strip away any leading or trailing whitespace.
        string = chunk_string.strip()
        # sometimes chatGPT separates paragraphs by "\n \n" or even "\n  \n", so standardize these.
        string = re.sub(r"\n *\n", "\n\n", string)
        return string.split("\n\n")
    
    # this function takes in a paragraph string and returns a list of sentences (using the `spacy` NLP module).
    def paragraph_to_sentences(paragraph_string):
        doc = nlp(paragraph_string)
        return [sentence.text for sentence in doc.sents]
    
    # this function takes in a paragraph string and returns a list of cues. (a cue always consists of two sentences if possible, except for possibly a dangling sentence at the end of a paragraph (if it has an odd number of sentences).)
    def paragraph_to_cues(paragraph_string):
        sentences = paragraph_to_sentences(paragraph_string)
        num_full_cues = len(sentences) // 2
        cues = []
        for i in range(num_full_cues):
            cues.append(sentences[2*i] + " " + sentences[2*i+1])
        if len(sentences) % 2 == 1:
            cues.append(sentences[-1])
        return cues

    # this function concatenates two above functions: it takes in a chunk and returns a list of cues.
    def chunk_to_cues(chunk_string):
        list_of_paragraphs = chunk_to_paragraphs(chunk_string)
        list_of_cues = []
        for paragraph_string in list_of_paragraphs:
            list_of_cues += paragraph_to_cues(paragraph_string)
        return list_of_cues

    ### here we define functions that process strings into kotlin code.

    # we use double-quotes in our kotlin code to delineate cues, so this function replaces those with single-quotes.
    def swap_quote_marks(string):
        return re.sub("\"", "'", string)
    
    # this function takes a (generally multi-line) string and prepend each line with `// ` (so that it becomes a comment in kotlin).
    def kotlin_comment(string):
        lines = string.split("\n")
        commented_lines = ["// " + line for line in lines]
        comment = "\n".join(commented_lines)
        return comment
    
    # this formats a list of cues into a single string of kotlin code.
    # (it will _not_ necessarily always be a single chunk, because e.g. in writing a long story we'll always attach the last stop's chunk to the end chunk for the `end` of the story.)
    # (down dog linting uses 2 spaces per tab, and the cue strings will be indented by 2 tabs.)
    def format_list_of_cues(list_of_cues):
        list_of_indented_and_quoted_cues = [f"    \"{cue_string}\"" for cue_string in list_of_cues]
        return " /\n".join(list_of_indented_and_quoted_cues)
    









    ##### OLD STUFF

    # # a chunk consists of paragraphs, and a paragraph consists of sentences. this takes in a chunk and returns a list of lists: each sub-list is the list of sentences in the corresponding paragraph.
    # def chunk_to_sentences(string):
    #     # strip away any leading or trailing whitespace.
    #     string = string.strip()
    #     # sometimes chatGPT separates paragraphs by "\n \n" or even "\n  \n", so standardize these.
    #     string = re.sub(r"\n *\n", "\n\n", string)
    #     # we'll later wrap cues in double-quotes, so first replace these.
    #     string = re.sub("\"", "'", string)
    #     paragraphs = string.split("\n\n")
    #     # again, strip away any leading or trailing whitespace.
    #     paragraphs = [paragraph.strip() for paragraph in paragraphs]
    #     # split paragraphs into sentences, using the `spacy` module.
    #     paragraphs_of_sentences = []
    #     for paragraph in paragraphs:
    #         doc = nlp(paragraph)
    #         paragraph_of_sentences = [sentence.text for sentence in doc.sents]
    #         paragraphs_of_sentences.append(paragraph_of_sentences)
    #     return paragraphs_of_sentences
    
    # # via the function chunk_to_sentences, each paragraph becomes saved as a list of strings. the following function turns these into cues, which each consist of two sentences except for possibly a dangling sentence at the end of a paragraph.
    # def paragraph_to_cues(sentences):
    #     num_full_cues = len(sentences) // 2
    #     cues = []
    #     for i in range(num_full_cues):
    #         cues.append(sentences[2*i] + " " + sentences[2*i+1])
    #     if len(sentences) % 2 == 1:
    #         cues.append(sentences[-1])
    #     return cues
    
    # # this function combines the two above functions, and takes a chunk (a string) to a list of lists of cues: each sub-list is the list of cues from the corresponding paragraph.
    # def chunk_to_cues(string):
    #     return [paragraph_to_cues(sentences) for sentences in chunk_to_sentences(string)]
    








    ###### PROCESS THE STORIES

    stories = {
        "long": {
            "story_filename": long_story_filename
        },
        "short": {
            "story_filename": short_story_filename
        }}
    
    # get data and metadata
    
    for length in stories:
        
        if not stories[length]["story_filename"]:
            stories[length]["story_filename"] = strings.get_latest_filename(destination, "stories", length)
        stories[length]["story_string"] = open(f"stories/{stories[length]['story_filename']}", "r").read()
        stories[length]["chunks"] = stories[length]["story_string"].split("\n\n=====\n\n")
        stories[length]["metadata"] = stories[length]["chunks"].pop()
        # henceforth, the metadata has been popped away from the list of chunks. (in order to do this, we need to split the story_string into chunks.)

        ### now, get the cues and process them both into raw cue strings and into the start/middle/end strings for kotlin.

        # make a list of lists of cues (each sub-list corresponding to a single chunk of the story).
        stories[length]["list_of_lists_of_cues"] = [chunk_to_cues(chunk_string) for chunk_string in stories[length]["chunks"]]

        # create the raw cues string and write it to a cues file.
        stories[length]["raw_cues_string"] = "\n".join(["\n".join(chunk_as_list_of_cues) for chunk_as_list_of_cues in stories[length]["list_of_lists_of_cues"]])
        # print("raw cues string is:\n", stories[length]["raw_cues_string"])
        stories[length]["cues_filename"] = "cues" + stories[length]["story_filename"][5: ]
        cues_file = open(f"cues/{stories[length]['cues_filename']}", "w")
        cues_file.write(stories[length]['raw_cues_string'])
        cues_file.close()
        
        # create the `start`, `middle`, and `end` strings for the kotlin file.
        if length == "long":
            index_between_start_and_middle = min_stops_for_long_story
            index_between_middle_and_end = -2
        else:
            index_between_start_and_middle = 1
            index_between_middle_and_end = -1
        # these are lists of lists of cue strings.
        start_chunks = stories[length]["list_of_lists_of_cues"][: index_between_start_and_middle]
        middle_chunks = stories[length]["list_of_lists_of_cues"][index_between_start_and_middle: index_between_middle_and_end]
        end_chunks = stories[length]["list_of_lists_of_cues"][index_between_middle_and_end: ]
        # make the start string.
        list_of_start_cues = sum(start_chunks, [])
        stories[length]["start"] = format_list_of_cues(list_of_start_cues)
        # make the middle string.
        middle_chunks_formatted = [format_list_of_cues(middle_chunk) for middle_chunk in middle_chunks]
        stories[length]["middle"] = ",\n\n".join(middle_chunks_formatted)
        # make the end string.
        list_of_end_cues = sum(end_chunks, [])
        stories[length]["end"] = format_list_of_cues(list_of_end_cues)
        # print(f"length is {length} and `start` is:\n", stories[length]["start"])
        # print(f"length is {length} and `middle` is:\n", stories[length]["middle"])
        # print(f"length is {length} and `end` is:\n", stories[length]["end"])

        # get the stops filename and string.
        stories[length]["stops_filename"] = stories[length]["metadata"].split("\n")[0].split(" ")[-1]
        stories[length]["stops_string"] = open(f"stops/{stories[length]['stops_filename']}", "r").read()

        # get the list of replaced sentences.
        stories[length]["replaced_sentences"] = "\n".join(stories[length]["metadata"].split("\n")[2:])
    
    ### now (outside of the `for` loop), do stuff that involves both stories simultaneously.
    
    # check if stops files are the same.
    if stories["long"]["stops_filename"] == stories["short"]["stops_filename"]:
        same_stops_filenames = True
    else:
        same_stops_filenames = False
    
    # write the kotlin file.

    stories_files_string = kotlin_comment(f"this code is generated from the story files {stories['short']['story_filename']} and {stories['long']['story_filename']}.")
    if same_stops_filenames:
        stops_files_info_string = kotlin_comment(f"these stories are both generated from the stops file {stories['long']['stops_filename']}, which is copied (commented-out) at the bottom of this file (after a bunch of slashes).")
        stops_string = f"""/*

////////////////////////////////////////////////////////////////////////////////

{stories['long']['stops_string']}

*/"""
    else:
        stops_files_info_string = kotlin_comment(f"the short story is generated from the stops file {stories['short']['stops_filename']}, while the long story is generated from the stops file {stories['long']['stops_filename']}. these are both copied (commented-out) at the bottom of this file as comments (after a bunch of slashes and separated by a bunch of slashes), in that order.")
        stops_string = f"""/*

////////////////////////////////////////////////////////////////////////////////

{stories['short']['stops_string']}

////////////////////////////////////////////////////////////////////////////////

{stories['long']['stops_string']}

*/"""
    min_stops_for_long_story_string = kotlin_comment(f"min_stops_for_long_story is set to {min_stops_for_long_story}.")
    short_story_replaced_sentences_string = kotlin_comment(f"SHORT STORY REPLACED SENTENCES:\n\n{stories['short']['replaced_sentences']}")
    long_story_replaced_sentences_string = kotlin_comment(f"LONG STORY REPLACED SENTENCES:\n\n{stories['long']['replaced_sentences']}")
    Destination = destination[: 1].upper() + destination[1: ]
    object_name = f"SleepStoryTravel{Destination}Cues"
    kotlin_filename = f"{object_name}.kt"

    kotlin_string = f"""{stories_files_string}

{stops_files_info_string}

{min_stops_for_long_story_string}

{short_story_replaced_sentences_string}

{long_story_replaced_sentences_string}

package com.downdogapp.cue

object {object_name} : SleepStoryPoseCues {{

  override val startShort =
{stories['short']['start']}

  override val middleShort = listOf(
{stories['short']['middle']}
)

  override val endShort =
{stories['short']['end']}

  override val start =
{stories['long']['start']}

  override val middle = listOf(
{stories['long']['middle']}
)

  override val end =
{stories['long']['end']}

}}

{stops_string}"""

    kotlin_file = open(f"code/{kotlin_filename}", "w")
    kotlin_file.write(kotlin_string)
    kotlin_file.close()

    return None











process_story_pair("berkeley")



















# # this is a dict, whose keys are destinations.
#     # the value of each destination is itself a dict, with the keys "short" and "long".
#         # the values of those are _also_ dicts, each of which has keys:
#             # "timestamp"
#             # "stops_with_tidbits"
#             # "dedigitization_comment_string"
#             # "start"
#             # "middle"
#             # "end"
# destinations = {}

# min_stops_for_long_story = 1

# for txt_file_name in txt_file_names:

#     print(f"now processing {txt_file_name}")

#     [destination, date, time, length] = txt_file_name[:-4].split("_")
#     if not destination in destinations:
#         destinations[destination] = {}
#     destinations[destination][length] = {}
#     timestamp = f"{date}_{time}"
#     destinations[destination][length]["timestamp"] = timestamp
    
#     #####

#     story_string = open(f"stories/{destination}_{timestamp}_{length}.txt", "r").read()
    
#     # retrieve the "stops with tidbits" info; this gets saved as comments at the bottom of the kotlin file, for easy reference.
#     destinations[destination][length]["stops_with_tidbits"] = open(f"stops_with_tidbits/{destination}_{timestamp}.txt", "r").read()
    
#     # this is a list of strings. each string is a single full response from chatGPT, except for the last one which is just a record of the strings that used to contain digits but were (hopefully) replaced with ones that do not.
#     chunks = story_string.split("=====")

#     # the last entry of the `chunks` list contains the dedigitization metadata. peel this off and save it.
#     dedigitization_string = chunks[-1]
#     dedigitization_string = f"{length.upper()}_STORY_{dedigitization_string.strip()}"
#     dedigitization_lines = dedigitization_string.split("\n")
#     dedigitization_lines_with_slashes = [f"// {dedigitization_line}" for dedigitization_line in dedigitization_lines]
#     dedigitization_comment_string = "\n".join(dedigitization_lines_with_slashes)
#     destinations[destination][length]["dedigitization_comment_string"] = dedigitization_comment_string
#     chunks = chunks[: -1]

#     ##### COMMENTS ON THE FUNCTION process_chunk BELOW...

#     ##### FURTHER UPDATE (2023-11-20): a "minibatch" here is what's later in the pipeline called a "cue" (as in "yoga cue"). we'll be associating a dall-e prompt, and thereafter an image, to each minibatch. so to do that, we'll want to save the raw minibatches (without quote-marks) in a file, in `cues`. these are separated by `\n`.
    
#     ##### NEW VERSION (2023-11-15): split each _paragraph_ into minibatches -- two sentences each, and if there are an odd number then the last one on its own. so for a 3-sentence paragraph followed by a 4-sentence paragraph, we want:
#         # "pgh1 minibatch 1" /
#         # "pgh1 minibatch 2" /
#         # "pgh2 minibatch 1" / ....
#     # the commas will _only_ be in the same spot: separating the `listOf` arguments in the middle val thingy.

#     ##### ORIGINAL VERSION: this function takes a chunk and breaks it into paragraphs, and then organizes those into a single (but generally multi-line) string like the following (with two tabs before each paragraph, to conform to linting style):
#         # "1st paragraph of the 3-paragraph chunk" /
#         # "2nd paragraph of the 3-paragraph chunk" /
#         # "3rd paragraph of the 3-paragraph chunk"
        
#     def process_chunk(string):
#         string = string.strip()
#         # chunks consist of paragraphs. usually the paragraphs are separated by "\n\n", but occasionally chatGPT separates them with "\n \n", or possibly even "\n  \n" (with two spaces). so, fix this.
#         string_with_fixed_paragraph_separations = re.sub(r'\n *\n', '\n\n', string)
#         paragraphs = string_with_fixed_paragraph_separations.split("\n\n")
#         minibatches = []
#         minibatches_raw = []
#         for paragraph in paragraphs:
#             # we'll later wrap minibatches in double-quotes, so first replace these.
#             paragraph_replaced = paragraph.replace("\"", "'")
#             # split into sentences. beware that these can end with a period, exclamation point, or question mark. there can be a quote-mark or two, too.
#             pattern_for_sentence_ending = r"([!\.\?]{1,4}'{0,2})\s+"
#             paragraph_stripped = paragraph_replaced.strip()
#             sentences_and_punctuations = re.split(pattern_for_sentence_ending, paragraph_stripped)
#             # for whatever reason, the above seems to split _some_ periods away from their preceding sentences, but not all. so, put them together manually.
#             sentences = []
#             for shortstring in sentences_and_punctuations:
#                 # the check that `len(shortstring) > 4` is supposed to ensure that we're looking at an actual sentence, instead of just e.g. some funky punctuation in and around a period at the end of a sentence (e.g. some quotation marks).
#                 # however, there was an error in processing `queenstown_2023-11-21_18-59-20_short.txt` since an entire paragraph starts with `Mt. Nicholas Station, a historic icon` and so there was nowhere for the `Mt.` to get appended to in the `else` block. so if there are no sentences yet, then we'll just kick things off with `shortstring` no matter how short it is.
#                 if len(shortstring) > 4 or len(sentences) == 0:
#                     sentences.append(shortstring)
#                 else:
#                     sentences[len(sentences)-1] += shortstring
#             num_full_minibatches = len(sentences) // 2
#             # use 4 spaces here -- down dog linting is 2 spaces per tab, and this is indented by 2 tabs.
#             for i in range(num_full_minibatches):
#                 minibatch = f"    \"{sentences[2*i]} {sentences[2*i+1]}\""
#                 minibatch_raw = sentences[2*i] + " " + sentences[2*i+1]
#                 minibatches.append(minibatch)
#                 minibatches_raw.append(minibatch_raw)
#             if len(sentences) % 2 == 1:
#                 minibatch = f"    \"{sentences[-1]}\""
#                 minibatch_raw = sentences[-1]
#                 minibatches.append(minibatch)
#                 minibatches_raw.append(minibatch_raw)
#         return " /\n".join(minibatches), "\n".join(minibatches_raw)

#     processed_chunks = []
#     processed_chunks_raw = []
#     for chunk in chunks:
#         processed_chunk, processed_chunk_raw = process_chunk(chunk)
#         processed_chunks.append(processed_chunk)
#         processed_chunks_raw.append(processed_chunk_raw)

#     # store the processed_chunks for later integration into a single kt file containing both a short story and a long story.

#     if length == "short":
#         destinations[destination][length]["start"] = " /\n".join(processed_chunks[: 1])
#         destinations[destination][length]["middle"] = ",\n\n".join(processed_chunks[1: -1])
#         destinations[destination][length]["end"] = " /\n".join(processed_chunks[-1: ])

#     if length == "long":
#         destinations[destination][length]["start"] = " /\n".join(processed_chunks[: min_stops_for_long_story+1])
#         destinations[destination][length]["middle"] = ",\n\n".join(processed_chunks[min_stops_for_long_story+1: -2])
#         destinations[destination][length]["end"] = " /\n".join(processed_chunks[-2: ])

#     # write the processed_chunks_raw to a file.
#     cue_file = open(f"cues/{txt_file_name}", "w")
#     cue_file.write("\n".join(processed_chunks_raw))

# #####




# for destination in destinations:
#     Destination = destination[:1].upper() + destination[1:]
#     object_name = f"SleepStoryTravel{Destination}Cues"
#     kt_file_name = f"{object_name}.kt"

#     output = f"""// this code is generated from the story files {destination}_{destinations[destination]['short']['timestamp']}_short.txt and {destination}_{destinations[destination]['long']['timestamp']}_long.txt.

# // the stops-with-tidbits that went into the user prompts for both of these stories are copied at the bottom as comments -- first those for the short story, then those for the long story -- separated by a bunch of slashes.

# // min_stops_for_long_story (the number of stops rolled into the 'start' for the long story) is set to {min_stops_for_long_story}.

# {destinations[destination]["short"]["dedigitization_comment_string"]}

# {destinations[destination]["long"]["dedigitization_comment_string"]}

# package com.downdogapp.cue

# object {object_name} : SleepStoryPoseCues {{

#   override val startShort =
# {destinations[destination]["short"]["start"]}

#   override val middleShort = listOf(
# {destinations[destination]["short"]["middle"]}
# )

#   override val endShort =
# {destinations[destination]["short"]["end"]}

#   override val start =
# {destinations[destination]["long"]["start"]}

#   override val middle = listOf(
# {destinations[destination]["long"]["middle"]}
# )

#   override val end =
# {destinations[destination]["long"]["end"]}

# /*

# ////////////////////////////////////////////////////////////////////////////////

# {destinations[destination]["short"]["stops_with_tidbits"]}

# ////////////////////////////////////////////////////////////////////////////////

# {destinations[destination]["long"]["stops_with_tidbits"]}

# */

# }}"""

#     output_file = open(f"code/{kt_file_name}", "w")
#     output_file.write(output)
#     output_file.close()