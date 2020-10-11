# (c) 2020 Moehre2

import sys
import os.path

inputfile = "";

def main():
    print("rwth-opencast-dwnldr 0.1")
    if len(sys.argv) == 1:
        inputfile = input("Please enter a file: ")
    elif len(sys.argv) == 2:
        inputfile = sys.argv[1]
    else:
        print("Error: Unknown parameters...")
        sys.exit(1)
    if os.path.exists(inputfile) and os.path.isfile(inputfile):
       print("Yeah")
    else:
        print("Error: Invalid file")
        sys.exit(2)

try:
    main()
except KeyboardInterrupt:
    print("Error: The execution was interrupted")
