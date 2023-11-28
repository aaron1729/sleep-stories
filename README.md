# sleep-stories

## setup

### virtual environment

make sure the `openai-env` virtual environment is both loaded and running.
* to load, on the command line in the root of the repo do `python -m venv openai-env`.
* to run, on the command line do `source openai-env/bin/activate` (at least in macOS -- it's slightly different elsewhere).

### openai module

make sure to do `pip install openai`. (i think `pip` only exists once python is installed (e.g. because usually i do `pip3` when i only have `python3` and `pip` doesn't even work). so, be sure to do this _after_ the venv setup above.)

### API key

this ought to have an API key saved (say at the bottom of the file `openai-env/bin/activate`), as explained [here](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key). remember that a terminal window sets the environment variables right when it's opened, so if/when this is updated, open a _new_ terminal window to test the new settings.

### other modules

these should be installed by `pip install`. a (probably incomplete) list of modules used in this repo is:
* `openai` (for chatGPT and dalle),
* `re` (for regex),
* `datetime` (for timestamps),
* `os` (for interacting with the operating system),
* `spacy` (for NLP sentence boundary detection),
* `hashlib` (to hash filenames for replicable psuedorandom binary numbers, to dictate tolerance for "overused words").

## pipeline

here's a description of the pipeline, script by script, in a (topo)logical ordering. see the [pipeline flowchart](sleep_stories_pipeline.pdf) for a visual representation.[^1]

### meta info

#### constants

here are some files that don't (mostly) contain functions.
* `inputs.py` contains info about destinations (including optional info like transport method, requested sightseeing stops, info about the tour guide, and season). every story begins with an entry here.
* `strings.py` contains some strings and string-writing functions (e.g. chatGPT prompts that depend on `destination` and `length`(-of-story) parameters).
* `models.py` contains global choices for `gpt_model` and `image_model` (currently set to `gpt-4-1106-preview` and `dall-e-3`, respectively).

#### other info

filenames are generally of the form `{filetype}_{destination}_{timestamp}[_{length}].ending`. here, `destination` is e.g. `costarica` and `length` is always either `short` or `long`. an exception is `art-styles_{timestamp}.txt` (since these are each generally associated to many different destinations).

#### misc to-do (not including stuff below)

- [ ] make sure to adhere to above format when writing code that creates new filenames.
- [x] make sure to use `strings.separator` everywhere instead of `"\n\n=====\n\n"`.
- [ ] keep `sleep_stories_pipeline.pdf` up-to-date.

### get_stops.py

this takes in a destination (listed in `inputs.py`), gets a list of (by default 20) stops along with tidbits about them, and writes it all to a `stops` file in `stops/`.

a typical result file is named `stops_berkeley_2023-11-23_02-25-23.txt`.

STATUS: done.

### write_story.py

this takes a length (either `short` or `long`), a destination, a `num_stops_parameter` (explained in the code), and a corresponding `stops` file (by default the most recent one for that destination), and writes a story. the code applies to both short and long stories simultaneously, but the actual writing prompts that we feed to chatGPT are rather different. this writes to a `story-unedited` file in `stories-unedited`.

a typical result file is named `story-unedited_berkeley_2023-11-24_17-25-36_short.txt`.

a `story-unedited` file is separated into "chunks", the last simply containing the metadata of which `stops` file the story was written based on.

for long stories, each chunk (aside from the last one) is a single chatGPT completion. but for short stories, in order to make the chunks themselves shorter, the middle completions are actually broken up into multiple chunks. (this is the purpose of having the parameter `n`; completions tend to be around 500-800 words, regardless of how many stops are given in the user prompt.)

if chatGPT ever fails to return the correct number of chunks in a middle completion, this is logged at the bottom of `logs/splitting_failure_log.txt`.

STATUS: done.

### edit_story.py

this takes an unedited story and attempts to edit out:
* digits (so that the ElevenLabs AI voice makes no mistake in pronouncing e.g. `"1950"` (depending on the context!)),
* roman numerals (likewise), and
* words that are overused by chatGPT (e.g. `"tapestry"`),

running chunk by chunk. this writes to `stories/`.[^2]






in this file, the final chunk now also contains the metadata of the "sentence replacement pairs", i.e. the pairs of an old sentence that was editing as well as the new sentence that replaced it.

a typical result file is named `story_berkeley_2023-11-24_17-25-36_short.txt`. the timestamp corresponds to the original writing time, not the editing time.

STATUS: not yet written, but will be based on existing stuff.

### make_cues.py

`DESCRIPTION & STATUS HERE` (this will be extracted from `process.py`)

### phoneticize_cues.py

`UPDATE DESCRIPTION & STATUS` (this will be new)

`UPDATED ARCHITECTURE (monday 3pm):`
* make a list of foreign words etc., one for each story cue file
* delete duplicates
* get phoneticizations from chatGPT for all of them
* later, when doing the "replace", be sure to run from longest to shortest, so that we never accidentally do a replacement for a substring and then miss the larger one.
* make sure chatGPT only gives _one_ pronunciation. sometimes it gives two. ask for "whichever is most common."
* when getting a pronunciation, make sure to ask: "in the context of the above story, ..." (or just pluck out the sentence/paragraph(s) where it appears).
* and "any words that are _even remotely_ possible to mispronounce, e.g. 'pergola'". for this, chatGPT suggests the prompt:
> Please review the following story and identify any words or terms that may be foreign, technical, proper nouns, or have pronunciations that are not immediately obvious. Include words that might be challenging to pronounce for readers who are not familiar with them, especially those of foreign origin, unique regional names, or specialized jargon. 

this takes a(n edited) story, asks chatGPT for a list of proper nouns, foreign words, or any other words/phrases that might be hard to pronounce (for an ElevenLabs AI voice), and then asks chatGPT for pronunciations of them one-by-one (in terms of the IPA) and replaces those in the story.

STATUS: not yet written at all (but tested in chatGPT and it seems to be a fine way to proceed). REMAINING QUESTION: how to ensure that we _exactly_ phoneticize everything that we should? for instance, maybe a word is actually pluralized. of course we can ask chatGPT to return the _exact_ matches throughout the story, and give an example to illustrate. and then when we search through the story, of course do so case-insensitively. we can also save the replacements as metadata.

### make_kt.py

`UPDATE DESCRIPTION & STATUS` (this will be extracted from `process.py`)

#### UPDATE: peel off `write_cues.py` from this, move it above "phoneticize"

this takes a pair of a short story and a long story set in the same destination, and generates both a single `.kt` file in `code/` as well as a pair of files in `cues/` that just contain the unadorned cues (for later usage in generating dalle prompts). we use the `spacy` NLP module to detect sentence boundaries (which seems to be much more robust (and convenient!) than using regex since then we'd have to watch out for abbreviations (which are typically followed by a period, e.g. `"Mt. Tamalpais"` or `"e.g."`)).

a typical `.kt` file is named `SleepStoryTravelBerkeleyCues.kt`. a typical cues file is named `cues_berkeley_2023-11-24_17-25-36_short.txt` (again timestamped by the original writing time).

STATUS: done. NO, actually update it to take in a PHONETICIZED story. but the `cues` should be non-phoneticized. so, some more refactoring is in order (as of sunday at around 9pm). really, we should be able to make a `cue` file based on just a single story; it doesn't need to be a short/long pair.

### get_art_styles.py

this takes a list of destinations in `inputs.py` and generates a list of styles of art that their stories can be illustrated in, along with a detailed description of the art style.

a typical result file is named `give one here: prob just art-styles_2023-11-23.txt`.

STATUS: does not yet exist. (we've been doing this part manually thus far.) this might begin with just a list (say comma-separated) of the locations that appear in this file.

### get_dalle_prompts.py

this takes a list of unadorned cues (in `cues/`) from a story as well as a list of art styles (by default the most recently written one) and generates one dalle prompt for each cue in the given style.

a typical result file is named `decide here. prob put timestamp, and then metadata of what story it came from.`

STATUS: the `for` loop exists, but as of now (11/26 at 4pm) the art style is hard-coded.

### get_pix.py

this takes a list of dalle prompts for a given story and generates illustrations.

`this should land in a dedicated folder, indicating the timestamps of: the story, the dalle-prompts file, and generation time. in particular, this should take as a parameter both the story and a dalle-prompts file that's based on it.`

STATUS: the `for` loop (over the list of dalle prompts) exists, but it's not a function yet.

[^1]: note to self: this must be _manually_ copied from the notability folder in dropbox. (unfortunately (though very believably), it doesn't work to just put an alias in the git folder.)

[^2]: actually, we do want to allow chatGPT to _occasionally_ use an "overused word". so, for each overused word, we choose either 0 or 1 and then allow that many instances to remain in the story. (for replicability, this is done by hashing the filename of the unedited story down to a binary number, and then running through its digits and assigning those. (this gives 256 bits, so in practice we should never run out -- but if we did, we could just rotate back through.)) to keep things simple, we just take this number as a counter and decrement it each time we encounter the word, and then require it to be removed when the counter is 0. of course, we search e.g. for `"tapestr"` case-insensitively, so that we catch both plural instances as well as instances at the beginning of a sentence. and if a single chunk ever has two or more instances of e.g. `"tapestr"`, then we just tell it to edit them _all_ out but keep the counter unchanged.