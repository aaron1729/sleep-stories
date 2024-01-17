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

    # for image filenames
    destination = dalle_prompts_filename.split("_")[4]

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
                png_file = strings.open_safe(images_directory_path, f"img_{destination}_{timestamp}_{index_string}.png", "wb")
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

# 12/21/2023 at 2:08am...
# all_prompts_filenames = strings.get_all_unhidden_files("dalle-prompts")
# for prompts_filename in all_prompts_filenames[14: ]:
#     get_pix(prompts_filename)



# morning of thurs 12/21
# greece
# get_pix("dalle-prompts_for_cues_greece_2023-12-05_17-42-24_short_in_pointillism_at_2023-12-21_00-08-56.txt")
# london
# get_pix("dalle-prompts_for_cues_london_2023-12-05_17-42-24_short_in_victorian_at_2023-12-21_00-08-56.txt")
# rio
# get_pix("dalle-prompts_for_cues_rio_2023-12-05_17-42-24_short_in_mondrian_at_2023-12-21_00-09-10.txt")
# amalfi
# get_pix("dalle-prompts_for_cues_amalfi_2023-12-05_17-42-24_short_in_van-gogh_at_2023-12-21_00-08-56.txt")
# paris
# get_pix("dalle-prompts_for_cues_paris_2023-12-05_17-42-24_short_in_neobaroque_at_2023-12-21_00-09-10.txt")
# chiangmai
# get_pix("dalle-prompts_for_cues_chiangmai_2023-12-05_17-42-24_short_in_lanna_at_2023-12-21_00-08-56.txt")



########

# monday 1/15/2024:

# 8:45pm

# get_pix("dalle-prompts_for_cues_accra_2024-01-15_14-36-17_short_in_ghanaian_at_2024-01-15_20-28-42.txt")
# get_pix("dalle-prompts_for_cues_arizona_2024-01-15_14-36-17_short_in_navajo_at_2024-01-15_20-27-51.txt")
# get_pix("dalle-prompts_for_cues_marrakech_2024-01-15_14-36-47_short_in_moroccan_at_2024-01-15_20-28-34.txt")
# get_pix("dalle-prompts_for_cues_yucatan_2024-01-15_17-03-38_short_in_mayan_at_2024-01-15_20-28-08.txt")

# 9:06pm
# get_pix("dalle-prompts_for_cues_seattle_2024-01-15_12-02-46_short_in_chihuly_at_2024-01-15_20-56-29.txt")
# get_pix("dalle-prompts_for_cues_vienna_2024-01-15_14-37-20_short_in_neobaroque_at_2024-01-15_20-58-01.txt")
# get_pix("dalle-prompts_for_cues_losangeles_2024-01-15_14-36-47_short_in_pop_at_2024-01-15_20-58-40.txt")
# get_pix("dalle-prompts_for_cues_normandy_2024-01-15_14-37-11_short_in_fauvism_at_2024-01-15_20-59-11.txt")
# get_pix("dalle-prompts_for_cues_amsterdam_2024-01-15_14-36-17_short_in_van-gogh_at_2024-01-15_20-59-26.txt")
# get_pix("dalle-prompts_for_cues_addisababa_2024-01-15_14-36-17_short_in_ethiopian_at_2024-01-15_20-59-56.txt")


# morning of tues 1/16/2024
# get_pix("dalle-prompts_for_cues_madagascar_2024-01-15_14-36-47_short_in_watercolor_at_2024-01-16_10-09-05.txt")
# get_pix("dalle-prompts_for_cues_dubrovnik_2024-01-15_14-36-17_short_in_pointillism_at_2024-01-16_10-11-43.txt")
# get_pix("dalle-prompts_for_cues_rome_2024-01-15_14-37-11_short_in_baroque_at_2024-01-16_10-16-57.txt")
# get_pix("dalle-prompts_for_cues_beijing_2024-01-15_14-36-17_short_in_chinese-silk_at_2024-01-16_10-22-15.txt")
# get_pix("dalle-prompts_for_cues_taipei_2024-01-15_14-37-20_short_in_chinese-ink-wash_at_2024-01-16_10-22-06.txt")
# get_pix("dalle-prompts_for_cues_losangeles_2024-01-15_14-36-47_short_in_graffiti_at_2024-01-16_10-34-44.txt")
# get_pix("dalle-prompts_for_cues_goa_2024-01-15_14-36-47_short_in_tanjore_at_2024-01-16_10-28-30.txt")


### tues 1/16/2024 around 1pm

# budapest
# get_pix("dalle-prompts_for_cues_budapest_2024-01-15_14-36-17_short_in_sepia-pencil_at_2024-01-16_12-20-21.txt")

# nepal
# get_pix("dalle-prompts_for_cues_nepal_2024-01-15_14-37-11_short_in_mithila_at_2024-01-16_12-20-31.txt")

# hawaii
# get_pix("dalle-prompts_for_cues_hawaii_2024-01-15_14-36-47_short_in_tapa_at_2024-01-16_12-20-40.txt")

# iceland
# get_pix("dalle-prompts_for_cues_iceland_2024-01-15_14-36-47_short_in_icelandic-illuminated_at_2024-01-16_12-20-47.txt")

# seoul
# get_pix("dalle-prompts_for_cues_seoul_2024-01-15_14-37-20_short_in_minhwa_at_2024-01-16_12-20-56.txt")

# mumbai
# get_pix("dalle-prompts_for_cues_mumbai_2024-01-15_14-36-47_short_in_mughal_at_2024-01-16_12-21-02.txt")

# norway
# get_pix("dalle-prompts_for_cues_norway_2024-01-15_14-37-11_short_in_viking-engraving_at_2024-01-16_12-21-09.txt")

#########

### tues 1/16/2024 around 2pm

# montreal
# get_pix("dalle-prompts_for_cues_montreal_2024-01-15_14-36-47_short_in_quebecois_at_2024-01-16_13-20-29.txt")

# patagonia
# get_pix("dalle-prompts_for_cues_patagonia_2024-01-15_14-37-11_short_in_peruvian_at_2024-01-16_13-20-37.txt")

# prague
# get_pix("dalle-prompts_for_cues_prague_2024-01-15_14-37-11_short_in_oil_at_2024-01-16_13-20-44.txt")

# puertorico
# get_pix("dalle-prompts_for_cues_puertorico_2024-01-15_14-37-11_short_in_carribean-folk_at_2024-01-16_13-20-53.txt")

# vancouver
# get_pix("dalle-prompts_for_cues_vancouver_2024-01-15_14-37-20_short_in_retrofuturism_at_2024-01-16_13-21-03.txt")

# yellowstone
# get_pix("dalle-prompts_for_cues_yellowstone_2024-01-15_14-37-20_short_in_american-romanticism_at_2024-01-16_13-21-10.txt")

### one more, since the previous batch was too small and didn't have enough good ones...

# get_pix("dalle-prompts_for_cues_normandy_2024-01-15_14-37-11_short_in_fauvism_at_2024-01-16_14-45-41.txt")

