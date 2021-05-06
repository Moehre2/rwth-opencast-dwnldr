# (c) 2020 - 2021 Moehre2

import sys
import http.client
import os.path
import shutil

playlist_buffer = []

def get_argvar(argnum, argname, text):
    if len(sys.argv) > argnum:
        argvar = sys.argv[argnum]
        print(argname, ":", argvar)
    else:
        print(text)
        argvar = input(argname + " : ")
    return argvar

def get_playlist(guid):
    global playlist_buffer
    conn = http.client.HTTPSConnection("streaming.rwth-aachen.de", timeout=16)
    conn.request("GET", "/rwth/smil:engage-player_" + guid + "_presentation.smil/playlist.m3u8")
    req = conn.getresponse()
    success = (req.status == 200)
    print("Status [" + str(req.status) + "] " + req.reason)
    if success:
        data = req.read()
        playlist_buffer = data.split(b"\n")
    conn.close()
    return success

def check_folder(folder_name):
    if os.path.exists(folder_name):
        if os.path.isfile(folder_name):
            os.remove(folder_name)
        elif os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
            os.makedirs(folder_name)
    else:
        os.makedirs(folder_name)

def main():
    print("rwth-opencast-dwnldr 0.2")
    guid = get_argvar(1, "guid", "Please enter the guid of the video.")
    if not get_playlist(guid):
        exit(1)
    name = get_argvar(2, "name", "Please enter a name for the video (without file endings)")
    check_folder(name)

try:
    main()
except KeyboardInterrupt:
    print("Error: The execution was interrupted")
