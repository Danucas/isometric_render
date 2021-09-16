document.getElementById('openfile').addEventListener('click', ()=> {
    const filename = document.getElementById('filename').value;
    eel.open_file(filename);
})