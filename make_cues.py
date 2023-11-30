##### this takes in a(n edited) story, splits it into cues, and writes these to a `cues` file, separated into chunks by strings.separator.
# or, without an argument, it runs on _all_ stories in `stories/`.

import re

import spacy
nlp = spacy.load("en_core_web_sm")

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

    ##### CONVERT STORIES TO CUES FIlES

    if not story_filename:
        story_filenames = strings.get_all_unhidden_files("stories")
        story_filenames.sort()
    else:
        story_filenames = [story_filename]

    for story_filename in story_filenames:
        print(f"converting {story_filename} to a cues file")
        story_string = open(f"stories/{story_filename}", "r").read()
        (chunks, metadata) = story_to_chunks_and_metadata(story_string)
        list_of_lists_of_cues = [chunk_to_cues(chunk) for chunk in chunks]
        chunks_as_cue_strings = ["\n".join(list_of_cues) for list_of_cues in list_of_lists_of_cues]
        cues_string = strings.separator.join(chunks_as_cue_strings + [metadata])
        cues_filename = "cues_" + "_".join(story_filename.split("_")[1:])
        cues_file = open(f"cues/{cues_filename}", "w")
        cues_file.write(cues_string)
        cues_file.close()

    return None



### let's make some cues!

make_cues()
# make_cues("story_chiangmai_2023-11-28_21-23-16_long.txt")
# make_cues("story_chiangmai_2023-11-26_20-26-02_short.txt")