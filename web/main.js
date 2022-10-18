font_size = 44

document.onkeydown = function(evt) {
    evt = evt || window.event;
    //console.log(evt.key)
    if(evt.key == "+" || evt.key == "-") change_font_size(evt.key)
    else eel.handle_key(evt.key)
};

eel.expose(set_text);
function set_text(text) {
    // let folder = document.getElementById('input-box').value;
    // let file_div = document.getElementById('file-name');
    
    // // Call into Python so we can access the file system
    // let random_filename = await eel.pick_file(folder)();
    // file_div.innerHTML = random_filename;
    // console.log(text)
    let div = document.getElementById('main_div');
    div.innerHTML = text
}

async function wrapper_start_video(){
    eel.start_video()
}

function change_font_size(op){
    if(op == "+") font_size+=2
    else font_size-=2
    document.getElementById("body").style.fontSize = `${font_size}px`
}