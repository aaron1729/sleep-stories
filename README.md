# sleep-stories

## setup

### virtual environment

make sure the `openai-env` virtual environment is both loaded and running.
* to load it, on the command line in the root of the repo do `python -m venv openai-env`.
* to run it, on the command line in the root of the repo do `source openai-env/bin/activate` (at least in macOS -- it's slightly different elsewhere, as explained [here](https://platform.openai.com/docs/quickstart/step-1-setup-python)).

### openai module

make sure to do `pip install openai`, _after_ the virtual environment is set up (so that the module lives in it).

### API key

make sure to incorporate an API key (say at the bottom of the file `openai-env/bin/activate`), as explained [here](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key). (of course, `openai-env/` is in `.gitignore`, so that this isn't exposed (even though the repo is private -- just for further security).) remember that a terminal window retrieves the environment variables right when it's opened; so, if/when the API key is updated, open a _new_ terminal window to use it.

### other modules

these should be installed by `pip install`. a (probably incomplete) list of modules used in this repo is:
* `datetime` (for timestamps),
* `hashlib` (to hash filenames for replicable psuedorandom binary numbers, to dictate tolerance for "overused words"),
* `openai` (for chatGPT and dalle),
* `os` (for interacting with the operating system, e.g. making directories and reading their contents),
* `re` (for regex),
* `requests` (to make GET requests for an image after dalle has created it and returned its url).
* `spacy` (for NLP sentence boundary detection),

## pipeline

here's a description of the pipeline, script by script, in a (topo)logical ordering. see the [pipeline flowchart](sleep_stories_pipeline.pdf) for a visual representation. from the root, `my_script.py` is executed by doing `python my_script.py` on the command line (with the virtual environment running).

### miscellaneous info

#### story organization

each story is decomposed according to the hierarchy

    story > completion > chunk > stop > paragraph > cue > sentence

as explained presently.

the word "cue" is reused from the yoga practice pipeline. a cue consists of either one or two sentences; more specifically, each paragraph is split into cues, and each cue is two sentences long except for possibly the last cue in a paragraph (if the paragraph has an odd number of sentences). this separation makes the ElevenLabs voice sound more relaxed. in the `kt` files, cues are surrounded by double-quotes (`"`), and the cues within a chunk are separated by slashes (`/`).

the "chunk" decomposition of a story is so that we can serve varying lengths of stories: in each `kt` file, the initial chunk comprises the `start` component, the final chunk comprises the `end` component, and the chunks in between them comprise the list of `middle` components (and they are separated by commas (`,`)). a story is always served with `start` and `end` components, as well as the first `x` middle components for some `x>=0` depending on the desired length. of course, the stories are written so that the story is always coherent regardless of the value of `x`. (actually, there is the possibility that the conclusion of the story (in the `end` component) refers to sightseeing locations that may or may not have actually been served, but we've decided to ignore this for the time being.)

a "stop" is a sightseeing location. (given a destination, these as well as tidbits about them are retrieved in `get_stops.py`.) typically, chatGPT begins a new paragraph whenever it moves on to a new stop.

a "completion" is a single response from chatGPT. for long stories, each (middle) completion constitutes a chunk, and corresponds to a single stop. for short stories, each (middle) completion is broken down into `n` stops (where `n` is an argument in the `write_story` function, and is currently by default set to `2`), and then it is broken down into chunks -- one for each stop. (this is so that the chunks themselves are shorter, since chatGPT tends to have a relatively stable completion length (in the neighborhood of 600-800 words) regardless of how many stops are listed in the user prompt.)

#### run times

waiting for chatGPT (and dalle) response is the main bottleneck in this process. here are some approximate run times, although it seems that chatGPT occasionally hangs and makes these much longer.
* get 20 stops for a stops file: `[fill this in -- probably on the order of 3min per stops file]`
* write a story: 6.5min for long (with 20 stops), 4.5min for short (with (a,c,n,z) = (1,5,2,1)).
* edit a story: 4-7min (and rather variable -- not even really correlated with the `length` of the story). `[or maybe far, far less after removing the roman numerals regex?!]` AND NOW (~dec 2): `without any roman numerals stuff, 2-3.5min!` but probably we'll add that back in...
* make cues: <1sec per cues file.
* make kt: <0.1sec per kt file.
* get art style description: 30-40sec each.
* get dalle prompts: 6-10sec per prompt.
* get images: 20-25sec each (with `size="1024x1792"` and `quality="standard"`).

#### constants

here are some files that don't (mostly) contain functions.
* `inputs.py` contains info about destinations (including optional info like transport method, requested sightseeing locations, info about the tour guide, and season). every story begins with an entry here. this is generally imported as `from inputs import *`, so that `my_input` defined over there is accessible as `my_input`.
* `strings.py` contains some strings and string-writing functions (e.g. chatGPT prompts that depend on `destination` and `length`(-of-story) parameters). this is generally imported as `import strings`, so that `my_string` defined over there is accessible as `strings.my_string`.
* `models.py` contains global choices for `gpt_model` and `image_model` (currently set to `gpt-4-1106-preview` and `dall-e-3`, respectively). this is generally imported as `import models`, so that `my_model` defined over there is accessible as `models.my_model`.

#### naming conventions

most filenames are of the form `{filetype}_{destination}_{timestamp}[_{length}].ending`. note that the `timestamp` is itself `_`-separated. here, the convention is that fields can be used both to describe type (e.g. to say what type of file this is, and relatedly what directory it lives in) and to record the instance (i.e. the `timestamp`). some later files in the pipeline are named more complexly; for instance, a typical log file that records edits made is called `rewriting-log-story-unedited_paris_2023-11-28_22-32-51_long_edited-at_2023-12-04_17-28-50.txt`. however, there is (at least) one exception, namely the file `splitting-failure-log.txt` (of which there's just one).

here are a few more notes.
* since we split overall filenames by underscores (to easily retrieve info (e.g. timestamps) from them), each `{filetype}` is always split with dashes (instead of underscores) when necessary, as is e.g. `edited-at`. moreover, directories are named analogously. for instance, `stories-unedited/` contains `story-unedited` files.
* the bare term "story" always refers to an edited story. (an "unedited story" is always referred to as such.)
* `destination` is e.g. `costarica` or `chiangmai`.
* `length` is always either `short` or `long`.

#### miscellanea

* functions are invoked at the bottom of their defining `.py` files. to keep track of a function having been invoked, typically leave it commented-out -- perhaps with a note of (approximately) when it was invoked.
* all directories containing generated content are in `.gitignore`. the code is written to "safely" generate new files (using `strings.open_safe(...)` instead of `open(...)`), so that these don't need to be created manually before running code.

#### miscellaneous to-do (not including stuff below)

- [ ] before a "final version of v1" pass, clear out all old files!
- [ ] add error-handling for all calls to chatGPT and dalle APIs (including if/when the dalle prompt is too long).
- [ ] improve filename conventions and organization (particularly e.g. for images).
- [x] make sure to use `strings.separator` everywhere instead of `"\n\n=====\n\n"` (and also `strings.separator_long`).
- [ ] keep `sleep_stories_pipeline.pdf` up-to-date. (unfortunately, there doesn't seem to be an easy way to keep it synced with the version in dropbox, so this'll just be done "manually".)
- [ ] delete `ZZZ_` files and directories as they become irrelevant.
- [ ] make sure the above list of modules is complete. to get a deduplicated list of lines in python scripts that contain the string `"import "`, on the command line do `grep "import " *.py | cut -d':' -f2- | sort | uniq`.
- [ ] continue to fill in list of approximate run times.

### get_stops.py

this takes in a destination (listed in `inputs.py`), gets a list of (by default 20) stops along with tidbits about them, and writes it all to a `stops` file in `stops/`.

a typical result file is named `stops_berkeley_2023-11-23_02-25-23.txt`.

STATUS: done.

### write_story.py

this writes a sleep story based on a length (either `short` or `long`), a destination (e.g. `costarica`), a `num_stops_parameter` (explained in the code), and a corresponding `stops` file (by default the most recent one associated to that destination). the code applies to both short and long stories simultaneously, but the actual writing prompts that we feed to chatGPT for these are rather different. this writes a `story-unedited` file in `stories-unedited/`.

a typical result file is named `story-unedited_berkeley_2023-11-24_17-25-36_short.txt`.

a `story-unedited` file is separated into chunks using `strings.separator`, the last simply containing the metadata of which `stops` file the story was written based on.

if chatGPT ever fails to return the correct number of chunks in a middle completion when writing a short story, this is logged at the bottom of `logs/splitting-failure-log.txt`. this should be checked (and fixed by hand where needed) before continuing on to `edit_story`.

STATUS: done.

### edit_story.py

this takes an unedited story and attempts to edit out:
* digits (so that the ElevenLabs AI voice makes no mistake in pronouncing e.g. `"1950"` (depending on the context!)),
* roman numerals (likewise), and
* words that are overused by chatGPT (e.g. `"tapestry"`),

running chunk by chunk. it also replaces all double-quotes (`"`) with single-quotes (`'`). (this is done _after_ the above processing, since in theory chatGPT might accidentally introduce new instances of double-quotes.) here we keep the unedited story's medata and add the metadata of the editing timestamp as well as the list of overused word allowances for this particular story.

actually, we do want to allow chatGPT to _occasionally_ use an "overused word" (such as `"tapestry"`). so there is an optional argument `B` (with default value `3` -- in any case this should always be `<= 10` otherwise the function won't work properly), and for each overused word, we assign an integer between `0` (inclusive) and `B` (exclusive) and then allow at most that many instances to remain in the story. for replicability, this assignment is done by hashing the filename of the unedited story down to base `B`, and then running through its digits and assigning those. (the hash is of size `2 ** 256`, so there's no way we'll run out.) to keep things simple, we just take this number as a counter and decrement it each time we encounter the overused word, and then require it to be removed when the counter is at `0`. (beware that this actually decrements on _each_ rewrite, so e.g. if an overused word appears and we want to allow it but then something else in the chunk triggers a rewrite, it'll be counted _again_ against the counter.) of course, we search e.g. for `"tapestr"` case-insensitively, so that we catch both plural instances as well as instances at the beginning of a sentence. and if a single chunk ever has two or more instances of e.g. `"tapestr"`, then we just tell it to edit them _all_ out but keep the counter unchanged.

this writes to a `story` file in `stories/`. alternatively, when given no arguments, this operates on _all_ `story-unedited` files in `stories-unedited/`.

a typical result file is named `story_berkeley_2023-11-24_17-25-36_short.txt`. the timestamp corresponds to the original writing time, not the editing time. (in particular, whenever we edit an unedited story, we overwrite any previous edited versions.) the metadata now also contains an "edited at" timestamp as well as a list of the allowances for overused words (as described in the above-linked footnote).

if any rewrites are undertaken (which is all but guaranteed), a log file is written to `logs/rewriting-logs`. if during an editing process any rewrite _fails_, a log file is written to `logs/rewriting-failure-logs`. these should both be checked (and fixed by hand where needed) before continuing on to `make_cues`. a quick overview is also available in `logs/rewriting-stats.txt`.

STATUS: done.

### make_cues.py

this takes a story, splits it into cues, and writes them to a `cues` file. this is separated into chunks by `strings.separator`, and the cues within each chunk are separated by `"\n"`. there's also a metadata chunk at the end, which is just copied directly from that of the `story` file.

a typical `cues` file is named `cues_berkeley_2023-11-24_17-25-36_short.txt` (again timestamped by the original writing time).

STATUS: done.

### get_phoneticizations.py

this takes a `cues` file and generates a list of words/phrases as well as phoneticizations for them (written in IPA) with the help of chatGPT. specifically, we phoneticize all proper nouns, all foreign words, and more broadly _any_ words that might be hard to pronounce for the ElevenLabs AI voice (e.g. `"pergola"`).

in testing, chatGPT worked best when operating based on the following prompt (which it itself write).
> Please review the following story and identify any words or terms that may be foreign, technical, proper nouns, or have pronunciations that are not immediately obvious. Include words that might be challenging to pronounce for readers who are not familiar with them, especially those of foreign origin, unique regional names, or specialized jargon.

`ARCHITECTURE (updated monday 3pm):`
* make a list of foreign words etc., one for each story cue file.
* delete duplicates.
* get phoneticizations from chatGPT for all of them, one by one.
* make sure chatGPT only gives _one_ pronunciation. sometimes it gives two. ask for "whichever is most common."
* when getting a pronunciation, make sure to give it context. (probably the chunk suffices, if not just a single cue.)
* remaining question: how can we ensure that we _exactly_ phoneticize everything that we should? for instance, maybe a word is actually pluralized. of course we can ask chatGPT to return the _exact_ matches throughout the story, and give an example to illustrate. and then when we search through the story, of course doing so case-insensitively. we can also save the replacements as metadata.

STATUS: not yet written at all, but tested in chatGPT and it seems to be a fine way to proceed.

### make_kt.py

this takes a pair of a short story cues file and a long story cues file set in the same location, and generates a single `kt` file in `code/` that combines them. optionally (since ElevenLabs is still in the process of getting its "pro" voices to handle IPA phoneticizations), this can first replace hard-to-pronounce words with phoneticizations, using `phoneticization` files for both stories.

if executed with just a `destination` as an argument, this operates as above on the most recent short story cues file and the most recent long story cues file that are set in that location.

if executed with no arguments, this operates as above on all destinations for which there exist both a short story cues file and a long story cues file.

a typical resulting `.kt` file is named `SleepStoryTravelBerkeleyCues.kt`.

STATUS: done, except for phoneticizations (which aren't currently relevant (as of 2023-11-28) anyways).

### get_art_style_description.py

this takes an art style listed in `art_styles.py` and retrieves a lengthy description of it from chatGPT, tailored to help chatGPT write dalle prompts in that style. when called without arguments, it runs on _all_ art styles listed there.

a typical result file is called `art-style-description_magical-realism_2023-11-29_18-29-46.txt`.

STATUS: done.

### get_dalle_prompts.py

`PROBABLY NOT YET FINAL`

this takes `cues` file as well as an `art-style_description` gets one dalle prompt for each cue in the given style from chatGPT. these are separated by `strings.separator` (but not otherwisely (e.g. into chunks)).

a typical result file is named `dalle-prompts_for_cues_queenstown_2023-11-28_22-32-51_short_in_thai-temple_at_2023-11-29_18-01-04.txt`. the latter timestamp is when the file was generated.

STATUS: done.

### get_pix.py

`PROBABLY REORGANIZE where/hoe the pix are stored.`

this takes a `dalle-prompts` file and gets corresponding images from dalle. these are saved in a dedicated directory in `images/`, whose name lists the input `dalle-prompts` file as well as a timestamp of when the images were generated (so that different runs of `get_pix` don't overwrite each other).

a typical name of such a dedicated directory is `images_dalle-prompts_for_cues_tokyo_2023-11-28_22-32-51_long_at_2023-11-29_12-46-14_at_2023-11-29_13-27-04`. conveniently, this name essentially contains the name of the corresponding story file as a substring (here, `story_tokyo_2023-11-28_22-32-51_long.txt`).

the images are named `000.png`, `001.png`, etc.; these align one-to-one with the dalle prompts, and therefore with the cues as well.

this also writes a file to `image-urls/`. however, note that these urls are only valid for 1 hour from when the images were generated. so this is really only useful for more-or-less-immediate debugging: error status codes are logged here.

a typical such file is named `image-urls_dalle-prompts_for_cues_queenstown_2023-11-28_22-32-51_short_in_thai-temple_at_2023-11-29_18-01-04.txt_at_2023-11-29_18-15-46.txt`.

[here](https://cookbook.openai.com/articles/what_is_new_with_dalle_3) is a quick info page on the dalle API. here are a few relevant notes therefrom.
* there doesn't seem to be anything like a "system prompt".
* the maximum allowable length of a prompt is `1_000` characters.
* the parameter `n` is the number of images to create. the default is `n=1`, and this is the _only_ option for dall-e-3.
* `style = "vivid"` is default, but also "natural" is possible.
* `quality = "standard"` is default, but also "hd" is possible.

STATUS: done.

### word_usage_stats.py

this runs some basic statistics, and logs them to the console.
* it runs through all of the unedited stories in `stories-unedited/` and counts the usages of the overused words (as listed in `strings.overused_words`).
* it runs through all of the unedited stories in `stories-unedited/`, counts the usages of _all_ words (ignoring case, but not handling conjugation or pluralization) and plucks out the top bunch of them.

of course, this could be improved or expanded if we ever want.
* we could count instances just in some of the stories.
* we could compare the words against a list of the some most common words (maybe like 20k of them?).
* we could compare the words against an actual list of SAT words.

of course, in any case hopefully we'd continue to handle variations (e.g. due to conjugation or pluralization) gracefully.

STATUS: done (at least for now).