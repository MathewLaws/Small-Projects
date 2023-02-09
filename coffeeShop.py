import tkinter as tk
import tkinter.font as font
import sqlite3
import json

#import requests
#response = requests.get("https://free-food-menus-api-production.up.railway.app/drinks")
#print(response)

import urllib.request
#r = urllib.request.urlopen('https://free-food-menus-api-production.up.railway.app/drinks')
res = urllib.request.urlopen("https://ipinfo.io/")
res = json.loads(res.read())
city = res["city"]
loc = res["loc"].split(",")
#r = urllib.request.urlopen(f"https://api.weatherapi.com/v1/current.json?key=a2a9a4f0093b4e04aac115917230902&q={city}&aqi=yes")

#514e0d7ffa43dae060a9c3c8bbda4c52
#http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API key}
#r = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=514e0d7ffa43dae060a9c3c8bbda4c52")

#parsed = json.loads(r.read())
#print(json.dumps(parsed, indent=4))

root = tk.Tk()
root.geometry("500x500")

root.title("Coffee Shop")

conn = sqlite3.connect("User Details.sqlite")

cur = conn.cursor()

conn.execute("PRAGMA foreign_keys = 1")

cur.execute("""CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_item TEXT,
            drink_item TEXT,
            food_amount INTEGER,
            drink_amount INTEGER,
            total REAL,
            customer_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES Details (id)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS courses (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT,
            date TEXT,
            total REAL,
            customer_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES Details (id)
)""") 

cur.execute("""CREATE TABLE IF NOT EXISTS Details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
)""")

food_value = 0
drink_value = 0
total = 0
total2 = 0
total_counter2 = None
user = 0

costs = {
    "Full English": 5.50,
    "Eggs Benedict": 6,
    "Spaghetti Bolognese": 4.50,
    "Cheese on Toast": 3,
    "Coffee": 1.5,
    "Americano": 1.5,
    "Latte": 1.5,
    "Tea": 1,
    "Barrista Course": 30,
    "Cake Making": 40
}

def destroy_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def callback2(food_drink, order, window):
    if food_drink:
        cur.execute("INSERT INTO orders (food_item, drink_item, food_amount, drink_amount, total, customer_id) VALUES (?, ?, ?, ?, ?, ?)",
                (order[0], order[1], food_value, drink_value, total, user[0]))
        conn.commit()
    else:
        cur.execute("INSERT INTO courses (course, date, total, customer_id) VALUES (?, ?, ?, ?)",
                (order[0], order[1], total2, user[0]))
        conn.commit()
    print(order, total)
    window.destroy()

def change(positive, label, food, total_counter, food_option, drink_option):
    global food_value, drink_value, total
    if food:
        if positive:
            food_value += 1
        else:
            food_value -= 1
        label.config(text=food_value)
    else:
        if positive:
            drink_value += 1
        else:
            drink_value -= 1
        label.config(text=drink_value)
    if food_option in costs:
        total = food_value * costs[food_option]
    if drink_option in costs:
        total += drink_value * costs[drink_option]
    total_counter.config(text=("£", total))

def food_drink():
    total = 0
    food_value = 0
    drink_value = 0
    menu = tk.Tk()
    menu.geometry("500x500")

    total_counter = tk.Label(menu, text = ("£", total))
    total_counter.config(font=("Arial", 20))
    total_counter.grid(column="0", row="3")

    label = tk.Label(menu, text = "Food")
    label.config(font=("Arial", 20))
    label.grid(column="0", row="0")

    food_option = tk.StringVar(menu)
    food_option.set("Select an Option")
    
    foods = tk.OptionMenu(menu, food_option, *["Full English", "Cheese on Toast", "Spaghetti Bolognese", "Eggs Benedict"])
    foods.grid(column="1", row="0")

    label = tk.Label(menu, text = "Drink")
    label.config(font=("Arial", 20))
    label.grid(column="0", row="1")

    drink_option = tk.StringVar(menu)
    drink_option.set("Select an Option")
    
    drinks = tk.OptionMenu(menu, drink_option, *["Coffee", "Tea", "Americano", "Latte"])
    drinks.grid(column="1", row="1")

    food_counter = tk.Label(menu, text = food_value)
    food_counter.config(font=("Arial", 20))
    food_counter.grid(column="3", row="0")

    button = tk.Button(menu, text = "+", command= lambda: change(True, food_counter, True, total_counter, food_option.get(), drink_option.get()))
    button.config(font=("Arial", 10))
    button.grid(column="2", row="0")

    button = tk.Button(menu, text = "-", command= lambda: change(False, food_counter, True, total_counter, food_option.get(), drink_option.get()))
    button.config(font=("Arial", 10))
    button.grid(column="4", row="0")

    drink_counter = tk.Label(menu, text = drink_value)
    drink_counter.config(font=("Arial", 20))
    drink_counter.grid(column="3", row="1")

    button = tk.Button(menu, text = "+", command= lambda: change(True, drink_counter, False, total_counter, food_option.get(), drink_option.get()))
    button.config(font=("Arial", 10))
    button.grid(column="2", row="1")

    button = tk.Button(menu, text = "-", command= lambda: change(False, drink_counter, False, total_counter, food_option.get(), drink_option.get()))
    button.config(font=("Arial", 10))
    button.grid(column="4", row="1")

    button = tk.Button(menu, text = "Submit")
    button.config(font=("Arial", 20), command = lambda: callback2(True, [food_option.get(), drink_option.get()], menu))
    button.grid(column="0", row="2")

