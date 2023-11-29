from openai import OpenAI
client = OpenAI()

import re
import requests
from os import makedirs

import models
import strings

timestamp = strings.time_now()

# the input `dalle_prompts_filename` is e.g. dalle-prompts_for_cues_tokyo_2023-11-28_22-32-51_long_at_2023-11-29_12-46-14.txt
def get_pix(dalle_prompts_filename):

    print(f"getting pix based on {dalle_prompts_filename} at {strings.time_now()}")

    images_directory_name = f"images_{dalle_prompts_filename[:-4]}_at_{timestamp}"
    images_directory_path = f"images/{images_directory_name}"
    makedirs(images_directory_path)

    dalle_prompts = open(f"dalle-prompts/{dalle_prompts_filename}", "r").read().split(strings.separator)

    print(f"now attempting to get {len(dalle_prompts)} images from dalle")

    image_urls = []
    for (index, dalle_prompt) in enumerate(dalle_prompts):
        index_string = ("00" + str(index))[-3: ]
        print(f"getting image {index_string}")
        try:
            response = client.images.generate(
                model = models.image_model,
                prompt = dalle_prompt,
                size = "1024x1792",
            )
            image_url = response.data[0].url
            print(f"image_url is: {image_url}")
            image = requests.get(image_url)
            if image.status_code == 200:
                print(f"got image {index_string} at {strings.time_now()}")
                image_urls.append(image_url)
                png_file = open(f"{images_directory_path}/{index_string}.png", "wb")
                png_file.write(image.content)
                png_file.close()
            else:
                error_message = f"ERROR getting image {index_string}; image.status_code={image.status_code}"
                print(error_message)
                image_urls.append(error_message)
        except Exception as exception:
            print(f"an error occurred: {exception}")
    
    image_urls_filename = f"image-urls_{dalle_prompts_filename}_at_{timestamp}.txt"
    image_urls_file = open(f"image-urls/{image_urls_filename}", "w")
    image_urls_file.write("\n".join(image_urls))
    image_urls_file.close()

    print(f"finished getting images based on {dalle_prompts_filename} at {strings.time_now()}")

    return None



### let's get some pix!
# get_pix("dalle-prompts_for_cues_tokyo_2023-11-28_22-32-51_long_at_2023-11-29_12-46-14.txt")
get_pix("dalle-prompts_for_cues_kyoto_2023-11-28_22-32-51_long_at_2023-11-29_13-56-54.txt")