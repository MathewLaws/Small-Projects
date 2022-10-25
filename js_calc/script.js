let buttons = Array.from(document.getElementsByClassName("button"));

let display = document.getElementById("display");

buttons.map(button => {
    button.addEventListener("click", (x) => {
        console.log(x.target.innerText);
        switch(x.target.innerText) {
            case "C":
                display.innerText = "";
                break
            case "=":
                display.innerText = eval(display.innerText);
                break
            default:
                display.innerText += x.target.innerText;
        }
    });
});