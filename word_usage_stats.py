##### this counts the instances of the overused words in all of the unedited stories together.

import re
import strings

unedited_story_filenames = strings.get_all_unhidden_files("stories-unedited/ZZZ")

story_strings = []

for unedited_story_filename in unedited_story_filenames:
    unedited_story_string = open(f"stories-unedited/ZZZ/{unedited_story_filename}", "r").read()
    # remove metadata
    story_chunks = unedited_story_string.split(strings.separator)[: -1]
    story_string = strings.nn.join(story_chunks)
    story_strings.append(story_string)

stories_string = strings.nn.join(story_strings)

for entry in strings.overused_words:
    count = len(re.findall(entry['pattern'], stories_string))
    print(f"{entry['word']}: {count}")

stories_string_lower = stories_string.lower()
words_list = re.sub(r"[^a-zA-Z ]", "", stories_string_lower).split(" ")

word_counts = {}
for word in words_list:
    if not word in word_counts:
        word_counts[word] = 0
    word_counts[word] += 1

print("number of distinct words is:", len(word_counts))

top_words = sorted(word_counts.items(), key=lambda kvp: kvp[1], reverse=True)[:500]

for kvp in top_words:
    if len(kvp[0]) > 4:
        print(kvp)


print("by-hand count:", word_counts['palpable'])

