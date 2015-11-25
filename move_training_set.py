import time
import argparse
import os
import shutil

TOP_WINNING_DIRECTORY='top_player_winning'
BOTTOM_WINNING_DIRECTORY='bottom_player_winning'

def create_dir_if_not_exist(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    return

def copy_frames_to_destination(src_dir, destination_dir, start_index):
    index = start_index
    frame_dirs = [os.path.join(src_dir, d) for d in sorted(os.listdir(src_dir)) if os.path.isdir(os.path.join(src_dir, d))]
    for frame_dir in frame_dirs:
        dest_dir = os.path.join(destination_dir, 'point_%05d'%index)
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        print 'Copy ', frame_dir, ' to destionation', dest_dir
        shutil.copytree(frame_dir, dest_dir)
        index+=1
    return index+1


def main(input_dir, output_dir):
    print 'move_training_set.py called with:\n', input_dir, '\n', output_dir
    start_time = time.time()
    # Copy points frames and .mp4 over to the final directory
    top_winning_destination_dir = os.path.join(output_dir, TOP_WINNING_DIRECTORY)
    bottom_winning_destination_dir = os.path.join(output_dir, BOTTOM_WINNING_DIRECTORY)
    create_dir_if_not_exist(top_winning_destination_dir)
    create_dir_if_not_exist(bottom_winning_destination_dir)
    print 'top_winning_destination_dir: ', top_winning_destination_dir
    print 'bottom_winning_destination_dir: ', bottom_winning_destination_dir

    video_dirs = [os.path.join(input_dir, f) for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    print video_dirs
    pt_index_top = 1
    pt_index_bottom = 1
    for video_dir in video_dirs:
        top_winning_source_dir = os.path.join(video_dir, TOP_WINNING_DIRECTORY)
        bottom_winning_source_dir = os.path.join(video_dir, BOTTOM_WINNING_DIRECTORY)
        print 'top_winning_source_dir: ', top_winning_source_dir
        print 'bottom_winning_source_dir: ', bottom_winning_source_dir
        pt_index_top = copy_frames_to_destination(top_winning_source_dir, top_winning_destination_dir, pt_index_top)
        pt_index_bottom = copy_frames_to_destination(bottom_winning_source_dir, bottom_winning_destination_dir, pt_index_bottom)

    print "MOVE_TRAINING_SET.PY TAKES:"+str(time.time()-start_time)+" seconds"
    return

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_training_data_dir", type=str, help='Path to the directory containing a set of folders, one for each video. Each video folder then contains two folders: top_player_winning and bottom_player_winning')
    parser.add_argument("output_dir", type=str, help='Final output directory, containing two folders: top_player_winning and bottom_player_winning')
    args = parser.parse_args()
    args.input_training_data_dir = os.path.abspath(args.input_training_data_dir)
    args.output_dir = os.path.abspath(args.output_dir)
    # Call main function
    main(args.input_training_data_dir, args.output_dir)
