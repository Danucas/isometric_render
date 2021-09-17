function getCanvasDimensions() {
    const canvas = document.querySelector('[active_canvas="true"]');
    return canvas.getBoundingClientRect();
}

class Menu {
    constructor() {
        this.barDiv = document.getElementById('menu_bar');
        this.optionsDiv = document.getElementById('menu_options');
        this.tabs = {
            file: {
                options: [
                    {label: 'Open File...', action: () => {}},
                    {label: 'Import...', action: () => {}, tail: true},
                    {label: 'Save...', action: () => {}},
                ]
            },
            edit: {
                options: [
                    {label: 'Undo...', action: () => {}},
                    {label: 'Redo...', action: () => {}},
                ]
            },
            scene: {
                options: [
                    {label: 'Render with Raytracer', action: async()=> {raytrace()}}
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
            li.innerHTML = option.label;
            li.addEventListener('click', async()=>{
                optionsContainer.style.display = 'none';
                option.action();
            });
            optionsContainer.querySelector('ul').appendChild(li);
        }
    }
}