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
    print 'folders:', folders   # This should be a list of POINT_xx

    for folder in folders:
        if 'point' not in folder.lower():
            continue
        full_input_folder_name = os.path.join(input_dir, folder)
        full_img_folder_name = os.path.join(output_image_dir, folder)
        create_folder_if_not_exist(full_img_folder_name)

        # Loop over frames
        for img_file in os.listdir(full_input_folder_name):
            if 'png' not in img_file.lower():
                if img_file.lower() == 'label.txt':
                    img_file_full_path = os.path.join(full_input_folder_name, img_file)
                    shutil.copy(img_file_full_path, full_img_folder_name)
                    print 'copy ', img_file_full_path, ' to ', full_img_folder_name
                continue
            ii = Image.open(os.path.join(full_input_folder_name, img_file))
            box = (300, 0, 900, 600)
            region = ii.crop(box)
            region.save(os.path.join(full_img_folder_name, img_file))
            print 'save cropped image to', os.path.join(full_img_folder_name, img_file)

    return

def main(input_dir, image_dir):
    start_time = time.time()
    crop_size_for_video_and_images(input_dir, image_dir)
    # select_images(args.image_dir, args.audio_dir)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing a set of points, each containing a set of .png files and a label.txt')
    parser.add_argument("image_dir", type=str, help='Path to the output directory.')
    # parser.add_argument("audio_dir", type=str, help='Path to the output audio directory.')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.image_dir = os.path.abspath(args.image_dir)
    # args.audio_dir = os.path.abspath(args.audio_dir)
    main(args.input_dir, args.image_dir)