def change2(course):
    global total2, total_counter2
    total2 = costs[course]
    total_counter2.config(text=("£", total2))

def book_course():
    global total2, total_counter2
    total2 = 0
    menu = tk.Tk()
    menu.geometry("500x500")

    label = tk.Label(menu, text = "Course")
    label.config(font=("Arial", 20))
    label.grid(column="0", row="0")

    menu_value = tk.StringVar(menu)
    menu_value.set("Select an Option")

    courses = tk.OptionMenu(menu, menu_value, *["Barrista Course", "Cake Making"], command=change2)
    courses.grid(column="1", row="0")

    label2 = tk.Label(menu, text = "Date: ")
    label2.config(font=("Arial", 20))
    label2.grid(column="0", row="1")

    date = tk.Entry(menu, width=30, font=("Arial", 15))
    date.grid(column="1", row="1")

    total_counter2 = tk.Label(menu, text = ("£", total2))
    total_counter2.config(font=("Arial", 20))
    total_counter2.grid(column="0", row="2")

    button = tk.Button(menu, text = "Submit")
    button.config(font=("Arial", 20), command = lambda: callback2(False, [menu_value.get(), date.get()], menu))
    button.grid(column="0", row="3")

def main():

    destroy_window(root)

    label = tk.Label(root, text = (f"Welcome {user[1]}!"))
    label.config(font=("Arial", 20))
    label.grid(column="0", row="0")

    food_and_drink = tk.Button(root, text = "Food & Drink")
    food_and_drink.config(font=("Arial", 20), command = lambda: food_drink())
    food_and_drink.grid(column="0", row="1")
    
    course = tk.Button(root, text = "Book a Course")
    course.config(font=("Arial", 20), command = lambda: book_course())
    course.grid(column="0", row="2")

def callback(name, email, password, login):
    global user
    if login:
        cur.execute("SELECT * FROM Details WHERE email = ? AND password = ?", (email, password))
        result = cur.fetchone()
        if result:
            user = result
            main()
        else:
            wrong = tk.Label(root, text = "Wrong Email or Password!")
            wrong.config(font=("Arial", 20))
            wrong.grid(column="0", row="4")
    else:
        cur.execute("INSERT INTO Details (name, email, password) VALUES (?, ?, ?)",
                (name, email, password))
        conn.commit()

        cur.execute("SELECT * FROM Details WHERE email = ? AND password = ?", (email, password))
        result = cur.fetchone()
        user = result
        main()
        

def form(login):
    registerBtn.destroy()
    loginBtn.destroy()
    if not login:
        label1 = tk.Label(root, text = "Enter name: ")
        label1.config(font=("Arial", 20))
        label1.grid(column="0", row="0")

        name = tk.Entry(root, width=30, font=("Arial", 15))
        name.grid(column="1", row="0")
    else:
        name = tk.Entry(root, width=30, font=("Arial", 15))

    label2 = tk.Label(root, text = "Enter email: ")
    label2.config(font=("Arial", 20))
    label2.grid(column="0", row="1")

    email = tk.Entry(root, width=30, font=("Arial", 15))
    email.grid(column="1", row="1")

    label3 = tk.Label(root, text = "Enter password: ")
    label3.config(font=("Arial", 20))
    label3.grid(column="0", row="2")

    password = tk.Entry(root, width=30, font=("Arial", 15))
    password.grid(column="1", row="2")
            
    button = tk.Button(root, text = "Enter")
    button.config(font=("Arial", 20), command = lambda: callback(name.get(), email.get(), password.get(), login))
    button.grid(column="0", row="3")

registerBtn = tk.Button(root, text = "Register")
registerBtn.config(font=("Arial", 20), command = lambda: form(False))
registerBtn.grid(column="0", row="0")

loginBtn = tk.Button(root, text = "Login")
loginBtn.config(font=("Arial", 20), command = lambda: form(True))
loginBtn.grid(column="1", row="0")

root.mainloop()
