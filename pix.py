from openai import OpenAI
client = OpenAI()
gpt_model = "gpt-4-1106-preview"
image_model = "dall-e-3"
# some quick API info is here: https://cookbook.openai.com/articles/what_is_new_with_dalle_3
# a few relevant notes:
    # there doesn't seem to be anything like a "system prompt".
    # the maximum allowable length of a prompt is 1_000 characters.
    # the parameter n is the number of images to create. the default is n=1, and this is the _only_ option for dall-e-3.
    # style = "vivid" is default, but also "natural" is possible.
    # quality = "standard" is default, but also "hd" is possible.

import re # regular expressions

import requests # to retrieve pix






# ### TEST API CALLS HERE

# try:
#     response = client.images.generate(
#         model = image_model,
#         prompt = """a mouse reading a book about a mouse reading a book""",
#         size = "1024x1792",
#         quality = "standard",
#         style = "vivid",
#     )
#     image_url = response.data[0].url
#     print(f"the image_url is: {image_url}")
#     image = requests.get(image_url)
#     print(f"image is: {image}")
#     print(f"type(image) is: {type(image)}")
#     if image.status_code == 200:
#         print("hooray, status code is 200!")
#         png_file = open("the_image.png", "wb")
#         png_file.write(image.content)
#     else:
#         print(f"sadly, status code is {image.status_code}")


# except Exception as exception:
#     print(f"an error occurred: {exception}")


dalle_prompts_txt_file_name = "london_2023-11-16_01-20-42_long.txt"

dalle_prompts_string = open(f"dalle_prompts/{dalle_prompts_txt_file_name}", "r").read()

dalle_prompts = dalle_prompts_string.split("\n")

image_urls = []
for index, dalle_prompt in enumerate(dalle_prompts):
    print(f"getting a pic for the dalle prompt:\n{dalle_prompt}")
    index_string = str(index)
    while len(index_string) < 3:
        index_string = "0" + index_string    
    try:
        response = client.images.generate(
            model = image_model,
            prompt = dalle_prompt,
            size = "1024x1792",
        )
        image_url = response.data[0].url
        image_urls.append(image_url)
        image = requests.get(image_url)
        if image.status_code == 200:
            png_file = open(f"images/{dalle_prompts_txt_file_name[:-4]}_{index_string}.png", "wb")
            png_file.write(image.content)
        else:
            print(f"ERROR: status code is: {image.status_code}")
    except Exception as exception:
        print(f"an error occurred: {exception}")

url_file = open(f"image_urls/{dalle_prompts_txt_file_name}", "w")
url_file.write("\n".join(image_urls))
url_file.close()