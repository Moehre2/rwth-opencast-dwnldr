# (c) 2020 Moehre2

import os.path

outputfolder = ""

def init(folder):
    global outputfolder
    outputfolder = folder

def check_folder(folder_name):
    if os.path.exists(folder_name):
        if os.path.isfile(folder_name):
            os.remove(folder_name)
    else:
        os.makedirs(folder_name)

def download(video):
    global outputfolder
    print("Download:", video["name"])
    if outputfolder[len(outputfolder) - 1:] == "/":
        check_folder(outputfolder + video["name"])
    else:
        check_folder(outputfolder + "/" + video["name"])
