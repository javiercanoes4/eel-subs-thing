import subprocess, json, os, sys, random, threading
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

# root = tk.Tk()
# root.withdraw()

# video_file_path = filedialog.askopenfilename(title = "Select video file")
# sub_file_path = filedialog.askopenfilename(title = "Select subtitles file")



eel.init('web')

def launch_mpv():
    args = ["mpv",video_file_path,'--input-ipc-server={}'.format(socket_name), 
    # r"--geometry=50%+50%+0%", 
    "--volume=50",
    "--no-terminal"]
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

def write_keypress(f, key):
    command = str(r'{"command": ["keypress","'+ key +'"]}' + '\n')
    if windows:
        f.write(command)
        f.flush()
    else:
        f.send(command.encode("utf-8"))
    

@eel.expose
def start_video():
    # eel.spawn(cock)
    x=threading.Thread(target=launch_and_observe,daemon=True)
    x.start()
    print("Thread started.")

def launch_and_observe():
    launch_mpv()
    eel.sleep(1)
    observe()

@eel.expose
def thread_observe():
    x=threading.Thread(target=observe,daemon=True)
    x.start()
    print("Thread started.")

def observe():
    f = open_pipe()
    
    # while True:
    #     time.sleep(0.1)
    #     id = random.randint(0,(2**32))
    #     f.write(r'{ "command": ["get_property", "sub-text"], "request_id":' + str(id)+ '}'+'\n')
    #     f.flush()
    #     while True:
    #         res = f.readline()
    #         #print(res)
    #         res_dict = json.loads(res)
    #         if "request_id" not in res_dict or res_dict["request_id"] != id: continue
    #         if "error" in res_dict and res_dict["error"] != "success": break
    #         #print(res_dict)
    #         res_line = res_dict["data"]
    #         if res_line != current_line:
    #             # print(res_line)
    #             current_line = res_line
    #             eel.testing(current_line)
    #         break

    id = random.randint(0,(2**32))
    command = str(r'{ "command": ["observe_property", '+ str(id)+ ', "sub-text"]}'+'\n')
    if windows:
        f.write(command)
        f.flush()
    else:
        f.send(command.encode("utf-8"))
    global current_sub_text

    while True:
        if windows: res = f.readline()
        else: res = (f.recv(1024)).decode("utf-8")
        print(res)
        try:
            res_dict = json.loads(res)
        except:
            continue
        if "event" in res_dict:
            if "id" in res_dict and res_dict["id"] == id:
                if "data" in res_dict: 
                    current_sub_text=res_dict["data"]
                    set_text()
                    # eel.set_text(to_html(res_dict["data"].replace(" ", " ").replace("\n","<br>")))
            else: eel.parse_event(res_dict["event"])


        # if "event" not in res_dict or "id" not in res_dict or res_dict["id"] != id: continue
        # if "data" in res_dict: eel.set_text(to_html(res_dict["data"].replace(" ", " ").replace("\n","<br>")))

@eel.expose
def set_text():
    furigana = eel.check_furigana()()
    print(furigana)
    if furigana:
        eel.set_text(to_html(current_sub_text.replace(" ", " ").replace("\n","<br>")))
    else:
        eel.set_text(current_sub_text.replace("\n","<br>"))

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
def open_video():
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
    start_video()

# keke()
eel.start('main.html', size=(1366, 800), block=True)

while True:
    eel.sleep(1)
