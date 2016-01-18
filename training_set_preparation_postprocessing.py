try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import numpy as np
import shutil

WIDTH = 18
HEIGHT = 18
DELTA_WIDTH = 4
DELTA_HEIGHT = 2
SAMPLE_RATE = 10

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

def main(input_dir, output_image_dir, output_video_dir):
    create_folder_if_not_exist(output_image_dir)
    create_folder_if_not_exist(output_video_dir)
    data = []
    target = []
    folders = [f for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    print 'folders:', folders

    # folders should contain bottom_player_winning and top_player_winning.
    for folder in folders:
        input_folder_path = os.path.join(input_dir, folder)
        image_folders = [f for f in sorted(os.listdir(input_folder_path)) if os.path.isdir(os.path.join(input_folder_path, f))]
        videos = [str(img)+'.mp4' for img in image_folders]
        output_video_path = os.path.join(output_video_dir, folder)
        output_image_path = os.path.join(output_image_dir, folder)
        create_folder_if_not_exist(output_video_path)
        create_folder_if_not_exist(output_image_path)
        # if more than 10 image frames, copy last five images in image_folders to output_image_path,
        # copy videos to output_video_path
        for img_folder in image_folders:
            v = img_folder+'.mp4'
            full_input_folder_name = os.path.join(input_folder_path, img_folder)
            if len(os.listdir(full_input_folder_name)) <= 10:
                continue
            full_video_name = os.path.join(input_folder_path, v)
            full_img_folder_name = os.path.join(output_image_path, img_folder)
            create_folder_if_not_exist(full_img_folder_name)
            output_img_files = os.path.join(full_img_folder_name, "frame_%05d.png")
            if (os.path.isfile(full_video_name)):
                cmd = "ffmpeg -i "+full_video_name+" -vf 'crop=600:600:300:0' -r "+str(SAMPLE_RATE)+" "+output_img_files
                print "DEBUG: image command - ", cmd
                os.system(cmd)
                # ffmpeg -i point_00010.mp4 -vf "crop=600:600:300:0" after.mp4
                cmd = "ffmpeg -i "+full_video_name+" -vf 'crop=600:600:300:0' "+os.path.join(output_video_path,v)
                print "DEBUG: video command - ", cmd
                os.system(cmd)
                # shutil.copy(full_video_name, output_video_path)
        print 'Finish copying to video destination:', output_video_path

        ###### CODE BELOW SELECTS THE LAST 10 FRAMES OF EACH POINT AND PUT INTO THE *_selected FOLDER #####
        output_selected_image_path = os.path.join(output_image_dir, folder+'_selected')
        create_folder_if_not_exist(output_selected_image_path)
        image_folders = [f for f in sorted(os.listdir(output_image_path)) if os.path.isdir(os.path.join(output_image_path, f))]
        for img_folder in image_folders:
            full_output_image_path = os.path.join(output_image_path, img_folder)
            files_to_copy = sorted(os.listdir(full_output_image_path))
            for f in files_to_copy[-10:]:
                src = os.path.join(full_output_image_path, f)
                dest = os.path.join(output_selected_image_path, img_folder+'_'+f)
                print "DEBUG: copy ", src, " to ", dest
                shutil.copy(src, dest)


if __name__=='__main__':
    start_time = time.time()
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing a top_player_winning folder and a bottom_player_winning folder.')
    parser.add_argument("image_dir", type=str, help='Path to the output images from the game.')
    parser.add_argument("video_dir", type=str, help='Path to the output video directory.')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.image_dir = os.path.abspath(args.image_dir)
    args.video_dir = os.path.abspath(args.video_dir)
    main(args.input_dir, args.image_dir, args.video_dir)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
