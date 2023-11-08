
# env_vars = open(".env", "r").read().splitlines()
# for str in env_vars:
#     if str[:15] == "openai_api_key=":
#         openai_api_key = str[15:]

from openai import OpenAI
client = OpenAI()

from datetime import datetime
now = str(datetime.now())
timestamp = now[:10] + "_" + now[11:13] + "-" + now[14:16] + "-" + now[17:19]

destination = "kyoto"


system_prompt = open("prompts/" + destination + "_system_prompt.txt", "r").read()
user_prompts = open("prompts/" + destination + "_user_prompts.txt", "r").read().split("*****")

user_message_objs = []

for user_prompt in user_prompts:
    user_message_obj = {"role": "user", "content": user_prompt}
    user_message_objs.append(user_message_obj)




completion = client.chat.completions.create(
  model="gpt-4-32k",
  messages=[{"role": "system", "content": system_prompt}, ] + user_message_objs
)



story = open("stories/" + destination + "_" + timestamp + ".txt", "w")

# actually it seems that there's only one element here, as of 2023-11-08 at ~2:30am.
# if it does ever become an array, a different way of writing it all out at once would be the following, although make sure to add extra newlines if needed.
    # story.writelines(choices_obj.message for choices_obj in completion.choices)

for obj in completion.choices:
    print("writing a message...")
    story.write(completion.choices[i].message.content + "\n\n")

print("finished writing")