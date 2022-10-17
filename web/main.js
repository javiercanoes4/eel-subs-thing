var current_line="start"

eel.expose(testing);
function testing(text) {
    // let folder = document.getElementById('input-box').value;
    // let file_div = document.getElementById('file-name');
    
    // // Call into Python so we can access the file system
    // let random_filename = await eel.pick_file(folder)();
    // file_div.innerHTML = random_filename;
    console.log(text)
    let div = document.getElementById('main_div');
    div.innerHTML = text
}

async function wrapper_test(){
    eel.test()
}