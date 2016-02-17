import time
import argparse
import os
import shutil

CLASSES = ['c1_top_player_forehand_serve',
'c2_top_player_backhand_serve',
'c3_bottom_player_forehand_serve',
'c4_bottom_player_backend_serve',
'c5_top_player_forehand_loop',
'c6_top_player_backhand_loop',
'c7_bottom_player_forehand_loop',
'c8_bottom_player_backend_loop',
'c9_top_player_forehand_block',
'c10_top_player_backhand_block',
'c11_bottom_player_forehand_block',
'c12_bottom_player_backend_block',
'c13_top_player_forehand_flip',
'c14_top_player_backhand_flip',
'c15_bottom_player_forehand_flip',
'c16_bottom_player_backend_flip',
'c17_top_player_forehand_chop',
'c18_top_player_backhand_chop',
'c19_bottom_player_forehand_chop',
'c20_bottom_player_backend_chop',
'c21_top_player_forehand_under_net',
'c22_top_player_forehand_hit_out',
'c23_top_player_forehand_miss_hit',
'c24_top_player_backend_under_net',
'c25_top_player_backend_hit_out',
'c26_top_player_backend_miss_hit',
'c27_bottom_player_forehand_under_net',
'c28_bottom_player_forehand_hit_out',
'c29_bottom_player_forehand_miss_hit',
'c30_bottom_player_backend_under_net',
'c31_bottom_player_backend_hit_out',
'c32_bottom_player_backend_miss_hit',
'c33_bottom_player_backend_lob',
'c34_top_player_forehand_smash',
'top_player_winning',
'bottom_player_winning']

def create_dir_if_not_exist(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    return

def copy_frames_to_destination(src_dir, destination_dir, start_index):
    index = start_index
    frame_dirs = [os.path.join(src_dir, d) for d in sorted(os.listdir(src_dir)) if os.path.isdir(os.path.join(src_dir, d))]
    for frame_dir in frame_dirs:
        basename = os.path.basename(os.path.normpath(frame_dir))
        # DO NOT COPY .mp4 VIDEOS FOR NOW
        # mp4_file_src = os.path.join(src_dir, basename+'.mp4')
        # if os.path.exists(mp4_file_src):
        #     mp4_file_dest = os.path.join(destination_dir, 'point_%05d.mp4'%index)
        #     shutil.copy(mp4_file_src, mp4_file_dest)
        #     print 'Copy mp4 file ', mp4_file_src, ' to destionation', mp4_file_dest
        dest_dir = os.path.join(destination_dir, 'point_%05d'%index)
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        print 'Copy folder ', frame_dir, ' to destionation', dest_dir
        shutil.copytree(frame_dir, dest_dir)
        index+=1
    return index


def main(input_dir, output_dir):
    print 'move_training_set.py called with:\n', input_dir, '\n', output_dir
    start_time = time.time()
    # Copy points frames and .mp4 over to the final directory
    destination_folders = []
    for cls in CLASSES:
        destination_folders.append(os.path.join(output_dir, cls))
        create_dir_if_not_exist(os.path.join(output_dir, cls))

    video_dirs = [os.path.join(input_dir, f) for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    # print video_dirs
    indices = [1 for _ in xrange(len(CLASSES))]
    pt_index_top = 1
    pt_index_bottom = 1
    for video_dir in video_dirs:
        # for cls in CLASSES:
        for i in xrange(len(CLASSES)):
            source_dir = os.path.join(video_dir, CLASSES[i])
            if os.path.exists(source_dir):
                indices[i] = copy_frames_to_destination(source_dir, destination_folders[i], indices[i])

    print "MOVE_TRAINING_SET.PY TAKES:"+str(time.time()-start_time)+" seconds"
    return

if __name__== '__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_training_data_dir", type=str, help='Path to the directory containing a set of folders, one for each video. Each video folder then contains two folders: top_player_winning and bottom_player_winning')
    parser.add_argument("output_dir", type=str, help='Final output directory, containing two folders: top_player_winning and bottom_player_winning')
    args = parser.parse_args()
    args.input_training_data_dir = os.path.abspath(args.input_training_data_dir)
    args.output_dir = os.path.abspath(args.output_dir)
    # Call main function
    main(args.input_training_data_dir, args.output_dir)
