try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import numpy as np
import shutil

mix_classes = {
    'cls_forehand' : SET(['C1_TOP_PLAYER_FOREHAND_SERVE',
    'C3_BOTTOM_PLAYER_FOREHAND_SERVE',
    'C5_TOP_PLAYER_FOREHAND_LOOP',
    'C7_BOTTOM_PLAYER_FOREHAND_LOOP',
    'C9_TOP_PLAYER_FOREHAND_BLOCK',
    'C11_BOTTOM_PLAYER_FOREHAND_BLOCK',
    'C13_TOP_PLAYER_FOREHAND_FLIP',
    'C15_BOTTOM_PLAYER_FOREHAND_FLIP',
    'C17_TOP_PLAYER_FOREHAND_CHOP',
    'C19_BOTTOM_PLAYER_FOREHAND_CHOP']),
    'cls_backhand' : SET(['C2_TOP_PLAYER_BACKHAND_SERVE',
    'C4_BOTTOM_PLAYER_BACKHAND_SERVE',
    'C6_TOP_PLAYER_BACKHAND_LOOP',
    'C8_BOTTOM_PLAYER_BACKHAND_LOOP',
    'C10_TOP_PLAYER_BACKHAND_BLOCK',
    'C12_BOTTOM_PLAYER_BACKHAND_BLOCK',
    'C14_TOP_PLAYER_BACKHAND_FLIP',
    'C16_BOTTOM_PLAYER_BACKHAND_FLIP',
    'C18_TOP_PLAYER_BACKHAND_CHOP',
    'C20_BOTTOM_PLAYER_BACKHAND_CHOP']),
    'cls_top_player_winning' : SET(['C25_BOTTOM_PLAYER_UNDER_NET',
    'C26_BOTTOM_PLAYER_HIT_OUT',
    'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT',
    'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT']),
    'cls_bottom_player_winning' : SET(['C21_TOP_PLAYER_UNDER_NET',
    'C22_TOP_PLAYER_HIT_OUT',
    'C23_TOP_PLAYER_FOREHAND_MISS_HIT',
    'C24_TOP_PLAYER_BACKHAND_MISS_HIT'])
    }

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

def crop_size_for_video_and_images(input_dir, output_image_dir):
    create_folder_if_not_exist(output_image_dir)
    folders = [f for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    print 'folders:', folders   # This should be a list of stroke classes
    mix_classes_pt_counter = {'cls_forehand': 0, 'cls_backhand': 0, 'cls_top_player_winning': 0, 'cls_bottom_player_winning': 0}

    # folders should contain bottom_player_winning and top_player_winning.
    for folder in folders:
        input_folder_path = os.path.join(input_dir, folder)
        image_folders = [f for f in sorted(os.listdir(input_folder_path)) if os.path.isdir(os.path.join(input_folder_path, f))]
        output_image_path = os.path.join(output_image_dir, folder)
        create_folder_if_not_exist(output_image_path)
        mix_classes_output_image_path = []
        for key in mix_classes:
            if folder in mix_classes[key]:
                mix_classes_output_image_path.append(os.path.join(output_image_dir, key))
                create_folder_if_not_exist(os.path.join(output_image_dir, key))
        print 'mix_classes_output_image_path for ', folder, ' is ', mix_classes_output_image_path

        # if more than 10 image frames, crop them and copy over into one folder
        # Loop over points
        for img_folder in image_folders:
            full_input_folder_name = os.path.join(input_folder_path, img_folder)
            if len(os.listdir(full_input_folder_name)) <= 10:
                continue
            full_img_folder_name = os.path.join(output_image_path, img_folder)
            create_folder_if_not_exist(full_img_folder_name)
            mix_classes_full_img_folder_name = [None for _ in xrange(len(mix_classes_output_image_path))]
            # loop over all hyper-classes and create_folder_if_not_exist
            for i in xrange(len(mix_classes_output_image_path)):
                print mix_classes_output_image_path[i]
                print os.path.basename(mix_classes_output_image_path[i])
                # mix_classes_full_img_folder_name[i] = os.path.join(mix_classes_output_image_path[i], img_folder)
                mix_classes_full_img_folder_name[i] = os.path.join(mix_classes_output_image_path[i], 'point_%05d'%(mix_classes_pt_counter[os.path.basename(mix_classes_output_image_path[i])]))
                mix_classes_pt_counter[os.path.basename(mix_classes_output_image_path[i])] += 1
                create_folder_if_not_exist(mix_classes_full_img_folder_name[i])
            # Loop over frames
            for img_file in os.listdir(full_input_folder_name):
                ii = Image.open(os.path.join(full_input_folder_name, img_file))
                box = (300, 0, 900, 600)
                region = ii.crop(box)
                region.save(os.path.join(full_img_folder_name, img_file))
                for i in xrange(len(mix_classes_full_img_folder_name)):
                    region.save(os.path.join(mix_classes_full_img_folder_name[i], img_file))
                    print 'save cropped image to mix class', os.path.join(mix_classes_full_img_folder_name[i], img_file)
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
