OpenCast Downloader for RWTHmoodle
==================================

This is a short piece of code for downloading videos from RWTHmoodle. Please execute it in Python3.
It takes two command line arguments:

  * The input file. This is a `.html` file which can be downloaded in the Download Center of RWTHmoodle.
  * The output folder. This is the folder were the downloaded videos will be saved.

The videos won't be converted. This means they will be in the exact format of the server.
Usually there are plenty of `.ts` files that are 10 seconds each and one `.m3u8` file. The `.m3u8` file contains the order of the `.ts` files.
For just playing one of the downloaded videos open the `.m3u8` file in for example [VLC Media Player](http://www.videolan.org/vlc/).