# (c) 2020 Moehre2

import sys
import os.path
import html_parser

def parse_file(htmlfile):
    if not html_parser.check_file_ending(htmlfile):
        print("Error: Wrong file ending! Expected html file...")
        sys.exit(3)
    html_parser.parse_file(htmlfile)

def main():
    print("rwth-opencast-dwnldr 0.1")
    inputfile = "";
    if len(sys.argv) == 1:
        inputfile = input("Please enter a file: ")
    elif len(sys.argv) == 2:
        inputfile = sys.argv[1]
    else:
        print("Error: Unknown parameters...")
        sys.exit(1)
    if os.path.exists(inputfile) and os.path.isfile(inputfile):
       parse_file(inputfile)
    else:
        print("Error: Invalid file")
        sys.exit(2)

try:
    main()
except KeyboardInterrupt:
    print("Error: The execution was interrupted")
