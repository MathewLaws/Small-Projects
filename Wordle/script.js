document.addEventListener("DOMContentLoaded", () => {
    createSquares();
    const keys = Array.from(document.getElementsByClassName("keyboard-row"));
    const overlay = document.getElementById("overlay");
    /* node js file reader
    const fs = require("fs");
    const words = fs.readFile("words.txt", "utf8", (err, data) => {
        if (err) {
            console.error(err);
            return;
        }
        return data;
    })
    */
    const words = [
        "large",
        "study",
        "music",
        "small",
        "great",
        "river",
        "round",
        "power",
        "field",
        "class"
    ]
    let word = words[Math.floor(Math.random() * words.length)];
    let guess = [];
    let tries = 1;
    let space = 0;

    function resetGame() {
        guess = [];
        tries = 1;
        space = 0;
        word = words[Math.floor(Math.random() * words.length)];
        for (i=1; i <= 30; i++) {
            document.getElementById(String(i)).innerText = "";
            document.getElementById(String(i)).style.color = "white";
        }
        for (i=0; i < 26; i++) {
            document.getElementById(String.fromCharCode(97 + i)).style.backgroundColor = "grey";
        }
    }

    overlay.addEventListener("click", () => {
        const modals = document.querySelectorAll(".modal.active");
        modals.forEach(modal => {
            closeModal(modal);
        })
    })

    function closeModal(modal) {
        if (modal == null) return;
        modal.classList.remove("active");
        overlay.classList.remove("active");
    }

    function openModal(modal, text) {
        if (modal == null) return;
        if (text) {
            document.getElementById("modal-body").innerText = text;
        }
        modal.classList.add("active");
        overlay.classList.add("active");
    }

    keys.map(key => {
        key.addEventListener("click", x => {
            updateWord(x.target.getAttribute("data-key"));
        })
    })

    function updateKeys(lett, color) {
        document.getElementById(lett).style.backgroundColor = color;
    }

    document.addEventListener("keydown", key => {
        updateWord(key.key);
    })

    function createSquares() {
        const board = document.getElementById("board");
        for (let i=0; i<30; i++) {
            let square = document.createElement("div");
            square.classList.add("square");
            square.setAttribute("id", i+1);
            board.appendChild(square);
        }
    }

    function checkWord(guess) {
        for (i=space - 4; i < space+1; i++) {
            document.getElementById(String(i)).style.color = "grey";
        }
        for (i=0; i < guess.length; i++) {
            document.getElementById(guess[i]).style.backgroundColor = "#2a2a2a";
        }
        for (i=0; i < word.length; i++) {
            run = true;
            for (j=0; j < guess.length; j++) {
                if (run) {
                    if (word[i] == guess[j]) {
                        document.getElementById(String((tries * 5 - 5) + (j + 1))).style.color = "orange";
                        updateKeys(guess[j], "orange");
                        if (guess.indexOf(word[i]) == i) {
                            document.getElementById(String((tries * 5 - 5) + (j + 1))).style.color = "green";
                            updateKeys(guess[j], "green");
                        }
                        run = false;
                    }
                }
            }
        }
    }

    function updateWord(lett) {
        if ((tries >= 7 || space >= 30)) {
            text = `You Lose!\n The word was\n${word}`;
            const modal = document.getElementById("modal");
            openModal(modal, text);
            resetGame();
        }
        if (lett != null && lett.length < 2 && lett.toUpperCase() != lett.toLowerCase()) {
            if (guess.length < 5 && space <= tries * 5) {
                space += 1;
                guess.push(lett);
                document.getElementById(String(space)).innerText = lett;
            }
        } else if ((lett == "enter" || lett == "Enter") && space % 5 == 0 && space != 0) {
            if (String(guess).replace(/,/g, "") == word) {
                text = `You Win!\n The word was\n${word}`;
                const modal = document.getElementById("modal");
                openModal(modal, text);
                resetGame();
            } else {
                checkWord(guess);
                guess = [];
                tries += 1;
            }
        } else if ((lett == "del" || lett == "Backspace") && guess.length > 0) {
            document.getElementById(String(space)).innerText = "";
            space -= 1;
            guess.splice(-1);
        }
    }
});