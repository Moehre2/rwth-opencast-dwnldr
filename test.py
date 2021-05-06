import subprocess

p = subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", "-I", "dummy", "-vv", "D:\\Coding\\python\\rwth-opencast-dwnldr\\test\\chunklist_w2066121446_b439876.m3u8", "--sout=#transcode{vcodec=h264,vb=1024,acodec=mp4a,ab=192,channels=2,deinterlace}:standard{access=file,mux=ts,dst=D:\\Coding\\python\\rwth-opencast-dwnldr\\MyVid.mp4}", "vlc://quit"])
p.wait()
print(p.returncode)
