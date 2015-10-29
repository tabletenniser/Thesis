import math, operator
import argparse
import time
import os
from skimage.measure import structural_similarity as ssim
from skimage import color
from skimage import io
from skimage import feature
from PIL import Image

def compare(file1, file2):
    image1 = io.imread(file1, as_grey = True)
    image2 = io.imread(file2, as_grey = True)
    image1 = feature.canny(image1)
    image2 = feature.canny(image2)

    return ssim(image1, image2)

if __name__=='__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=str, help='Path to .jpeg file where the image locates')
    parser.add_argument("images_dir", type=str, help='Path to the directory where the image database locates')
    args = parser.parse_args()
    args.image = os.path.abspath(args.image)
    args.images_dir = os.path.abspath(args.images_dir)
    max_score = -1

    for im in os.listdir(args.images_dir):
        im_file, im_file_extension = os.path.splitext(im)
        if not im_file_extension==".jpg":
            print "file: "+str(im)+" is NOT an image file and skipped"
            continue
        score = compare(args.image, os.path.join(args.images_dir, im))
        if score > max_score:
            max_score = score
            max_image = im
            print "MIN_SCORE_FOUND - Image: "+str(im)+" with score: "+str(score)
        print "Image: "+str(im)+" with score: "+str(score)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
