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
def main(input_label_file):
    last_finish_time = 0
    last_is_top_player = 0
    with open(input_label_file) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                last_finish_time = 0
                continue

            frames = line.split(':')
            # case where a label instead of the actual frame range
            if len(frames)!=3:
                print 'WARNING: line #%d: %s is NOT properly formated'%(i, line)
                continue

            # Case where the actual point data - COPY OVER THE IMAGES
            if last_finish_time != 0:
                if int(frames[0]) != last_finish_time:
                    print 'WARNING: %d != %d'%(int(frames[0]), last_finish_time)
                if 'TOP_PLAYER' in frames[2] and last_is_top_player == 1 and not 'HIT_OUT' in frames[2] and not 'UNDER_NET' in frames[2]:
                    print 'WARNING: %s contains TOP_PLAYER'%(line)
                if 'BOTTOM_PLAYER' in frames[2] and last_is_top_player == 0 and not 'HIT_OUT' in frames[2] and not 'UNDER_NET' in frames[2]:
                    print 'WARNING: %s contains BOTTOM_PLAYER'%(line)

            last_finish_time = int(frames[1])
            if 'TOP_PLAYER' in frames[2]:
                last_is_top_player = 1
            else:
                last_is_top_player = 0
    print "INFO: VALIDATION CHECK FINISHES!!!"

    return

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_label_file", type=str, help='.in file of the manual labeling')
    args = parser.parse_args()
    args.input_label_file = os.path.abspath(args.input_label_file)

    ########## Initialize the logging to stdout
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)
    logging=log

    ######### Call main function to perform the copies
    main(args.input_label_file)
