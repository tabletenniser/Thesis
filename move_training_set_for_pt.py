import time
import argparse
import os
import shutil

def create_dir_if_not_exist(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    return

def main(input_dir, output_dir):
    print 'move_training_set.py called with:\n', input_dir, '\n', output_dir
    start_time = time.time()

    video_dirs = [os.path.join(input_dir, f) for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    pt_index = 1

    for video_dir in video_dirs:
        pt_dirs = [os.path.join(video_dir, f) for f in sorted(os.listdir(video_dir)) if os.path.isdir(os.path.join(video_dir, f))]
        for pt_dir in pt_dirs:
            if 'POINT' not in pt_dir:
                continue
            dest_dir = os.path.join(output_dir, 'point_%05d'%pt_index)
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(pt_dir, dest_dir)
            print "Copy from ", pt_dir, " to ", dest_dir
            pt_index += 1

    print "MOVE_TRAINING_SET.PY TAKES:"+str(time.time()-start_time)+" seconds"
    return

if __name__== '__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_training_data_dir", type=str, help='Path to the directory containing a set of folders, one for each video. Each video folder then contains a set of POINT_xx folders, each with a label.txt')
    parser.add_argument("output_dir", type=str, help='Final output directory, containing a list of POINT_xx folders, each with a label.txt')
    args = parser.parse_args()
    args.input_training_data_dir = os.path.abspath(args.input_training_data_dir)
    args.output_dir = os.path.abspath(args.output_dir)
    # Call main function
    main(args.input_training_data_dir, args.output_dir)
