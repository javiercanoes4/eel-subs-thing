import eel, subprocess, json, os, sys, time
from os.path import exists

# def get_correct_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

# web_path = get_correct_path("web")



eel.init('web')

def launch_mpv():
    subprocess.Popen(["mpv","C:\\Users\\T4U\Desktop\\netflix subs\\bisque\\[SubsPlease] Sono Bisque Doll wa Koi wo Suru - 08 (1080p) [ED3FCEAB].mkv", '--input-ipc-server=mpvsocket', r"--geometry=50%+50%+0%", "--volume=50"])

def open_pipe():
    f=open(r'\\.\pipe\mpvsocket', "r+", encoding="utf-8")
    return f

@eel.expose
def test():
    current_line = ""
    launch_mpv()
    time.sleep(1)
    f = open_pipe()
    
    while True:
        f.write(r'{ "command": ["get_property", "sub-text"] }'+'\n')
        f.flush()
        while True:
            res = f.readline()
            #print(res)
            res_dict = json.loads(res)
            if "event" in res_dict: continue
            res_line = res_dict["data"]
            if res_line != current_line:
                # print(res_line)
                current_line = res_line
                eel.testing(current_line)
            break


eel.start('main.html', size=(1366, 400))
