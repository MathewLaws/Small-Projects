document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const tools = document.getElementById("tools");
    const slider = document.getElementById("slider");
    const sizeText = document.getElementById("size");
    const colors = Array.from(document.getElementsByClassName("color"));
    const rubber = document.getElementById("rubber-btn");
    const clearBtn = document.getElementById("clear");

    let painting = false;
    let size = 10;
    let curColor = "black";

    canvas.height = window.innerHeight - tools.offsetHeight;
    canvas.width = window.innerWidth;

    function draw(pos) {
        if (painting) {
            ctx.lineWidth = size;
            ctx.lineCap = "round";
            ctx.strokeStyle = curColor;

            ctx.lineTo(pos.clientX, pos.clientY);
            ctx.stroke();
            ctx.beginPath();
        }
    }

    colors.forEach((color) => {
        color.style.background = color.getAttribute("data-key");
        color.addEventListener("click", () => {
            colors.forEach((color) => {
                color.style.border = "1px solid black";
            })
            rubber.style.border = "none";
            color.style.border = "5px solid black"
            curColor = color.getAttribute("data-key");
        })
    })

    canvas.addEventListener("mousemove", draw);

    canvas.addEventListener("mousedown", (pos) => {
        painting = true;
        draw(pos);
    })

    canvas.addEventListener("mouseup", () => {
        painting = false;
    })

    rubber.addEventListener("click", () => {
        rubber.style.border = "5px solid black";
        colors.forEach((color) => {
            color.style.border = "1px solid black";
        })
        curColor = "white";
    })

    clearBtn.addEventListener("click", () => {
        canvas.height = window.innerHeight - tools.offsetHeight;
        canvas.width = window.innerWidth;
    })

    slider.oninput = function() {
        sizeText.innerHTML = this.value;
        size = this.value;
    }

})