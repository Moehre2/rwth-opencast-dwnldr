# (c) 2020 Moehre2

import os.path
import http.client

outputfolder = ""
playlist_buffer = []

def init(folder):
    global outputfolder
    outputfolder = folder

def check_folder(folder_name):
    if os.path.exists(folder_name):
        if os.path.isfile(folder_name):
            os.remove(folder_name)
    else:
        os.makedirs(folder_name)

def get_playlist(output, guid):
    global playlist_buffer
    conn = http.client.HTTPSConnection("streaming.rwth-aachen.de")
    conn.request("GET", "/rwth/smil:engage-player_" + guid + "_presentation.smil/playlist.m3u8")
    req = conn.getresponse()
    success = (req.status == 200)
    if not success:
        playlist_buffer = []
        print(req.status, req.reason)
    else:
        data = req.read()
        playlist_buffer = data.split(b"\n")
        print(playlist_buffer)
        print("=> playlist.m3u8")
    conn.close()
    return success

def download(video):
    global outputfolder
    print("Download:", video["name"])
    if outputfolder[len(outputfolder) - 1:] == "/":
        output = outputfolder + video["name"]
    else:
        output = outputfolder + "/" + video["name"]
    check_folder(output)
    get_playlist(output, video["guid"])
