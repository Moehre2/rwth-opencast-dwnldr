# (c) 2020 - 2021 Moehre2

import sys
import http.client
import os
import shutil
import math
import subprocess

playlist_buffer = []
qualities = []

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

def list_qualities():
    global playlist_buffer, qualities
    temp = []
    for elem in playlist_buffer:
        if elem == b"":
            pass
        elif elem[:17] == b"#EXT-X-STREAM-INF":
            temp = elem[18:].lower().split(b",")
        elif elem[:1] != b"#":
            qualities.append({"terms": temp, "link": elem})
    resolutions = []
    for q in qualities:
        res = 0
        for t in q["terms"]:
            if t[:11] == b"resolution=":
                temp = t[11:].split(b"x")
                if len(temp) == 2:
                    res = int(temp[0]) * int(temp[1])
        resolutions.append(res)
    minres = min(resolutions)
    maxres = max(resolutions)
    mini = maxi = -1
    for i in range(0, len(resolutions)):
        if resolutions[i] == 0:
            pass
        elif resolutions[i] == minres:
            mini = i
        elif resolutions[i] == maxres:
            maxi = i
    qualities[mini]["terms"].append(b"min")
    qualities[maxi]["terms"].append(b"max")
    for i in range(0, len(qualities)):
        line = str(i) + ")"
        for t in qualities[i]["terms"]:
            line = line + " " + t.decode("utf-8")
        print(line)

def get_quality_index(quality):
    global qualities
    for i in range(0, len(qualities)):
        if quality == str(i):
            return i
        else:
            for t in qualities[i]["terms"]:
                if quality == t.decode("utf-8"):
                    return i
    return -1

def download_part(guid, name, part):
    conn = http.client.HTTPSConnection("streaming.rwth-aachen.de")
    conn.request("GET", "/rwth/smil:engage-player_" + guid + "_presentation.smil/" + part)
    req = conn.getresponse()
    success = (req.status == 200)
    if success:
        data = req.read()
        with open(name + "/" + part, "wb") as filewriter:
            filewriter.write(data)
            filewriter.close()
    conn.close()
    return success

def download_elements(guid, name, elements):
    parts = []
    for elem in elements:
        if elem != b"" and elem[:1] != b"#":
            parts.append(elem)
    progress = 0
    parts_len = len(parts)
    print("[", end="", flush=True)
    for i in range(0, parts_len):
        download_part(guid, name, parts[i].decode("utf-8"))
        if math.floor(i / parts_len * 33) - progress > 0:
            print("=", end="", flush=True)
        progress = math.floor(i / parts_len * 33)
    print("]")

def download_m3u8(guid, name, element):
    conn = http.client.HTTPSConnection("streaming.rwth-aachen.de")
    conn.request("GET", "/rwth/smil:engage-player_" + guid + "_presentation.smil/" + element)
    req = conn.getresponse()
    success = (req.status == 200)
    print("Status [" + str(req.status) + "] " + req.reason)
    if success:
        data = req.read()
        with open(name + "/" + element, "wb") as filewriter:
            filewriter.write(data)
            filewriter.close()
        download_elements(guid, name, data.split(b"\n"))
    conn.close()
    return success

def vlc_convert(vlcpath, name, element):
    vlccmd = [vlcpath, "-I", "dummy", "-vv", os.path.join(os.getcwd(), name, element), "--sout=#transcode{vcodec=h264,vb=1024,acodec=mp4a,ab=192,channels=2,deinterlace}:standard{access=file,mux=ts,dst=" + os.path.join(os.getcwd(), name + ".mp4") + "}", "vlc://quit"]
    print("Converting the video. This may take some time...")
    p = subprocess.Popen(vlccmd)
    p.wait()
    return p.returncode

def delete_raw_files(name):
    if os.path.exists(name) and os.path.isdir(name):
        shutil.rmtree(name)

def main():
    global qualities
    print("rwth-opencast-dwnldr 0.2")
    guid = get_argvar(1, "guid", "Please enter the guid of the video.")
    if not get_playlist(guid):
        exit(2)
    name = get_argvar(2, "name", "Please enter a name for the video (without file endings)")
    check_folder(name)
    list_qualities()
    quality = get_argvar(3, "quality", "Please enter one of the qualities")
    qindex = get_quality_index(quality)
    if qindex < 0:
        print("Cannot find the specified quality")
        exit(3)
    print("Starting download...")
    element = qualities[qindex]["link"].decode("utf-8")
    if not download_m3u8(guid, name, element):
        exit(4)
    vlc = get_argvar(4, "vlc", "Do you want to convert the downloaded files with VLC Media Player (Y/n)")
    if vlc == "n":
        exit(0)
    elif vlc != "Y":
        print("Unknown option. Aborting.")
        exit(5)
    vlcpath = get_argvar(5, "vlcpath", "Please enter the VLC path (leave empty to load from path envvar)")
    if vlcpath == "":
        vlcpath = "vlc"
    if vlc_convert(vlcpath, name, element) != 0:
        print("Error while converting!")
        exit(6)
    deleterawfiles = get_argvar(6, "deleterawfiles", "Do you want to delete the raw files and just keep the converted video? (Y/n)")
    if deleterawfiles == "n":
        exit(0)
    elif deleterawfiles != "Y":
        print("Unknown option. Aborting.")
        exit(6)
    delete_raw_files(name)

try:
    main()
except KeyboardInterrupt:
    print("Error: The execution was interrupted")
    exit(1)
