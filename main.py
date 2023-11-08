from openai import OpenAI
client = OpenAI()

from datetime import datetime
now = str(datetime.now())
timestamp = now[:10] + "_" + now[11:13] + "-" + now[14:16] + "-" + now[17:19]

#####

destination = "kyoto"


system_prompt = open("prompts/" + destination + "_system_prompt.txt", "r").read()
user_prompts = open("prompts/" + destination + "_user_prompts.txt", "r").read().split("*****")

system_message_obj = {"role": "user", "content": system_prompt}

user_message_objs = []





for user_prompt in user_prompts:
    user_message_obj = {"role": "user", "content": user_prompt}
    user_message_objs.append(user_message_obj)


storyfile = open("stories/" + destination + "_" + timestamp + ".txt", "w")




# FOR LOOP


messages_list = [system_message_obj]

i = 0
for user_message_obj in user_message_objs[:5]:
    print("sending user message number", i)
    messages_list.append(user_message_obj)
    completion = client.chat.completions.create(
        model = "gpt-4-32k",
        messages = messages_list
    )
    assistant_message = completion.choices[0].message.content
    storyfile.write(assistant_message + "\n\n=====\n\n")
    assistant_message_obj = {"role": "assistant", "content": assistant_message}
    messages_list.append(assistant_message_obj)
    i += 1









# BY HAND, BEGINNING OF FOR LOOP


# print("getting completion_0")
# completion_0 = client.chat.completions.create(
#   model="gpt-4-32k",
#   messages=[system_message_obj, user_message_objs[0]]
# )


# assistant_message_0 = completion_0.choices[0].message.content

# assistant_message_obj_0 = {"role": "assistant", "content": assistant_message_0}

# storyfile.write(assistant_message_0 + "\n\n")

# print("getting completion_1")
# completion_1 = client.chat.completions.create(
#     model="gpt-4-32k",
#     messages=[system_message_obj, user_message_objs[0], assistant_message_obj_0, user_message_objs[1]]
# )

# assistant_message_1 = completion_1.choices[0].message.content

# storyfile.write(assistant_message_1 + "\n\n")

# print("done")













### SAVE TO A TXT FILE

# story = open("stories/" + destination + "_" + timestamp + ".txt", "w")




# actually it seems that there's only one element here, as of 2023-11-08 at ~2:30am.
# if it does ever become an array, a different way of writing it all out at once would be the following, although make sure to add extra newlines if needed.
    # story.writelines(choices_obj.message for choices_obj in completion.choices)
