/**
 * EntryPoint to the tool configurations
 * define menu events and callbacks
 * prompt utilities
 */

var menu;

window.onload = () => {
    let menu = new Menu();
};

document.getElementById('openfile').addEventListener('click', ()=> {
    closePompt();
})


async function raytrace() {
    dialog = new LoadDialog('Rendering Scene');
    dialog.display();
    const canvas = document.querySelector('[active_canvas="true"]');
    let dimensions = getCanvasDimensions();
    let pixels = await eel.raytrace(dimensions)();
    const ctx = canvas.getContext('2d');
    canvas.width = dimensions.width;
    canvas.height = dimensions.height;
    let dataImage = ctx.createImageData(canvas.width, canvas.height);
    dataImage.data.set(pixels);
    ctx.putImageData(dataImage, 0, 0);
    dialog.close();
}

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
