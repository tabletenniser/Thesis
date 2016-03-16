try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import sys
import logging

# Copy frames images specified by input_label_file to the corresponding folder in output_dir
def main(input_label_file, output_label_file):
    perform_start_time = time.time()

    frame_class_tuple = []  # A list of tuples in the form of (start_frame, end_frame, class)
    with open(input_label_file) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                continue

            frames = line.split(':')
            # case where a label instead of the actual frame range
            if len(frames)!=2:
                output_class = line.upper()
                continue

            # Case where the actual point data - COPY OVER THE IMAGES
            frames[0] = int(frames[0])
            frames[1] = int(frames[1])
            frame_class_tuple.append((frames[0], frames[1], output_class))
    frame_class_tuple.sort()
    pt_index = 0
    prev_finish_ind = 0

    with open(output_label_file, 'w+') as f:
        for tup in frame_class_tuple:
            if tup[0] > prev_finish_ind+1:
                pt_index +=1
                f.write('\n#POINT_%d\n'%(pt_index))
            f.write('%d:%d:%s\n'%(tup[0], tup[1], tup[2]))
            prev_finish_ind = tup[1]

    return

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_label_file", type=str, help='File containing the labels and corresponding set of frame numbers')
    parser.add_argument("output_label_file", type=str, help='File containing the labels and corresponding set of frame numbers')
    args = parser.parse_args()
    args.input_label_file = os.path.abspath(args.input_label_file)
    args.output_label_file = os.path.abspath(args.output_label_file)

    ########## Initialize the logging to stdout
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)
    logging=log

    ######### Call main function to perform the copies
    main(args.input_label_file, args.output_label_file)
