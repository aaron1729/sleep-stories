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
                # style = "natural", # TEST!
                # quality = "hd", # TEST!
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

# all have been sent to carlos. except for the first few, 
# get_pix("dalle-prompts_for_cues_tokyo_2023-11-28_22-32-51_long_at_2023-11-29_12-46-14.txt")
# get_pix("dalle-prompts_for_cues_kyoto_2023-11-28_22-32-51_long_at_2023-11-29_13-56-54.txt")
# get_pix("dalle-prompts_for_cues_algarve_2023-11-28_22-12-12_short_at_2023-11-29_15-41-13.txt")
# get_pix("dalle-prompts_for_cues_dubai_2023-11-28_22-32-51_short_at_2023-11-29_15-44-24.txt")
# get_pix("dalle-prompts_for_cues_napa_2023-11-28_22-32-51_long_in_cubism_at_2023-11-29_17-36-26.txt")
# get_pix("dalle-prompts_for_cues_rio_2023-11-28_22-32-51_long_in_victorian_at_2023-11-29_17-49-06.txt")
# get_pix("dalle-prompts_for_cues_chiangmai_2023-11-28_22-32-51_long_in_sepia-pencil_at_2023-11-29_17-50-37.txt")


# run at 6:15pm. commented-out means sent to carlos.
# get_pix("dalle-prompts_for_cues_bali_2023-11-28_22-32-51_short_in_manga_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_costarica_2023-11-28_22-32-51_short_in_pop_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_newyorkcity_2023-11-28_22-32-51_long_in_psychedelic_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_queenstown_2023-11-28_22-32-51_short_in_thai-temple_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_paris_2023-11-28_22-32-51_short_in_islamic-geometric_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_istanbul_2023-11-28_22-32-51_long_in_turkish-marbling_at_2023-11-29_18-01-04.txt")



# run at 6:48pm. commented-out means sent to carlos.
# get_pix("dalle-prompts_for_cues_greece_2023-11-28_22-32-51_short_in_pointillism_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_london_2023-11-28_22-32-51_short_in_abstract_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_shanghai_2023-11-28_22-32-51_short_in_surrealism_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_barcelona_2023-11-28_22-32-51_short_in_neoexpressionism_at_2023-11-29_18-01-04.txt")
# get_pix("dalle-prompts_for_cues_algarve_2023-11-28_22-12-12_long_in_cave_at_2023-11-29_18-41-22.txt")
# get_pix("dalle-prompts_for_cues_amalfi_2023-11-28_22-32-51_short_in_magical-realism_at_2023-11-29_18-30-59.txt")
