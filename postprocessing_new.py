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
    'cls_forehand' : set(['c1_top_player_forehand_serve',
    'c3_bottom_player_forehand_serve',
    'c5_top_player_forehand_loop',
    'c7_bottom_player_forehand_loop',
    'c9_top_player_forehand_block',
    'c11_bottom_player_forehand_block',
    'c13_top_player_forehand_flip',
    'c15_bottom_player_forehand_flip',
    'c17_top_player_forehand_chop',
    'c19_bottom_player_forehand_chop',
    'c21_top_player_forehand_under_net',
    'c22_top_player_forehand_hit_out',
    'c27_bottom_player_forehand_under_net',
    'c28_bottom_player_forehand_hit_out',
    'c34_top_player_forehand_smash']),
    'cls_backhand' : set(['c2_top_player_backhand_serve',
    'c4_bottom_player_backend_serve',
    'c6_top_player_backhand_loop',
    'c8_bottom_player_backend_loop',
    'c10_top_player_backhand_block',
    'c12_bottom_player_backend_block',
    'c14_top_player_backhand_flip',
    'c16_bottom_player_backend_flip',
    'c18_top_player_backhand_chop',
    'c20_bottom_player_backend_chop',
    'c24_top_player_backend_under_net',
    'c25_top_player_backend_hit_out',
    'c30_bottom_player_backend_under_net',
    'c31_bottom_player_backend_hit_out',
    'c33_bottom_player_backend_lob']),
    'cls_top_player_winning' : set(['c27_bottom_player_forehand_under_net',
    'c28_bottom_player_forehand_hit_out',
    'c29_bottom_player_forehand_miss_hit',
    'c30_bottom_player_backend_under_net',
    'c31_bottom_player_backend_hit_out',
    'c32_bottom_player_backend_miss_hit']),
    'cls_bottom_player_winning' : set(['c21_top_player_forehand_under_net',
    'c22_top_player_forehand_hit_out',
    'c23_top_player_forehand_miss_hit',
    'c24_top_player_backend_under_net',
    'c25_top_player_backend_hit_out',
    'c26_top_player_backend_miss_hit'])
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
