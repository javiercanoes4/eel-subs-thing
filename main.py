import subprocess, json, os, sys, random, threading, math
# import gevent.monkey
# gevent.monkey.patch_all()
import eel

import tkinter as tk
from tkinter import filedialog

from furigana import to_html

# def get_correct_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

# web_path = get_correct_path("web")

# import tkinter as tk
# from tkinter import filedialog

# root = tk.Tk()
# root.withdraw()

windows = os.name == 'nt'
socket_name = "mpvsocket" if windows else "/tmp/mpvsocket"

if not windows: import socket

video_file_path=""
sub_file_path=""
current_sub_text=""
current_secondary_sub_text=""
playing = False
observing = False
current_time=-1

# root = tk.Tk()
# root.withdraw()

# video_file_path = filedialog.askopenfilename(title = "Select video file")
# sub_file_path = filedialog.askopenfilename(title = "Select subtitles file")



eel.init('web')

def launch_mpv():
    args = ["mpv",video_file_path,'--input-ipc-server={}'.format(socket_name), 
    # r"--geometry=50%+50%+0%", 
    "--volume=50",
    "--no-terminal",
    "--secondary-sid=1",
    "--no-secondary-sub-visibility"]
    if sub_file_path: args.append("--sub-file={}".format(sub_file_path))
    subprocess.Popen(args)

def open_pipe():
    if windows:
        f=open(r'\\.\pipe\mpvsocket', "r+", encoding="utf-8")
    else:
        f=socket.socket(family=socket.AF_UNIX)
        f.connect(socket_name)
    return f

def close_pipe(f):
    f.close()

def pipe_read(f):
    if windows: res= f.readline()
    else: res=(f.recv(1024)).decode("utf-8")
    return res

def pipe_write(f,command):
    if windows:
        f.write(command)
        f.flush()
    else:
        f.send(command.encode("utf-8"))

def write_keypress(f, key):
    command = str(r'{"command": ["keypress","'+ key +'"]}' + '\n')
    pipe_write(f,command)

def seek_sub(f,n):
    command = str(r'{"command": ["sub-seek","'+ str(n) +'"]}' + '\n')
    pipe_write(f,command)
    

@eel.expose
def start_video():
    x=threading.Thread(target=launch_and_observe,daemon=True)
    x.start()
    print("Thread started.")

def launch_and_observe():
    launch_mpv()
    eel.sleep(1)
    observe()

@eel.expose
def thread_observe():
    if not observing:
        x=threading.Thread(target=observe,daemon=True)
        x.start()
        print("Thread started.")

def observe():
    f = open_pipe()
    global playing
    global observing
    playing=True
    observing=True

    id_base = random.randint(0,(2**31))
    id_sub_text = id_base+0
    id_secondary_sub_text = id_base+1
    id_duration = id_base+2
    id_time_pos = id_base+3
    command_list = [
    str(r'{ "command": ["observe_property", '+ str(id_sub_text)+ ', "sub-text"]}'+'\n'),
    str(r'{ "command": ["observe_property", '+ str(id_secondary_sub_text)+ ', "secondary-sub-text"]}'+'\n'),
    str(r'{ "command": ["observe_property", '+ str(id_duration)+ ', "duration"]}'+'\n'),
    str(r'{ "command": ["observe_property", '+ str(id_time_pos)+ ', "time-pos"]}'+'\n')
    ]
    for command in command_list:
        pipe_write(f,command)
    global current_sub_text
    global current_secondary_sub_text
    global current_time

    while True:
        res=pipe_read(f)
        print(res)
        try:
            res_dict = json.loads(res)
        except:
            continue
        if "event" in res_dict:
            if "id" in res_dict and res_dict["id"] == id_sub_text:
                if "data" in res_dict: 
                    current_sub_text=res_dict["data"]
                    set_text()
            elif "id" in res_dict and res_dict["id"] == id_secondary_sub_text:
                if "data" in res_dict:
                    current_secondary_sub_text=res_dict["data"]
                    set_secondary_text()
            elif "id" in res_dict and res_dict["id"] == id_duration:
                if "data" in res_dict:
                    eel.set_duration(math.floor(res_dict["data"]))
            elif "id" in res_dict and res_dict["id"] == id_time_pos:
                if "data" in res_dict:
                    seconds = math.floor(res_dict["data"])
                    if seconds!=current_time:
                        current_time = seconds
                        eel.set_time_pos(current_time)
            elif res_dict["event"] == "end-file": break
            else: eel.parse_event(res_dict["event"])

    playing = False
    observing = False
    print("video ended")

@eel.expose
def set_text():
    furigana = eel.check_furigana()()
    # print(furigana)
    if furigana:
        eel.set_text(to_html(current_sub_text.replace(" ", " ").replace("\n","<br>")))
    else:
        eel.set_text(current_sub_text.replace("\n","<br>"))

def set_secondary_text():
    eel.set_secondary_text(current_secondary_sub_text.replace("\n","<br>"))

@eel.expose
def handle_key(key):
    f = open_pipe()
    if key == " ":
        write_keypress(f,"SPACE")
    elif key == "ArrowRight":
        write_keypress(f,"RIGHT")
    elif key == "ArrowLeft":
        write_keypress(f,"LEFT")
    elif key == "0":
        write_keypress(f,"0")
    elif key == "9":
        write_keypress(f,"9")
    elif key == "j":
        write_keypress(f,"j")
    elif key == "q":
        write_keypress(f,"q")
    close_pipe(f)

@eel.expose
def handle_sub_seek(n):
    f = open_pipe()
    seek_sub(f,n)
    close_pipe(f)

@eel.expose
def open_video():
    if not playing:
        global video_file_path
        global sub_file_path
        root = tk.Tk()
        root.title("How does one hide this earlier??")
        f1= tk.Frame(root, height=0, width=0)
        f1.pack()
        video_file_path = filedialog.askopenfilename(title = "Select video file")
        root.withdraw()
        sub_file_path = filedialog.askopenfilename(title = "Select subtitles file")
        root.destroy()
        if video_file_path != "":
            start_video()

eel.start('main.html', size=(1366, 800), block=True)

while True:
    eel.sleep(1)
