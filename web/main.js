font_size = 44
furigana = false
translation = false
current_translation_text=""
duration = 0

document.onkeydown = function(evt) {
    evt = evt || window.event;
    //console.log(evt.key)
    if(evt.key == "+" || evt.key == "-") change_font_size(evt.key)
    else eel.handle_key(evt.key)
    if (evt.key != "F12") return false
};

function set_symbol_play_button(symbol){
    let btn = document.getElementById("play_button")
    btn.innerHTML=symbol
}

eel.expose(set_text);
function set_text(text) {
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

function format_time(seconds){
    tmp = parseInt(seconds/3600)
    hours = tmp > 9 ? tmp : "0"+tmp
    seconds = seconds%3600

    tmp = parseInt(seconds/60)
    minutes = tmp > 9 ? tmp : "0"+tmp
    seconds = seconds%60

    seconds = seconds > 9 ? seconds : "0"+seconds

    return `${hours}:${minutes}:${seconds}`
}

eel.expose(set_duration)
function set_duration(seconds) {
    seconds = parseInt(seconds)
    duration = seconds
    let div = document.getElementById("duration")
    div.innerHTML="/ "+format_time(seconds)
}

eel.expose(set_time_pos)
function set_time_pos(seconds) {
    seconds = parseInt(seconds)
    let div = document.getElementById("time_pos")
    div.innerHTML= format_time(seconds)
    div = document.getElementById("time_left")
    div.innerHTML= "-"+format_time(duration-seconds)
}

eel.expose(parse_event);
function parse_event(event){
    if(event == "pause") set_symbol_play_button("▶")
    else if (event == "unpause") set_symbol_play_button("|&nbsp|")
}

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