try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import numpy as np
import shutil

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

def crop_size_for_video_and_images(input_dir, output_image_dir):
    create_folder_if_not_exist(output_image_dir)
    folders = [f for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    print 'folders:', folders   # This should be a list of stroke classes

    # folders should contain bottom_player_winning and top_player_winning.
    for folder in folders:
        input_folder_path = os.path.join(input_dir, folder)
        image_folders = [f for f in sorted(os.listdir(input_folder_path)) if os.path.isdir(os.path.join(input_folder_path, f))]
        output_image_path = os.path.join(output_image_dir, folder)
        create_folder_if_not_exist(output_image_path)
        # if more than 10 image frames, crop them and copy over into one folder
        for img_folder in image_folders:
            full_input_folder_name = os.path.join(input_folder_path, img_folder)
            if len(os.listdir(full_input_folder_name)) <= 10:
                continue
            full_img_folder_name = os.path.join(output_image_path, img_folder)
            create_folder_if_not_exist(full_img_folder_name)
            for img_file in os.listdir(full_input_folder_name):
                ii = Image.open(os.path.join(full_input_folder_name, img_file))
                box = (300, 0, 900, 600)
                region = ii.crop(box)
                region.save(os.path.join(full_img_folder_name, img_file))
                print 'save cropped image to', os.path.join(full_img_folder_name, img_file)

    return

###### CODE BELOW SELECTS LAST SAMPLE_RATE FRAMES (last second) OF EACH POINT AND PUT INTO THE *_selected FOLDER #####
def select_images_last_10(output_image_dir):
    assert(os.path.isdir(output_image_dir))
    folders = [f for f in sorted(os.listdir(output_image_dir)) if os.path.isdir(os.path.join(output_image_dir, f))]
    # folders should contain bottom_player_winning and top_player_winning.
    for folder in folders:
        output_selected_image_path = os.path.join(output_image_dir, folder+'_selected')
        create_folder_if_not_exist(output_selected_image_path)
        output_image_path = os.path.join(output_image_dir, folder)
        assert(os.path.isdir(output_image_path))

        image_folders = [f for f in sorted(os.listdir(output_image_path)) if os.path.isdir(os.path.join(output_image_path, f))]
        for img_folder in image_folders:
            full_output_image_path = os.path.join(output_image_path, img_folder)

            files_to_copy = sorted(os.listdir(full_output_image_path))
            if len(files_to_copy) < 10:
                continue
            for f in files_to_copy[-10:]:
                src = os.path.join(full_output_image_path, f)
                dest = os.path.join(output_selected_image_path, img_folder+'_'+f)
                print "DEBUG: copy ", src, " to ", dest
                shutil.copy(src, dest)

def main(input_dir, image_dir):
    start_time = time.time()
    crop_size_for_video_and_images(input_dir, image_dir)
    # select_images(args.image_dir, args.audio_dir)
    select_images_last_10(image_dir)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing a set of stroke classes like top_player_winning, bottom_player_winning etc.')
    parser.add_argument("image_dir", type=str, help='Path to the output images from the game.')
    # parser.add_argument("audio_dir", type=str, help='Path to the output audio directory.')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.image_dir = os.path.abspath(args.image_dir)
    # args.audio_dir = os.path.abspath(args.audio_dir)
    main(args.input_dir, args.image_dir)
