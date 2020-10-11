# (c) 2020 Moehre2

import os.path
import shutil
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
        elif os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
            os.makedirs(folder_name)
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
        print("=> playlist.m3u8")
    conn.close()
    return success

def parse_m3u8(output, guid, m3u8file):
    for elem in m3u8file:
        if not elem == b"" and not elem[:1] == b"#":
            download_element(output, guid, elem.decode("utf-8"))

def download_m3u8(output, guid, element):
    conn = http.client.HTTPSConnection("streaming.rwth-aachen.de")
    conn.request("GET", "/rwth/smil:engage-player_" + guid + "_presentation.smil/" + element)
    req = conn.getresponse()
    success = (req.status == 200)
    if not success:
        print(req.status, req.reason)
    else:
        data = req.read();
        with open(output + "/" + element, "wb") as filewriter:
            filewriter.write(data)
            filewriter.close()
        print("=>", element)
        parse_m3u8(output, guid, data.split(b"\n"))
    conn.close()

def download_binary(output, guid, element):
    conn = http.client.HTTPSConnection("streaming.rwth-aachen.de")
    conn.request("GET", "/rwth/smil:engage-player_" + guid + "_presentation.smil/" + element)
    req = conn.getresponse()
    success = (req.status == 200)
    if not success:
        print(req.status, req.reason)
    else:
        with open(output + "/" + element, "wb") as filewriter:
            while chunk := req.read(512):
                filewriter.write(chunk)
            filewriter.close()
        print("=>", element)
    conn.close()

def download_element(output, guid, element):
    if element.endswith(".m3u8"):
        download_m3u8(output, guid, element)
    else:
        download_binary(output, guid, element)

def download_playlist(output, guid):
    global playlist_buffer
    parse_m3u8(output, guid, playlist_buffer)

def download(video):
    global outputfolder
    print("Download:", video["name"])
    if outputfolder[len(outputfolder) - 1:] == "/":
        output = outputfolder + video["name"]
    else:
        output = outputfolder + "/" + video["name"]
    check_folder(output)
    if get_playlist(output, video["guid"]):
        download_playlist(output, video["guid"])
