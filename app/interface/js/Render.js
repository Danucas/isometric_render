/**
 * Takes control over canvas drawing and procces logging
 */
class Render {
    constructor(tools) {
        this.canvas = document.querySelector('[active_canvas="true"]').querySelector('canvas');
        this.tools = tools
    }


    log(text) {
        this.console.log(text);
    }


    async raytrace() {
        // Get dimensions from canvas
        const canvas = this.canvas;
        let dimensions = getCanvasDimensions();

        // Calculate the pixels Python side
        let pixels = await eel.raytrace(dimensions)();
    
        // Draw the pixels in canvas
        const ctx = canvas.getContext('2d');
        canvas.width = dimensions.width;
        canvas.height = dimensions.height;
        let dataImage = ctx.createImageData(canvas.width, canvas.height);
        dataImage.data.set(pixels);
        ctx.putImageData(dataImage, 0, 0);
    }


    async wireframe(type) {
        // Get dimensions from canvas
        const canvas = this.canvas;
        let dimensions = getCanvasDimensions();
        let objects;

        // Calculate the pixels Python side
        if (type == 'perspective') {
            objects = await eel.perspective(dimensions)();
        } else {
            objects = await eel.ortho(dimensions)();
        }
        
    
        console.log(objects);

        var ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, dimensions.width * 2, dimensions.height * 2);

        if (this.tools.mode == this.tools.MODES.hedges) {
            ctx.strokeStyle = 'orange';
            ctx.fillStyle = 'white';
        } else {
            ctx.strokeStyle = 'white';
            ctx.fillStyle = 'orange';
        }
        for (let object of objects) {
            for (let face of object.faces) {
                ctx.beginPath();
                ctx.moveTo(face[0][0], face[0][1]);
                for (let vertex of face) {
                    ctx.lineTo(vertex[0], vertex[1]);
                }
                ctx.lineTo(face[0][0], face[0][1]);
                if (this.tools.mode == this.tools.MODES.faces) {
                    ctx.fill();
                }
                ctx.stroke();
                ctx.closePath();
            }
            if (this.tools.mode == this.tools.MODES.vertices) {
                let index = 1;
                for (let vertice of object.vertices) {
                    ctx.fillStyle = 'orange';
                    ctx.fillRect(vertice[0] - 2, vertice[1] - 2, 4, 4);
                    ctx.fillText(`${index}`, vertice[0] - 4, vertice[1] - 4);
                    index++;
                }
            }
            ctx.fillStyle = 'red';
            ctx.fillRect(object.center[0] - 2, object.center[1] - 2, 4, 4);
        }
        
    }
}

