##### this code takes in a pair of cues files set in the same location `destination`, one long and one short, and creates a kotlin file `SleepStory{Destination}Cues.kt` in `code/`.
# if we _only_ specify a destination, we automatically pull the cues files for the most recently written short and long stories in that destination.
# if we don't even specify a destination, then we do this for all destinations that have cues files associated to both short and long stories.
# this function will EVENTUALLY (as of 2023-11-28) accept a `use_phoneticizations` boolean, which defaults to `False`. if this is set to `True`, we do a find-and-replace on the cues string over the relevant phoneticizations (which will have been retrieved from chatGPT and stored in `phoneticizations/`) before writing to the kotlin file. (this will be put at `INSERT PHONETICIZATION LOGIC HERE`.)

import strings # so, `my_string` defined over there is accessible here as `strings.my_string`.

# here, the `_arg` suffix is to distinguish from other variables that appear in the function definition. (they quickly get subsumed as instances of those.)
# when writing a long story, we _always_ roll the last stop into the `end` of the story. so, min_stops_for_long_story is one more than the number of stops rolled into the `start` of the story.
def make_kt(destination_arg = None, long_story_cues_filename_arg = None, short_story_cues_filename_arg = None, min_stops_for_long_story = 1, use_phoneticizations = False):

    # create a dictionary whose keys are all destinations that we will make a pair for. for now, all values are `None`.
    if destination_arg:
        print(f"destination_arg exists, and is: {destination_arg}")
        story_pairs = {
            destination_arg: None
        }
    else:
        all_cues_filenames = strings.get_all_unhidden_files("cues")
        list_of_destinations_of_cues_filenames = [cues_filename.split("_")[1] for cues_filename in all_cues_filenames]
        set_of_destinations = set(list_of_destinations_of_cues_filenames)
        story_pairs = {}
        for destination in set_of_destinations:
            story_pairs[destination] = None
    
    # now, change the values to dictionaries storing the of cues_filenames, or delete a key if it doesn't have cue files for both a short and a long story available. (this needs to happen _after_ the `for` loop, though; it's apparently not allowed to delete a key while we're in the process of running through it.)
    keys_for_deletion = []
    for destination in story_pairs:
        long_story_cues_filename = strings.get_latest_filename(destination, "cues", "long")
        print(f"long_story_cues_filename is: {long_story_cues_filename}")
        short_story_cues_filename = strings.get_latest_filename(destination, "cues", "short")
        print(f"short_story_cues_filename is: {short_story_cues_filename}")
        # overwrite the above if either/both was specified as an argument of the function.
        if destination == destination_arg:
            if long_story_cues_filename_arg:
                long_story_cues_filename = long_story_cues_filename_arg
                print(f"overwriting long_story_cues_filename (in case a not-most-recent filename was passed in), and now it is: {long_story_cues_filename}")
            if short_story_cues_filename_arg:
                short_story_cues_filename = short_story_cues_filename_arg
                print(f"overwriting short_story_cues_filename (in case a not-most-recent filename was passed in), and now it is: {short_story_cues_filename}")
        # if both short and long stories exist for the destination, save them to the dictionary in a dictionary. otherwise, delete the key from the dictionary.
        if long_story_cues_filename and short_story_cues_filename:
            story_pairs[destination] = {
                "long_story_cues_filename": long_story_cues_filename,
                "short_story_cues_filename": short_story_cues_filename
            }
        else:
            keys_for_deletion.append(destination)
    for key in keys_for_deletion:
        del story_pairs[key]
    
    print(f"story_pairs is:\n{story_pairs}")
    
    # now, write one kt file for each pair.
    for destination in story_pairs:

        # make a dictionary specifically for this destination and kt file.
        stories = {
            "short": {
                "filename": story_pairs[destination]['short_story_cues_filename']
            },
            "long": {
                "filename": story_pairs[destination]['long_story_cues_filename']
            }
        }

        for length in stories:
            
            cues_string = open(f"cues/{stories[length]['filename']}", "r").read()
            chunks_as_strings = cues_string.split(strings.separator)
            stories[length]["metadata"] = chunks_as_strings.pop()
            
            ### INSERT PHONETICIZATION LOGIC HERE, applied to each chunk in chunks_as_strings. (we do it here, _after_ popping off the metadata.) then, append to the metedata the info of what phoneticizations occurred.
            ### be sure to run from longest to shortest string that's being replaced with a phoneticization, so that we never accidentally do a replacement for a substring and then miss the larger one.
            
            chunks_as_lists_of_cues = [chunk_as_string.split("\n") for chunk_as_string in chunks_as_strings]
            
            # create the `start`, `middle`, and `end` strings for the kotlin file.
            
            if length == "long":
                index_between_start_and_middle = min_stops_for_long_story
                index_between_middle_and_end = -2
            elif length == "short":
                index_between_start_and_middle = 1
                index_between_middle_and_end = -1
            
            start_chunks = chunks_as_lists_of_cues[: index_between_start_and_middle]
            middle_chunks = chunks_as_lists_of_cues[index_between_start_and_middle: index_between_middle_and_end]
            end_chunks = chunks_as_lists_of_cues[index_between_middle_and_end: ]

            list_of_start_cues = sum(start_chunks, [])
            stories[length]["start"] = strings.format_list_of_cues_as_kotlin(list_of_start_cues)

            middle_chunks_formatted = [strings.format_list_of_cues_as_kotlin(middle_chunk) for middle_chunk in middle_chunks]
            stories[length]["middle"] = ",\n\n".join(middle_chunks_formatted)

            list_of_end_cues = sum(end_chunks, [])
            stories[length]["end"] = strings.format_list_of_cues_as_kotlin(list_of_end_cues)

            # get the stops filename and string.
            stories[length]["stops_filename"] = stories[length]["metadata"].split("\n")[0].split(" ")[-1]
            stories[length]["stops_string"] = open(f"stops/{stories[length]['stops_filename']}", "r").read()
        
        # now (outside of the `for` loop), do stuff that involves both stories simultaneously.

        cues_files_string = f"this code was generated from the cues files {stories['short']['filename']} and {stories['long']['filename']}, which were generated from story files with the corresponding names."

        # check if the stops files are the same, and generate a `stops_info_string` and an `aggregated_stops_string` accordingly.
        if stories["long"]["stops_filename"] == stories["short"]["stops_filename"]:

            stops_files_info_string = f"in turn, these stories were both generated from the single stops file {stories['short']['stops_filename']}, which is copied (commented-out) at the bottom of this file (after a bunch of slashes)."
            
            aggregated_stops_string = f"""/*

////////////////////////////////////////////////////////////////////////////////

{stories['short']['stops_string']}

*/"""
        else:

            stops_files_info_string = f"in turn, the short story was generated from the stops file {stories['short']['stops_filename']}, while the long story was generated from the stops file {stories['long']['stops_filename']}. these stops files are both copied (commented-out) at the bottom of this file (after a bunch of slashes and separated by a bunch of slashes), in that order."

            aggregated_stops_string = f"""/*

////////////////////////////////////////////////////////////////////////////////

{stories['short']['stops_string']}

////////////////////////////////////////////////////////////////////////////////

{stories['long']['stops_string']}

*/"""

        min_stops_for_long_story_string = f"min_stops_for_long_story is set to {min_stops_for_long_story}."

        aggregated_story_metadata = f"""SHORT STORY METADATA:

story filename: {stories['short']['filename']}

{stories['short']['metadata']}

LONG STORY METADATA:

story filename: {stories['long']['filename']}

{stories['long']['metadata']}"""

        Destination = destination[: 1].upper() + destination[1: ]
        object_name = f"SleepStoryTravel{Destination}Cues"
        kotlin_filename = f"{object_name}.kt"

        kotlin_string = f"""{strings.kotlin_comment(cues_files_string)}

{strings.kotlin_comment(stops_files_info_string)}

{strings.kotlin_comment(min_stops_for_long_story_string)}

{strings.kotlin_comment(aggregated_story_metadata)}

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

{aggregated_stops_string}"""

        kotlin_file = open(f"code/{kotlin_filename}", "w")
        kotlin_file.write(kotlin_string)
        kotlin_file.close()

        print(f"finished processing the cues files {stories['short']['filename']} and {stories['long']['filename']} into a single kotlin file.")

    return None

make_kt()