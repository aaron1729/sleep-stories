from os import listdir
from os.path import isfile, join
txt_file_names_incl_hidden = [f for f in listdir("stories/") if isfile(join("stories/", f))]
txt_file_names = [file_name for file_name in txt_file_names_incl_hidden if file_name[0] != "."]
txt_file_names.sort() # make alphabetical, for reproduceability.

enums = []
index = 8598 # starting value
for txt_file_name in txt_file_names:
    [destination, date, time] = txt_file_name.split("_")
    # timestamp = date + "_" + time[:8] # not needed
    enums.append(f"sleep_story_travel_{destination}({index})".upper())
    index += 1

print(",\n".join(enums))