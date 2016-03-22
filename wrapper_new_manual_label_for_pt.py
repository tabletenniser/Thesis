import os
import time
import argparse
import crawler
import decompose_ffmpeg
import copy_labeled_frame_images_over_for_pt
import training_set_creation
import construct_clips_structure
import move_training_set_for_pt
import logging
import postprocessing_new_for_pt

def init_logging():
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)15s()] %(levelname)s:%(message)s"
    # FORMAT = "%(asctime)s %(levelname)s:\t%(message)s"
    logging.basicConfig(filename='wrapper_new.log', format=FORMAT, datefmt='%m/%d %H:%M:%S', level=logging.DEBUG)
    logging.info('PROGRAM STARTS')

def create_folder_if_not_exist(path):
    print 'Running create_folder_if_not_exist() with: ', path
    print 'os.path.isdir(): ', os.path.isdir(path)
    print 'os.path.exists(): ', os.path.exists(path)
    if not os.path.isdir(path) and not os.path.exists(path):
        os.makedirs(path)
    return

if __name__ == '__main__':
    init_logging()
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("url_file", type=str, help='Path to the url.txt file')
    parser.add_argument("input_label_dir", type=str, help='Path to directory where the manual label files locate (i.e a list of videoxx_<metadata>.in files)')
    parser.add_argument("inter_dir", type=str, help='Path to the directory where intermediate result goes. Including decomposed frame images, score images and frame pair files.')
    parser.add_argument("output_dir", type=str, help='Output directory where points are separated into top_winning and bottom_winning folders.')
    parser.add_argument("output_labeled_image_dir", type=str, help='Final output directory concatenating all images from different points together and crop them to 600*600. (i.e output from postprocessing_new)')
    parser.add_argument("-s", "--steps", type=str, default='12345', help="steps to perform. 1(crawler) 2(decompose_ffmpeg) 3(copy_labeled_frame_images_over) 4(move_training_set) 5(postprocessing) to perform all steps.")
    parser.add_argument("-m", "--mp4_video_dir", type=str, default='', help="mp4_video_dir")
    parser.add_argument("-f", "--frames_dir", type=str, default='', help="frames_dir")
    args = parser.parse_args()

    if args.mp4_video_dir == '':
        args.mp4_video_dir = os.path.join(args.inter_dir, 'videos')
    if args.frames_dir == '':
        args.frames_dir = os.path.join(args.inter_dir, 'frames')
    # Convert everythign to absolute path to avoid confusion
    args.frames_dir = os.path.abspath(args.frames_dir)
    args.mp4_video_dir = os.path.abspath(args.mp4_video_dir)
    args.url_file = os.path.abspath(args.url_file)
    args.input_label_dir = os.path.abspath(args.input_label_dir)
    args.inter_dir = os.path.abspath(args.inter_dir)
    args.output_dir = os.path.abspath(args.output_dir)
    args.output_labeled_image_dir = os.path.abspath(args.output_labeled_image_dir)

    mp4_video_dir = args.mp4_video_dir
    frames_dir = args.frames_dir
    file_name = args.url_file
    input_label_dir = args.input_label_dir
    ############### STEP 1: CRAWLER.PY ##############
    if '1' in args.steps:
        logging.info("="*20+'STEP #1: CRAWLER.PY'+'='*20)
        create_folder_if_not_exist(mp4_video_dir)
        crawler.main(file_name, mp4_video_dir)
    ############### STEP 2: DECOMPOSE_FFMPEG.PY ##############
    if '2' in args.steps:
        logging.info("="*15+'STEP #2: DECOMPOSE_FFMPEG.PY'+'='*15)
        create_folder_if_not_exist(frames_dir)
        decompose_ffmpeg.main(mp4_video_dir, frames_dir)
    ############### STEP 3: COPY_LABELED_FRAME_IMAGES_OVER_FOR_PT.PY ##############
    if '3' in args.steps:
        training_data_dir = os.path.join(args.inter_dir, 'classified_data_for_pt')
        create_folder_if_not_exist(training_data_dir)
        for fn in os.listdir(frames_dir):
            logging.info("="*15+'STEP #3: COPY_LABELED_FRAME_IMAGES_OVER_FOR_PT.PY'+'='*15)
            input_frame_dir = os.path.join(frames_dir, fn)
            if not os.path.isdir(input_frame_dir):
                continue
            logging.info("input frame folder: %s", input_frame_dir)
            train_subdir = os.path.join(training_data_dir, fn)
            # video_file = os.path.join(mp4_video_dir, str(fn)+'.mp4')
            create_folder_if_not_exist(train_subdir)
            input_label_file = os.path.join(input_label_dir, str(fn)+'.in')
            # copy_labeled_frame_images_over.main(input_frame_dir, video_file, input_label_file, train_subdir)
            copy_labeled_frame_images_over_for_pt.main(input_frame_dir, '', input_label_file, train_subdir)

            # logging.info("="*15+'STEP #4: CONSTRUCT_CLIPS_STRUCTURE.PY'+'='*15)
            # if not os.path.isdir(train_subdir):
            #     os.makedirs(train_subdir)
            # video_file = os.path.join(mp4_video_dir, str(fn)+'.mp4')
            # construct_clips_structure.main(input_frame_dir, video_file, train_subdir)
    ############### STEP 4: MOVE_TRAINING_SET_FOR_PT.PY ##############
    if '4' in args.steps:
        logging.info("="*15+'STEP #4: MOVE_TRAINING_SET_FOR_PT.PY'+'='*15)
        move_training_set_for_pt.main(training_data_dir, args.output_dir)
    ############### STEP 5: POSTPROCESSING_NEW.PY ##############
    if '5' in args.steps:
        logging.info("="*15+'STEP #5: POSTPROCESSING_NEW_FOR_PT.PY'+'='*15)
        postprocessing_new_for_pt.main(args.output_dir, args.output_labeled_image_dir)

