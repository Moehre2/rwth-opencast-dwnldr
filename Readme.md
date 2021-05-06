OpenCast Downloader for RWTHmoodle
==================================

This is a short piece of code for downloading videos from RWTHmoodle. Please execute it in Python3.

After not using this piece of software for several months I realized it was pretty messy. So I rewrote it.

## Parameters

The script takes the following parameters:

  * `guid` can be found in the url and looks like `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` where the `x`s are random letters and numbers.
  * `name` is the file/folder name (please enter without endings).
  * `quality` The program lists some qualities it found. For example `max` is always the maximum quality thats possible.
  * `vlc` The program asks if you want to convert the downloaded file(s) with [VLC Media Player](http://www.videolan.org/vlc/).
  * `vlcpath` If you answered `Y` (yes) to the question above please specify the path of your [VLC Media Player](http://www.videolan.org/vlc/) installation.
  * `deleterawfiles` does exactly what it says.

You can also call the script with command line parameters for the listed values. They have to be in the exact order of the list.
