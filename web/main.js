// const kuroshiro = new Kuroshiro();
// await kuroshiro.init(new KuromojiAnalyzer());
// import Kuroshiro from "./kuroshiro.min.js"

font_size = 44
furigana = false
translation = false
current_translation_text=""

document.onkeydown = function(evt) {
    evt = evt || window.event;
    //console.log(evt.key)
    if(evt.key == "+" || evt.key == "-") change_font_size(evt.key)
    // else if(evt.key == ' ') play_button()
    else eel.handle_key(evt.key)
};

// function play_button(){
//     eel.handle_key(' ')
//     play_button_switch()
// }

// function play_button_switch(){
//     let btn = document.getElementById("play_button")
//     if(btn.innerHTML == "▶") btn.innerHTML="|&nbsp|"
//     else btn.innerHTML = "▶"
// }

function set_symbol_play_button(symbol){
    let btn = document.getElementById("play_button")
    btn.innerHTML=symbol
}

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

eel.expose(set_secondary_text);
function set_secondary_text(text) {
    current_translation_text = text
    if(translation){
        let div = document.getElementById('secondary_div');
        div.innerHTML = current_translation_text
    }
}

eel.expose(parse_event);
function parse_event(event){
    if(event == "pause") set_symbol_play_button("▶")
    else if (event == "unpause") set_symbol_play_button("|&nbsp|")
}


// async function wrapper_start_video(){
//     eel.start_video()
// }

function change_font_size(op){
    if(op == "+") font_size+=2
    else font_size-=2
    document.getElementById("body").style.fontSize = `${font_size}px`
}

function switch_furigana(){
    furigana = !furigana
    eel.set_text()
}

function switch_translation(){
    translation=!translation
    let div = document.getElementById('secondary_div');
    if(translation) div.innerHTML = current_translation_text
    else div.innerHTML = ""
}

eel.expose(check_furigana);
function check_furigana(){
    return furigana
}