### this is tailored to rotate "apparently-rotated" vids (with respect to apple's ecosystem) to be _truly_ rotated.


import strings
import subprocess


pathname = "vids/2024-01-16/"


vid_filenames = strings.get_all_unhidden_files(pathname + "vids-rotated")

for vid_filename in vid_filenames:

    print("\n" + vid_filename)

    print("\nold dimensions are:")
    subprocess.run(f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1 {pathname + 'vids-rotated/' + vid_filename}", shell=True)

    new_vid_filename = "vid_" + "_".join(vid_filename.split("_")[1: ])

    subprocess.run(f"ffmpeg -i {pathname + 'vids-rotated/' + vid_filename} -vf \"crop=in_h*9/16:in_h\" {pathname + 'vids/' + new_vid_filename}", shell=True)

    print("\nnew dimensions are:")
    subprocess.run(f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1 {pathname + 'vids/' + new_vid_filename}", shell=True)

