##### this takes in a(n edited) story, splits it into cues, and writes these to a `cues` file, separated into chunks by strings.separator.
# or, without an argument, it runs on _all_ stories in `stories/`.

import re

import strings

def make_cues(story_filename = None):

    ###### DEFINE AUXILIARY FUNCTIONS

    ### at this point in the pipeline, the relevant hierarchy is:
        # story > chunk > paragraph > cue > sentence
    ### (the decomposition into completions is no longer relevant.)
    ### however, the order of operations will not be purely outwards-to-inwards, because we must break a paragraph into sentences in order to construct its list of cues.
    ### note too that we ultimately _won't_ care about the breakdown of chunks into paragraphs: these are only relevant for breaking a chunk into cues. (namely, we don't allow a cue to span multiple paragraphs.)

    # this function takes in a story and returns a list of its chunks as well as its metadata
    def story_to_chunks_and_metadata(story_string):
        story_chunks = story_string.split(strings.separator)
        story_metadata = story_chunks.pop()
        return (story_chunks, story_metadata)

    # this function takes in a chunk string and returns a list of its paragraphs.
    def chunk_to_paragraphs(chunk_string):
        # strip away any leading or trailing whitespace.
        string = chunk_string.strip()
        # sometimes chatGPT separates paragraphs by "\n \n" or even "\n  \n", so standardize these.
        string = re.sub(r"\n *\n", "\n\n", string)
        return string.split("\n\n")
    
    # this function takes in a paragraph string and returns a list of cues. (a cue always consists of two sentences if possible, but may also consist of a single dangling sentence at the end of a paragraph (if the paragraph has an odd number of sentences).)
    def paragraph_to_cues(paragraph_string):
        sentences = strings.string_to_sentences(paragraph_string)
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
    
    # on 2023-12-05, we decided to slow down the last handful of sentences, to give more of a feeling of completion as the story wraps up. for this, we'll make the last 4 or 5 sentences be their own individual cues (whichever allows any prior cues in the paragraph where these start to all have two sentences each).
    # rather than worry about how this splits up against the paragraphs (e.g. how many sentences the last paragraph has), let's just implement this as a "post-production" operation on a chunk that has already been convert to a list of cues. (we'll _certainly_ operate under the assumption that there are at least 5 sentences in the chunk, though!)
    # specifically, we'll just make sure that there are _at least_ `min_num_of_one_sentence_cues = 4` one-sentences cues at the end, and this _might_ accidentally cause there to be 5 (which we're fine with).
    def chop_cues_at_end_of_chunk(list_of_cues, min_num_of_one_sentence_cues = 4):
        list_of_cues.reverse()
        output = []
        for cue in list_of_cues:
            if len(output) < min_num_of_one_sentence_cues:
                cue_as_list_of_sentences = strings.string_to_sentences(cue)
                cue_as_list_of_sentences.reverse()
                output += cue_as_list_of_sentences
            else:
                output.append(cue)
        output.reverse()
        return output

    ##### CONVERT STORIES TO CUES FIlES

    if not story_filename:
        story_filenames = strings.get_all_unhidden_files("stories")
        story_filenames.sort()
    else:
        story_filenames = [story_filename]

    for story_filename in story_filenames:
        print(f"converting {story_filename} to a cues file")
        story_string = open(f"stories/{story_filename}", "r").read()
        # adding this here after shipping a putative v1... but why isn't it working in `edit_story.py`???
        story_string = strings.swap_quote_marks(story_string)
        (chunks, metadata) = story_to_chunks_and_metadata(story_string)
        list_of_lists_of_cues = [chunk_to_cues(chunk) for chunk in chunks]
        # split off the last chunk and apply the function chop_cues_at_end_of_chunk, then replace it in list_of_lists_of_cues.
        ending_chunk_as_list_of_cues = list_of_lists_of_cues[-1]
        chopped_ending_chunk_as_list_of_cues = chop_cues_at_end_of_chunk(ending_chunk_as_list_of_cues)
        list_of_lists_of_cues[-1] = chopped_ending_chunk_as_list_of_cues
        chunks_as_cue_strings = ["\n".join(list_of_cues) for list_of_cues in list_of_lists_of_cues]
        cues_string = strings.separator.join(chunks_as_cue_strings + [metadata])
        cues_filename = "cues_" + "_".join(story_filename.split("_")[1:])
        cues_file = strings.open_safe("cues", cues_filename, "w")
        cues_file.write(cues_string)
        cues_file.close()

    return None



### let's make some cues!
# make_cues(...)


# on monday 1/15/2024:
filenames = strings.get_all_unhidden_files("stories")
filenames_today_only = [filename for filename in filenames if filename.split("_")[2] == "2024-01-15"]
filenames_today_only.sort()
for filename in filenames_today_only:
    make_cues(filename)