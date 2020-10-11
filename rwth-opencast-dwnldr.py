# (c) 2020 Moehre2

import sys
import os.path
import html_parser
import video_downloader

videos = []

def parse_file(htmlfile):
    global videos
    if not html_parser.check_file_ending(htmlfile):
        print("Error: Wrong file ending! Expected html file...")
        sys.exit(3)
    if not html_parser.parse_file(htmlfile):
        print("Error: Could not parse html file...")
        sys.exit(4)
    html_parser.url2guid()
    videos = html_parser.get_parsed_values()
    print("Found", str(len(videos)), "videos(s)...")

def download(folder):
    global videos
    if len(videos) == 0:
        print("Nothing to do...")
    else:
        video_downloader.init(folder)
        for video in videos:
            video_downloader.download(video)

def main():
    print("rwth-opencast-dwnldr 0.1")
    inputfile = "";
    outputfolder = "";
    if len(sys.argv) == 1:
        inputfile = input("Please enter a file: ")
        outputfolder = input("Please enter an output folder: ")
    elif len(sys.argv) == 2:
        inputfile = sys.argv[1]
        outputfolder = input("Please enter an output folder: ")
    elif len(sys.argv) == 3:
        inputfile = sys.argv[1]
        outputfolder = sys.argv[2]
    else:
        print("Error: Unknown parameters...")
        sys.exit(1)
    if os.path.exists(inputfile) and os.path.isfile(inputfile):
       parse_file(inputfile)
       download(outputfolder)
    else:
        print("Error: Invalid file")
        sys.exit(2)

try:
    main()
except KeyboardInterrupt:
    print("Error: The execution was interrupted")
