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
                png_file = strings.open_safe(images_directory_path, f"{index_string}.png", "wb")
                png_file.write(image.content)
                png_file.close()
            else:
                error_message = f"ERROR getting image {index_string}; image.status_code={image.status_code}"
                print(error_message)
                image_urls.append(error_message)
        except Exception as exception:
            print(f"an error occurred: {exception}")
    
    image_urls_filename = f"image-urls_{dalle_prompts_filename}_at_{timestamp}.txt"
    image_urls_file = strings.open_safe("image-urls", image_urls_filename, "w")
    image_urls_file.write("\n".join(image_urls))
    image_urls_file.close()

    print(f"finished getting images based on {dalle_prompts_filename} at {strings.time_now()}")

    return None



### let's get some pix!
# get_pix(...)
# get_pix("dalle-prompts_for_cues_dubai_2023-11-28_22-32-51_short_in_rothko_at_2023-12-06_00-41-33.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_long_in_rococo_at_2023-12-07_00-10-20.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_long_in_gothic_at_2023-12-07_00-26-03.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_long_in_retrofuturism_at_2023-12-07_00-48-55.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_long_in_steampunk_at_2023-12-07_11-26-12.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_long_in_acrylic-pour_at_2023-12-14_16-09-00.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_long_in_autumn-skye_at_2023-12-14_16-34-50.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_long_in_impressionism_at_2023-12-20_18-28-02.txt")



### starting here on 12/20/2023, with actual art styles for v1 of illustrations.
# get_pix

# 7:06pm: algarve
# ("dalle-prompts_for_cues_algarve_2023-12-05_17-42-24_short_in_fauvism_at_2023-12-20_18-59-24.txt")

# 7:29pm: amalfi through berkeley
# get_pix("dalle-prompts_for_cues_amalfi_2023-12-05_17-42-24_short_in_van-gogh_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_bali_2023-12-05_17-42-24_short_in_batik_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_bangkok_2023-12-05_17-42-24_short_in_thai-temple_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_barcelona_2023-12-05_17-42-24_short_in_miro_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_berkeley_2023-12-05_17-42-24_short_in_art-nouveau_at_2023-12-20_18-59-24.txt")

# 8:12pm: chiangmai through paris
# get_pix("dalle-prompts_for_cues_chiangmai_2023-12-05_17-42-24_short_in_lanna_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_cinqueterre_2023-12-05_17-42-24_short_in_cave_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_costarica_2023-12-05_17-42-24_short_in_watercolor_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_dubai_2023-12-05_17-42-24_short_in_visionary_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_greece_2023-12-05_17-42-24_short_in_pointillism_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_istanbul_2023-12-05_17-42-24_short_in_islamic-geometric_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_kyoto_2023-12-05_17-42-24_short_in_japanese-woodblock_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_london_2023-12-05_17-42-24_short_in_victorian_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_napa_2023-12-05_17-42-24_short_in_cubism_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_newyorkcity_2023-12-05_17-42-24_short_in_pop_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_paris_2023-12-05_17-42-24_short_in_neobaroque_at_2023-12-20_18-59-24.txt")

# 8:31pm: queenstown through tokyo
# get_pix("dalle-prompts_for_cues_queenstown_2023-12-05_17-42-24_short_in_retrofuturism_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_rio_2023-12-05_17-42-24_short_in_mondrian_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_shanghai_2023-12-05_17-42-24_short_in_tomine_at_2023-12-20_18-59-24.txt")
# get_pix("dalle-prompts_for_cues_tokyo_2023-12-05_17-42-24_short_in_manga_at_2023-12-20_18-59-24.txt")