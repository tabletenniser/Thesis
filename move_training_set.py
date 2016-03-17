import time
import argparse
import os
import shutil

CLASSES = ['C1_TOP_PLAYER_FOREHAND_SERVE',
'C2_TOP_PLAYER_BACKHAND_SERVE',
'C3_BOTTOM_PLAYER_FOREHAND_SERVE',
'C4_BOTTOM_PLAYER_BACKHAND_SERVE',
'C5_TOP_PLAYER_FOREHAND_LOOP',
'C6_TOP_PLAYER_BACKHAND_LOOP',
'C7_BOTTOM_PLAYER_FOREHAND_LOOP',
'C8_BOTTOM_PLAYER_BACKHAND_LOOP',
'C9_TOP_PLAYER_FOREHAND_BLOCK',
'C10_TOP_PLAYER_BACKHAND_BLOCK',
'C11_BOTTOM_PLAYER_FOREHAND_BLOCK',
'C12_BOTTOM_PLAYER_BACKHAND_BLOCK',
'C13_TOP_PLAYER_FOREHAND_FLIP',
'C14_TOP_PLAYER_BACKHAND_FLIP',
'C15_BOTTOM_PLAYER_FOREHAND_FLIP',
'C16_BOTTOM_PLAYER_BACKHAND_FLIP',
'C17_TOP_PLAYER_FOREHAND_CHOP',
'C18_TOP_PLAYER_BACKHAND_CHOP',
'C19_BOTTOM_PLAYER_FOREHAND_CHOP',
'C20_BOTTOM_PLAYER_BACKHAND_CHOP',
'C21_TOP_PLAYER_UNDER_NET',
'C22_TOP_PLAYER_HIT_OUT',
'C23_TOP_PLAYER_FOREHAND_MISS_HIT',
'C24_TOP_PLAYER_BACKHAND_MISS_HIT',
'C25_BOTTOM_PLAYER_UNDER_NET',
'C26_BOTTOM_PLAYER_HIT_OUT',
'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT',
'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT',
'C29_TOP_PLAYER_BACKHAND_LOB',
'C30_BOTTOM_PLAYER_BACKHAND_LOB',
'TOP_PLAYER_WINNING',
'BOTTOM_PLAYER_WINNING']

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
