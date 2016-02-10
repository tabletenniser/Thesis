try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import logging

# writes classified frames in .txt format to output_dir; cropped score images to score_dir
def main(input_frame_dir, input_label_file, output_dir, debug=True):
    start_time = time.time()

    logging.info("COPY_LABLED_FRAME_IMAGES_OVER.PY TAKES:"+str(time.time()-start_time)+" seconds")
    return

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_frame_dir", type=str, help='Path to the directory containing .png frames from the video')
    parser.add_argument("input_label_file", type=str, help='File containing the labels and corresponding set of frame numbers')
    parser.add_argument("output_dir", type=str, help='Training set storage directory. Contain folders, each one is a label specified in input_label_file(e.g top_player_winning and bottom_player_winning)')
    args = parser.parse_args()
    args.input_frame_dir = os.path.abspath(args.input_frame_dir)
    args.input_label_file = os.path.abspath(args.input_label_file)
    args.output_dir = os.path.abspath(args.output_dir)
    main(input_frame_dir, input_label_file, output_dir)

