import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse
import time
import os

if __name__=='__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("images_dir", type=str, help='Path to the directory where the image database locates')
    args = parser.parse_args()
    args.images_dir = os.path.abspath(args.images_dir)
    count = 0


    for im in os.listdir(args.images_dir):
        im_file, im_file_extension = os.path.splitext(im)
        if not im_file_extension==".jpg":
            print "file: "+str(im)+" is NOT an image file and skipped"
            continue
        count += 1
        if count > 1:
            break
        path = os.path.join(args.images_dir, im)
        img = cv2.imread(path,0)
        edges = cv2.Canny(img,10,20)
        print edges
        cv2.imwrite(os.path.join(args.images_dir, "test.jpg"), edges)
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        plt.show()
        print "Image: "+str(im)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
