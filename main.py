import subprocess, json, os, sys, random, threading
# import gevent.monkey
# gevent.monkey.patch_all()
import eel

# def get_correct_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

# web_path = get_correct_path("web")



eel.init('web')

def launch_mpv():
    subprocess.Popen(["mpv","C:\\Users\\T4U\Desktop\\netflix subs\\bisque\\[SubsPlease] Sono Bisque Doll wa Koi wo Suru - 08 (1080p) [ED3FCEAB].mkv", 
    '--input-ipc-server=mpvsocket', r"--geometry=50%+50%+0%", "--volume=50", "--no-audio"])

def open_pipe():
    f=open(r'\\.\pipe\mpvsocket', "r+", encoding="utf-8")
    return f

def close_pipe(f):
    f.close()

def write_keypress(f, key):
    f.write(r'{"command": ["keypress","'+ key +'"]}' + '\n')
    f.flush()

@eel.expose
def start_video():
    # eel.spawn(cock)
    x=threading.Thread(target=launch_and_observe)
    x.start()
    print("Thread started.")

def launch_and_observe():
    # current_line = ""
    launch_mpv()
    eel.sleep(1)
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
    f.write(r'{ "command": ["observe_property", '+ str(id)+ ', "sub-text"]}'+'\n')
    f.flush()

    while True:
        res = f.readline()
        print(res)
        res_dict = json.loads(res)
        if "event" not in res_dict or "id" not in res_dict or res_dict["id"] != id: continue
        if "data" in res_dict: eel.set_text(res_dict["data"])


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
    close_pipe(f)


eel.start('main.html', size=(1366, 400))

while True:
    eel.sleep(1)
    print("REEE")
