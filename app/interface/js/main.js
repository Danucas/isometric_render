/**
 * EntryPoint to the tool configurations
 * define menu events and callbacks
 * prompt utilities
 */

var menu;

window.onload = () => {
    let menu = new Menu();
    let tools = new ViewTools();
    tools.mode = tools.MODES.vertices;
    let renderer = new Render(tools);
    
    renderer.wireframe('perspective');
    window.addEventListener('keypress', async function (evn) {
        console.log(evn);
        await eel.key_pressed(evn.key);
        renderer.wireframe('perspective');
    })
    // renderer.raytrace();
};

document.getElementById('openfile').addEventListener('click', ()=> {
    closePompt();
})


function closePompt() {
    const prompt = document.getElementById('prompt');
    prompt.style.display = "none";
}


function openPrompt() {
    const prompt = document.getElementById('prompt');
    prompt.style.display = "block";
}


class LoadDialog {
    constructor(label) {
        this.label = label;
    }

    display() {
        const dialog =  this;
        openPrompt();
        document.getElementById('load_dialog').querySelector('h1').innerHTML = this.label;
        document.getElementById('load_dialog').style.display = 'block';
        let counter = 1;
        this.clockInterval = setInterval(function () {
            let dots = new Array(counter).join('.');
            document.getElementById('load_dialog').querySelector('h1').innerHTML = dialog.label + dots;
            counter++;
            if (counter > 4)
                counter = 1;
        }, 500);
    }

    close() {
        document.getElementById('load_dialog').style.display = 'none';
        closePompt();
    }
}
