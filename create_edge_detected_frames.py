import argparse
import time
import os
from skimage.measure import structural_similarity as ssim
from skimage import color
from skimage import io
from skimage import feature

def compare(file1, file2):
    image1 = io.imread(file1, as_grey = True)
    image2 = io.imread(file2, as_grey = True)
    image1 = feature.canny(image1)
    image2 = feature.canny(image2)

    return ssim(image1, image2)

if __name__=='__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to .jpeg file where the image locates')
    parser.add_argument("output_dir", type=str, help='Output path for the edge detected images')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)

    for im in os.listdir(args.input_dir):
        im_file, im_file_extension = os.path.splitext(im)
        if not im_file_extension==".jpg":
            print "file: "+str(im)+" is NOT an image file and skipped"
            continue
        image = io.imread(os.path.join(args.input_dir, im), as_grey = True)
        output_image = feature.canny(image)
        output_file = os.path.join(args.output_dir, im)
        io.imsave(output_file, output_image.astype(float))
        print "saving to output file "+str(output_file)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
