from pytube import YouTube
import os
import time
import argparse
from pytube.utils import print_status
from pprint import pprint
import logging

# [<Video: MPEG-4 Visual (.3gp) - 144p>,
#  <Video: MPEG-4 Visual (.3gp) - 240p>,
#  <Video: Sorenson H.263 (.flv) - 240p>,
#  <Video: H.264 (.flv) - 360p>,
#  <Video: H.264 (.flv) - 480p>,
#  <Video: H.264 (.mp4) - 360p>,
#  <Video: H.264 (.mp4) - 720p>,
#  <Video: VP8 (.webm) - 360p>,
#  <Video: VP8 (.webm) - 480p>]

def download_video(yt, path, file_name):
    if os.path.exists(os.path.join(path, file_name+'.mp4')):
        logging.warning('file %s already exists. Skipped!', str(os.path.join(path, file_name+'.mp4')))
        return
    yt.set_filename(file_name)

    # print(yt.filter('mp4')[-1])
    # pprint(yt.filter(resolution='480p'))
    # video = yt.get('mp4', '720p')
    # video.download()
    # yt.videos[0].download()
    try:
        # yt.videos[0].download(path=os.getcwd(), on_progress=print_status)
        yt.get('mp4', '720p').download(path=path, on_progress=print_status)
    except KeyboardInterrupt:
        logging.error("Download interrupted.")
        print("Download interrupted.")
    # Note: If you wanted to choose the output directory, simply pass it as an
    # argument to the download method.

def main(file_name, output_dir):
    start_time = time.time()
    with open(file_name) as f:
        for line in f:
            if line[0] == "#":
                prev_line = line
                continue
            logging.info("========= DOWNLOAD YOUTUBE VIDEO =========")
            logging.info("Link: %s", str(line[:-1]))
            logging.info("Name: %s", str(prev_line[2:-1]))
            yt = YouTube(line)
            # download_video(yt, os.getcwd(), prev_line[2:])
            download_video(yt, output_dir, prev_line[2:-1])
            prev_line = line
    logging.info("CRAWLER.PY TAKES:"+str(time.time() - start_time)+" seconds")
    return

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("url_file", type=str, help='Path to the url.txt file')
    parser.add_argument("output_dir", type=str, help='Output directory where the downloaded .mp4 files go')
    args = parser.parse_args()

    file_name = args.url_file
    print "file_name is: ", file_name
    main(file_name, output_dir)

