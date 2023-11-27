# sleep-stories

## setup

### venv

make sure the `openai-env` virtual environment is both loaded and running. to load, on the command line in the root of the repo do `python -m venv openai-env`; to run, on the command line (in macOS) do `source openai-env/bin/activate`.

### openai module

make sure to do `pip install openai`. (i think `pip` only exists once python is installed (e.g. because usually i do `pip3` when i only have `python3` and `pip` doesn't even work). so, be sure to do this _after_ the venv setup above.)

### API key

this ought to have an API key saved (say at the bottom of the file `openai-env/bin/activate`), as explained [here](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key). remember that a terminal window sets the environment variables right when it's opened, so if/when this is updated, open a _new_ terminal window to test the new settings.

### other modules

these should be installed by `pip install`. a (probably incomplete) list of modules used (beyond `openai` of course) is: `re` (for regex), `datetime` (for timestamps), `os` (for interacting with the operating system), 

## pipeline

here's a description of the pipeline, script by script, in order.

### meta info

`strings.py` contains some strings and string-writing functions (e.g. chatGPT prompts).

`models.py` contains choice of `gpt_model` and `image_model` (currently set to `gpt-4-1106-preview` and `dall-e-3`, respectively).

filenames are generally of the form `{filetype}_{destination}_{timestamp}[_{length}].ending`. here, `destination` is e.g. `costarica` and `length` is always either `short` or `long`. an exception is `art-styles_{timestamp}.txt` (since these are each generally associated to many different destinations).

### inputs.py

the file `inputs.py` contains info about destinations (including optional info like transport method, requested sightseeing stops, info about the tour guide, and season). every story begins with an entry here.

STATUS: done.

### get_stops.py

this takes in a destination (listed in `inputs.py`), gets a list of (by default 20) stops along with tidbits about them, and writes it all to a `stops` file in `stops/`.

a typical result file is named `stops_berkeley_2023-11-23_02-25-23.txt`.

STATUS: done.

### write_stories.py

this takes a length (either `short` or `long`), a destination, a `num_stops_parameter` (explained in the code), and a corresponding `stops` file (by default the most recent one for that destination), and writes a story. the code applies to both short and long stories simultaneously, but the actual writing prompts are rather different. this writes to `stories-unedited`.

this file is separated into "chunks", the last simply containing the metadata of which `stops` file the story was written based on.

for long stories, each chunk (aside from the last one) is a single chatGPT completion. but for short stories, in order to make the chunks themselves shorter, the middle completions are actually broken up into multiple chunks. (this is the purpose of having the parameter `n`; completions tend to be around 500-800 words, regardless of how many stops are given in the user prompt.)

a typical result file is named `story-unedited_berkeley_2023-11-24_17-25-36_short.txt`.

STATUS: mostly done, but currently editing (4pm on sun 11/26). mainly just remove the edit_stories stuff, and also log any splitting failures during the process of writing a short story. if this ever fails, we make a log to `logs/splitting_failure_log.txt`.

### edit_stories.py

this takes an unedited story and attempts to edit out digits, roman numerals, and words that are overused by chatGPT (e.g. "tapestry"). this writes to `stories/`.

in this file, the final chunk now also contains the metadata of the "sentence replacement pairs", i.e. the pairs of an old sentence that was editing as well as the new sentence that replaced it.

a typical result file is named `story_berkeley_2023-11-24_17-25-36_short.txt`. (the timestamp corresponds to the original writing time, not the editing time.)

STATUS: not yet written, but will be based on existing stuff.

### process.py

this takes a pair of a short story and a long story set in the same destination, and generates both a single `.kt` file in `code/` as well as a pair of files in `cues/` that just contain the unadorned cues (for later usage in generating dalle prompts).

a typical `.kt` file is named `SleepStoryTravelBerkeleyCues.kt`. a typical cues file is named `cues_berkeley_2023-11-24_17-25-36_short.txt` (again timestamped by the original writing time).

STATUS: done.

### choose_art_styles.py

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