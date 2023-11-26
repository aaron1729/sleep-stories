##### this code takes in a _pair_ of stories (one long and one short) set in the same location `destination`, and creates:
    ##### a kotlin file SleepStory{Destination}Cues.kt in `code/``, and
    ##### a text pair of text files cues_{destination}_{timestamp}_{length}.txt in `cues/`.

import re # regular expressions

# this NLP tool detects sentence boundaries.
import spacy
nlp = spacy.load("en_core_web_sm")

import strings # so, `my_string` defined over there is accessible here as `strings.my_string`.

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
    ### note too that we ultimately _won't_ care about the breakdown of chunks into paragraphs: these are only relevant for breaking a chunk into cues. (namely, we don't allow a cue to span multiple paragraphs.)

    # this function takes in a chunk string and returns a list of its paragraphs.
    def chunk_to_paragraphs(chunk_string):
        # strip away any leading or trailing whitespace.
        string = chunk_string.strip()
        # sometimes chatGPT separates paragraphs by "\n \n" or even "\n  \n", so standardize these.
        string = re.sub(r"\n *\n", "\n\n", string)
        return string.split("\n\n")
    
    # this function takes in a paragraph string and returns a list of its sentences (using the `spacy` NLP module).
    def paragraph_to_sentences(paragraph_string):
        doc = nlp(paragraph_string)
        return [sentence.text for sentence in doc.sents]
    
    # this function takes in a paragraph string and returns a list of cues. (a cue always consists of two sentences if possible, but may also consist of a single dangling sentence at the end of a paragraph (if the paragraph has an odd number of sentences).)
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
    
    # this function formats a list of cues into a single string of kotlin code.
    # (it will _not_ necessarily always be a single chunk; for instance, in writing a long story, we'll always attach the last stop's chunk to the end chunk for the `end` of the story.)
    # (down dog linting uses 2 spaces per tab, and the cue strings will be indented by 2 tabs.)
    def format_list_of_cues(list_of_cues):
        list_of_indented_and_quoted_cues = [f"    \"{cue_string}\"" for cue_string in list_of_cues]
        return " /\n".join(list_of_indented_and_quoted_cues)

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
        # henceforth, the metadata has been popped away from the list of chunks. (this is why there's no function story_to_chunks defined above.)

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
        print(f"finished writing the cues file {stories[length]['cues_filename']}")
        
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
        stops_files_info_string = kotlin_comment(f"in turn, these stories are both generated from the single stops file {stories['long']['stops_filename']}, which is copied (commented-out) at the bottom of this file (after a bunch of slashes).")
        stops_string = f"""/*

////////////////////////////////////////////////////////////////////////////////

{stories['long']['stops_string']}

*/"""
    else:
        stops_files_info_string = kotlin_comment(f"in turn, the short story is generated from the stops file {stories['short']['stops_filename']}, while the long story is generated from the stops file {stories['long']['stops_filename']}. these stops files are both copied (commented-out) at the bottom of this file as comments (after a bunch of slashes and separated by a bunch of slashes), in that order.")
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

    print(f"finished processing the stories {stories['short']['story_filename']} and {stories['long']['story_filename']} into a single kotlin file")

    return None



process_story_pair("berkeley")