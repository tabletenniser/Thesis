try:
    import Image
except ImportError:
    from PIL import Image
from PIL import ImageEnhance
import time
import argparse
import os


WIDTH = 20
HEIGHT = 20
DELTA_WIDTH = 4
DELTA_HEIGHT = 4

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

def main(input_dir, output_dir):
    create_folder_if_not_exist(output_dir)
    data = []
    target = []
    folders = [f for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    print 'folders:', folders
    for folder in folders:
        input_folder_path = os.path.join(input_dir, folder)
        output_folder_path = os.path.join(output_dir, folder)
        create_folder_if_not_exist(output_folder_path)
        print 'folder: ', folder
        input_images = [d for d in sorted(os.listdir(input_folder_path)) if d.endswith('png')]
        print 'images: ', input_images
        im_counter = 0
        for pic in input_images:
            # if not pic.endswith('png'):
            #     continue
            im = Image.open(os.path.join(input_folder_path, pic))
            counter = 0
            for x in xrange(DELTA_WIDTH):
                for y in xrange(DELTA_HEIGHT):
                    im2 = im.crop((x, y, x+WIDTH, y+HEIGHT)).convert('1')
                    im2.save(os.path.join(output_folder_path, "%d_%d_%02d.png" % (int(folder), im_counter, counter)))
                    counter+=1
            im_counter += 1

if __name__=='__main__':
    start_time = time.time()
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing 24*24 training images. Consist of folders from 0 to 15, each containing at least 5 images.')
    parser.add_argument("output_dir", type=str, help='Path to the output directory of the same directory structure but each digit folder contains 20*20 images with different horizontal and vertical shifts..')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)
    main(args.input_dir, args.output_dir)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
