function getCanvasDimensions() {
    const view = document.querySelector('[active_canvas="true"]');
    return view.querySelector('canvas').getBoundingClientRect();
}

class Menu {
    constructor() {
        this.DEV_STATUSES = {
            1: {def: 'Not Implemented', color: 'grey'},
            2: {def: 'In develop', color: 'yellow'},
            3: {def: 'Completed', color: 'green'},
        }
        this.barDiv = document.getElementById('menu_bar');
        this.optionsDiv = document.getElementById('menu_options');
        this.tabs = {
            file: {
                options: [
                    {label: 'Open File...', action: () => {}, status: 1},
                    {label: 'Import...', action: () => {}, status: 1, tail: true},
                    {label: 'Save...', action: () => {}, status: 1},
                ]
            },
            edit: {
                options: [
                    {label: 'Undo...', action: () => {}, status: 1},
                    {label: 'Redo...', action: () => {}, status: 1},
                ]
            },
            scene: {
                options: [
                    {label: 'Render with Raytracer', action: async()=> {raytrace()}, status: 3}
                ]
            },
        }
        for (const li of this.barDiv.querySelectorAll('li')) {
            li.addEventListener('click', (evn) => { this.drawMenu(evn.target, li.getAttribute('tab')) });
        }
        const context = this;
        document.addEventListener('click', function(event) {
            var isClickInsideElement = context.optionsDiv.contains(event.target);
            var isClickInMenu = context.barDiv.contains(event.target)
            if (!isClickInsideElement && !isClickInMenu) {
                console.log(isClickInsideElement, isClickInMenu);
                context.optionsDiv.style.display = 'none';
            }
        });
    }

    drawMenu(element, tab) {
        let context = this;
        // Get and display the menu options container in the correct position
        let optionsContainer = this.optionsDiv;
        optionsContainer.querySelector('ul').innerHTML = "";
        optionsContainer.style.display = 'block';
        optionsContainer.style.left = Math.round(element.getBoundingClientRect().left) + 'px';

        // Apply the events to each option
        for (const option of this.tabs[tab].options) {
            let li = document.createElement('li');
            li.innerHTML = `<i style="background-color: ${context.DEV_STATUSES[option.status].color}"></i>${option.label}`;
            li.addEventListener('click', async()=>{
                optionsContainer.style.display = 'none';
                option.action();
            });
            optionsContainer.querySelector('ul').appendChild(li);
        }
    }
}