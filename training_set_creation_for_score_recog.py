try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import numpy as np

WIDTH = 18
HEIGHT = 18
DELTA_WIDTH = 4
DELTA_HEIGHT = 2

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
            print 'Processing image: ', pic
            counter = 0
            im_width, im_height = im.size
            for size in xrange(18, 25):
                for x in xrange(-DELTA_WIDTH, DELTA_WIDTH+1):
                    x_left = (im_width-size)/2+x
                    if x_left < 0 or x_left+size > im_width:
                        continue
                    for y in xrange(-DELTA_HEIGHT, DELTA_HEIGHT+1):
                        y_top = (im_height-size)/2+y
                        if y_top < 0 or y_top+size > im_height:
                            continue
                        im2 = im.crop((x_left, y_top, x_left+size, y_top+size)).convert('L')
                        print 'Create image of square: ', (x_left, y_top, x_left+size, y_top+size)
                        # bw_threshold = 0.3
                        # im_max=np.amax(np.asarray(im2))
                        # im_min=np.amin(np.asarray(im2))
                        # im2 = im2.point(lambda x: 0 if x<((im_max-im_min)*bw_threshold+im_min) else 255, '1')
                        im2 = im2.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
                        im2_array = np.asarray(im2)
                        im2_array_mean = im2_array.mean()
                        im2 = im2.point(lambda x: 0 if x < im2_array_mean else 255, '1')
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
