let food = randPos()
const EXPANSION_RATE = 1

import { onSnake, expandSnake } from "./snake.js"

export function update() {
    if (onSnake(food)) {
        expandSnake(EXPANSION_RATE)
        food = randPos()
    }
}

export function draw(gameBoard) {
    const foodElement = document.createElement('div')
    foodElement.style.gridRowStart = food.y
    foodElement.style.gridColumnStart = food.x
    foodElement.classList.add('food')
    gameBoard.append(foodElement)
}

function randPos() {
    let newPos
    while (newPos == null || onSnake(newPos)) {
        newPos = randGridPos()
    }
    return newPos
}

function randGridPos() {
    return {
        x: Math.floor(Math.random() * 21) + 1,
        y: Math.floor(Math.random() * 21) + 1
    }
}