import time
import argparse
import os

def main(input_dir, output_dir):
    print 'move_training_set.py called with:\n', input_dir, '\n', output_dir
    start_time = time.time()

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
