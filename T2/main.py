# import the required modules
import urllib.request
import json
import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
import datetime
import customtkinter
from PIL import Image, ImageTk
from math import log10

# create the GUI
root = customtkinter.CTk()

WIDTH = 700
HEIGHT = 700

# resize the GUI to fit
root.geometry(f"{WIDTH}x{HEIGHT}")

# change background colour
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# connect to the database
conn = sqlite3.connect("Database.db")

# initialize a cursor to traverse the database records
c = conn.cursor()

# allow foreign keys
conn.execute("PRAGMA foreign_keys = 1")

# create the details database if it does not already exist
c.execute("""
          CREATE TABLE IF NOT EXISTS Details(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          Username TEXT,
          Password TEXT,
          Gender TEXT,
          DOB TEXT
)""")

# create the to-do list database if it does not already exist
c.execute("""
          CREATE TABLE IF NOT EXISTS Todos(
          todo_id INTEGER PRIMARY KEY AUTOINCREMENT,
          description TEXT,
          complete BOOLEAN,
          user_id INTEGER,
          FOREIGN KEY(user_id) REFERENCES Details(id)
)""")

# create the prefrences database if it does not already exist
c.execute("""
          CREATE TABLE IF NOT EXISTS Prefrences(
          prefrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
          dark_mode BOOLEAN,
          user_id INTEGER,
          FOREIGN KEY(user_id) REFERENCES Details(id)
)""")

# save changes
conn.commit()

# get the user's location from their IP address
loc = json.loads(
    urllib.request.urlopen("https://ipinfo.io/").read())["loc"].split(",")

# get the current time
current_time = datetime.datetime.now()

# generate start and end dates
d = datetime.timedelta(7)
d2 = datetime.timedelta(5)
start_date = current_time.strftime("%Y-%m-%d")
weather_end_date = (current_time + d).strftime("%Y-%m-%d")
airQuality_end_date = (current_time + d2).strftime("%Y-%m-%d")


# define a new class
class Main:

    def __init__(self):
        # set the user to None as they have not yet signed in
        self.user = None

    # funtion used to destroy all GUI objects on the screen
    def destroy_children(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def display_weather_graph(self, weatherData):
        # create a plot
        fig, ax = plt.subplots()

        # create two y-axis labels for temperature and precipitation
        ax2 = ax.twinx()
        # set the first y-axis label to temperature
        ax.set_ylabel("Temp (C)", color="g")
        # set the second y-axis label to precipitation
        ax2.set_ylabel("Precipitation (mm)", color="b")

        # plot the hourly data for the specified time period
        ax.plot(
            weatherData["hourly"]["time"],
            weatherData["hourly"]["temperature_2m"],
            "g-",
        )
        ax2.plot(
            weatherData["hourly"]["time"],
            weatherData["hourly"]["precipitation"],
            "b-",
        )

        # plot the dates in increments of 24 (everyday)
        ax.set_xticks(
            [i for i in range(0, len(weatherData["hourly"]["time"]), 24)])

        # format ticks
        ax.tick_params(axis="x", rotation=20, labelsize=8)

        # display the plot
        plt.show()

    def weather(self):
        # title
        customtkinter.CTkLabel(root, text="Weather",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            pady=5,
                                                            padx=10)

        # send a request to a weather API
        res = urllib.request.urlopen(
            f"https://api.open-meteo.com/v1/forecast?latitude={loc[0]}&longitude={loc[1]}&hourly=temperature_2m,relativehumidity_2m,surface_pressure,windspeed_10m,precipitation&windspeed_unit=ms&start_date={start_date}&end_date={weather_end_date}"
        )
        # format the data using JSON for ease of use
        weatherData = json.loads(res.read())

        # weatherImg = customtkinter.CTkImage(
        # dark_image=Image.open("./imgs/weather.png"), size=(100, 100))

        today = datetime.datetime.now()

        days = [(today+datetime.timedelta(days=i)).strftime('%A')
                for i in range(7)]

        tabview = customtkinter.CTkTabview(
            root, width=(WIDTH-20))
        tabview.grid(row=1, column=0, sticky="W", pady=5, padx=10)

        for i in range(7):
            tabview.add(days[i])

        frames = []

        for i in range(len(days)):
            frames.append(customtkinter.CTkScrollableFrame(
                tabview.tab(days[i]), orientation="horizontal", width=(WIDTH-40)))
            frames[i].grid(row=0, column=0)

            for k, j in enumerate(range(0, 22, 3)):

                customtkinter.CTkLabel(
                    frames[i],
                    text=(f"{j}:00"),
                    font=("Helvetica", 20)).grid(row=0, column=k, sticky="W", pady=5, padx=10)

                customtkinter.CTkLabel(
                    frames[i],
                    text=(
                        (f"{weatherData['hourly']['temperature_2m'][(i*24)+j]} °C")),
                    font=("Helvetica", 30),
                    text_color="red").grid(row=1, column=k, sticky="W", pady=5, padx=10)

                customtkinter.CTkLabel(
                    frames[i],
                    text=(
                        f"Precipitation: {weatherData['hourly']['precipitation'][(i*24)+j]}mm"),
                    font=("Helvetica", 15)).grid(row=2,
                                                 column=k,
                                                 sticky="W",
                                                 pady=5,
                                                 padx=10)

                customtkinter.CTkLabel(
                    frames[i],
                    text=(
                        (f"Humidity: {weatherData['hourly']['relativehumidity_2m'][(i*24)+j]}%").ljust(30)),
                    font=("Helvetica", 15)).grid(row=3,
                                                 column=k,
                                                 sticky="W",
                                                 pady=5,
                                                 padx=10)

                customtkinter.CTkLabel(
                    frames[i],
                    text=(
                        f"Pressure: {weatherData['hourly']['surface_pressure'][(i*24)+j]}hPa"),
                    font=("Helvetica", 15)).grid(row=4,
                                                 column=k,
                                                 sticky="W",
                                                 pady=5,
                                                 padx=10)

                customtkinter.CTkLabel(
                    frames[i],
                    text=(
                        f"Wind Speed: {weatherData['hourly']['windspeed_10m'][(i*24)+9]}km/h"),
                    font=("Helvetica", 15)).grid(row=5,
                                                 column=k,
                                                 sticky="W",
                                                 pady=5,
                                                 padx=10)

        # display graph button
        customtkinter.CTkButton(
            root,
            text="Display Graph",
            font=("Helvetica", 15),
            command=lambda: (self.display_weather_graph(weatherData)),
        ).grid(row=2, column=0, sticky="W", pady=10, padx=10)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=3, column=0, sticky="W", pady=10, padx=10)

    def display_airQuality_graph(self, airData):

        # create a plot
        fig, ax = plt.subplots()

        # create two y-axis labels, one for micrograms per cubic meter of air and one for European Air Quality Index
        ax2 = ax.twinx()
        # set the first y-axis label to micrograms per cubic meter of air
        ax.set_ylabel("µg/m3", color="g")
        # set the second y-axis label to European Air Quality Index
        ax2.set_ylabel("EAQI", color="b")

        # plot the hourly data for the specified time period
        pm10 = ax.plot(airData["hourly"]["time"],
                       airData["hourly"]["pm10"], "g-")

        pm2_5 = ax.plot(airData["hourly"]["time"],
                        airData["hourly"]["pm2_5"], "r-")

        ax2.plot(airData["hourly"]["time"],
                 airData["hourly"]["european_aqi"], "b-")

        # create a legend
        ax.legend(["pm10", "pm2.5", "EAQI"])

        # plot the dates in increments of 24 (everyday)
        ax.set_xticks(
            [i for i in range(0, len(airData["hourly"]["time"]), 24)])

        # format ticks
        # format ticks
        ax.tick_params(axis="x", rotation=20, labelsize=8)

        # display the plot
        plt.show()

    def air_quality(self):
        # title
        customtkinter.CTkLabel(root, text="Air Quality",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10, pady=5)

        # send a request to a weather API
        res = urllib.request.urlopen(
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={loc[0]}&longitude={loc[1]}&hourly=pm10,pm2_5,european_aqi&start_date={start_date}&end_date={airQuality_end_date}"
        )
        # format the data using JSON for ease of use
        airData = json.loads(res.read())

        # display graph button
        customtkinter.CTkButton(
            root,
            text="Display Graph",
            font=("Helvetica", 15),
            command=lambda: (self.display_airQuality_graph(airData)),
        ).grid(row=1, column=0, sticky="W", pady=10, padx=10)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=2, column=0, sticky="W", pady=10, padx=10)

    # function to show and hide the labels when the corrosponding button is clicked
    # e.g. when the corona virus button is presses, the advice on the corona virus
    # will display on the screen
    def show_hide_label(self, object):
        if object[1]:
            object[0].grid_remove()
        else:
            object[0].grid(row=object[2], column=0,
                           sticky="W", padx=10, pady=4)

        object[1] = not object[1]
        return object

    def advice(self):

        # title
        customtkinter.CTkLabel(root, text="Advice",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10, pady=5)

        # advice on the corona virus
        coronaLabel = [
            customtkinter.CTkLabel(
                root,
                text="""If you have any of the main symptoms of coronovirus it's important that you get tested as soon as possible:

A high temperature
A new continuous cough
A loss or change to your sense of smell or taste""",
                font=("Helvetica", 15),
                wraplength=680,
            ),
            False,
            2,
        ]

        # button to reveal the advice
        customtkinter.CTkButton(
            root,
            text="Corona Virus",
            font=("Helvetica", 15),
            command=lambda: (self.show_hide_label(coronaLabel)),
        ).grid(row=1, column=0, sticky="W", padx=10, pady=5)

        # advice on the flu virus
        fluLabel = [
            customtkinter.CTkLabel(
                root,
                text="""Flu can affect people in different ways and can be more serious than you think. The flu vaccination is offered free of charge to people who are at most risk from the effects of the virus to protect them from catching flu and developing serious complications. Find out who is eligible for a free flu jab.

Contact your GP or pharmacist if you think you, or someone you care for, should be eligible for a free flu jab. There's further information about flu and the flu vaccine on the NHS website.""",
                font=("Helvetica", 15),
                wraplength=680,
            ),
            False,
            4,
        ]

        # button to reveal the advice
        customtkinter.CTkButton(
            root,
            text="Flu",
            font=("Helvetica", 15),
            command=lambda: (self.show_hide_label(fluLabel)),
        ).grid(row=3, column=0, sticky="W", padx=10, pady=5)

        # advice on cold weather
        coldLabel = [
            customtkinter.CTkLabel(
                root,
                text="""It is important to keep warm in winter both inside and outdoors. Keeping warm can help to prevent colds, flu and more serious health problems.

Eating regularly helps keep you warm so try to have at least one hot meal a day along with regular hot drinks.

Keep your house warm and your bedroom window closed especially on cold winter nights, as breathing cold air can be bad for your health as it increases the risk of chest infections.

Try to keep moving when you are indoors, try not to sit still for more than an hour or so. Break up your time spent being inactive by walking around your home or standing up from your chair when you are on the phone.

If you are heading outside for a walk or maybe some gardening, wear several layers of light clothes. Remember that several thin layers of clothing will keep you warmer than one thick layer as the layers trap warm air.""",
                font=("Helvetica", 15),
                wraplength=680,
            ),
            False,
            6,
        ]

        # button to reveal advice
        customtkinter.CTkButton(
            root,
            text="Cold Weather",
            font=("Helvetica", 15),
            command=lambda: (self.show_hide_label(coldLabel)),
        ).grid(row=5, column=0, sticky="W", padx=10, pady=5)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=7, column=0, sticky="W", pady=5, padx=10)

    # function to calculate the bmi after the details are entered
    def calculate_bmi(self, h, w):
        # error handling for empty fields and incorrect datatypes
        if h == "" or w == "":
            return "Fields are empty!"
        try:
            h = float(h)
            w = float(w)
        except:
            return "Invalid datatype!"

        res = round((w / h) / h, 2)

        return f"BMI: {res}"

    def bmi(self):

        # title
        customtkinter.CTkLabel(root, text="BMI Calculator",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        # height entry
        customtkinter.CTkLabel(root, text="Height(m): ",
                               font=("Helvetica", 15)).grid(row=1,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        height = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        height.grid(row=1, column=1, sticky="W", padx=10, pady=5)

        # weight entry
        customtkinter.CTkLabel(root, text="Weight(kg): ",
                               font=("Helvetica", 15)).grid(row=2,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        weight = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        weight.grid(row=2, column=1, sticky="W", padx=10, pady=5)

        # submit button
        customtkinter.CTkButton(
            root,
            text="Submit",
            font=("Helvetica", 15),
            command=lambda: (bmi_label.configure(text=self.calculate_bmi(
                height.get(), weight.get()))),
        ).grid(row=3, column=0, sticky="W", padx=10, pady=5)

        # bmi label
        bmi_label = customtkinter.CTkLabel(
            root, text="", font=("Helvetica", 15))
        bmi_label.grid(row=4, column=0, sticky="W", padx=10, pady=5)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.calculators()),
        ).grid(row=5, column=0, sticky="W", padx=10, pady=5)

    def insert_todo(self, description):
        if description != "":
            query = "INSERT INTO Todos(description, complete, user_id) VALUES(?,?,?)"
            c.execute(query, (description, False, self.user[0]))

            # save changes
            conn.commit()

    def create_todo(self):
        # title
        customtkinter.CTkLabel(root, text="Create To-do",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10)
        # description entry box
        customtkinter.CTkLabel(root, text="Description: ",
                               font=("Helvetica", 15)).grid(row=1,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        description = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        description.grid(row=1, column=1, sticky="W", padx=10, pady=5)

        # submit button
        customtkinter.CTkButton(
            root,
            text="Submit",
            font=("Helvetica", 15),
            command=lambda: (
                self.insert_todo(description.get()),
                self.destroy_children(root),
                self.todo(),
            ),
        ).grid(row=5, column=0, sticky="W", pady=5, padx=10)

        # cancel button
        customtkinter.CTkButton(
            root,
            text="Cancel",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.todo()),
        ).grid(row=6, column=0, sticky="W", pady=5, padx=10)

    # function to toggle the checkboxs of the todo items and update the database
    def check_box_toggle(self, num):
        sql = "SELECT * FROM Todos WHERE todo_id = ?"
        c.execute(sql, (num, ))
        todo_selected = c.fetchone()

        if todo_selected[2] == 1:
            op = 0
        else:
            op = 1

        sql = "UPDATE Todos SET complete = ? WHERE todo_id = ?"
        c.execute(sql, (op, num))

        conn.commit()

        self.destroy_children(root)
        self.todo()

    def todo(self):
        # title
        customtkinter.CTkLabel(root, text="To-do List",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10, pady=5)
        # get the state of the todo items from the database
        sql = "SELECT * FROM Todos WHERE user_id = ?"
        c.execute(sql, (self.user[0], ))

        data = c.fetchall()

        # create the GUI objects to display the todo items
        todos = [
            customtkinter.CTkCheckBox(
                root,
                variable=tk.IntVar(root, i[2]),
                command=lambda i=i: self.check_box_toggle(i[0]),
                onvalue=1,
                offvalue=0,
                text=f"{e+1}: {i[1]}",
                font=("Helvetica", 15),
            ) for e, i in enumerate(data)
        ]

        for i, todo in enumerate(todos):
            todos[i].grid(row=i + 1, column=0, sticky="W", padx=10, pady=5)

        # button to create a new todo item
        customtkinter.CTkButton(
            root,
            text="Create new todo",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.create_todo()),
        ).grid(row=len(todos) + 2, column=0, sticky="W", pady=5, padx=10)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=len(todos) + 3, column=0, sticky="W", pady=5, padx=10)

    # function to switch between light and dark mode
    def switch_mode(self, value):

        # update the database for new prefrence
        sql = "UPDATE Prefrences SET dark_mode = ? WHERE user_id = ?"
        c.execute(sql, (value.get(), self.user[0]))

        conn.commit()

        if value.get() == 1:

            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

        else:
            customtkinter.set_appearance_mode("light")
            customtkinter.set_default_color_theme("blue")

    def settings(self):
        # title
        customtkinter.CTkLabel(root, text="Settings",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        # get the users prefrences from the database
        sql = "SELECT * FROM Prefrences WHERE user_id = ?"
        c.execute(sql, (self.user[0], ))

        data = c.fetchone()

        # create a string variable to store the state of the switch
        dark_mode = customtkinter.IntVar(value=data[1])
        # dark mode switch
        customtkinter.CTkSwitch(
            root,
            text="Dark mode",
            command=lambda: self.switch_mode(dark_mode),
            variable=dark_mode,
            onvalue=1,
            offvalue=0,
        ).grid(row=1, column=0, sticky="W", padx=10, pady=3)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=5, column=0, sticky="W", pady=3, padx=10)

    # function to calculate body far percentage
    def calculate_bf(self, age, gender, weight, height, neck, waist, hip):
        # try except statement to prevent any edge case errors such as entering a letter instead of a number
        try:
            age = float(age)
            height = float(height)
            weight = float(weight)
            neck = float(neck)
            waist = float(waist)
            hip = float(hip)
        except:
            return "Invalid inputs!"

        if gender == "Male":
            bfp = (495 / (1.0324 - 0.19077 * (log10(waist - neck)) + 0.15456 *
                          (log10(height)))) - 450
        else:
            bfp = (495 / (1.29579 - 0.35004 * (log10(waist + hip - neck)) + 0.22100 *
                          (log10(height)))) - 450

        return f"Body Fat Percentage: {round(bfp, 1)}%"

    def bf_calc(self):

        sql = "SELECT * FROM Details WHERE id = ?"
        c.execute(sql, (self.user[0], ))

        data = c.fetchone()

        # calculate
        today = datetime.date.today()
        birthdate = datetime.datetime.strptime(data[4], "%d/%m/%Y")

        db_age = today.year - birthdate.year - ((today.month, today.day) <
                                                (birthdate.month, birthdate.day))
        db_gender = data[3]

        # title
        customtkinter.CTkLabel(root,
                               text="Body Fat Calculator",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        # age entry
        customtkinter.CTkLabel(root, text="Age: ",
                               font=("Helvetica", 15)).grid(row=1,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        age = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        age.grid(row=1, column=1, sticky="W", padx=10, pady=5)

        age.delete(0, "end")
        age.insert(0, db_age)

        # gender entry
        gender = customtkinter.StringVar(value=db_gender)

        customtkinter.CTkLabel(root, text="Gender: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=2,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        gender_entry = customtkinter.CTkComboBox(root,
                                                 values=["Male", "Female"],
                                                 variable=gender)

        gender_entry.grid(column=1, row=2, sticky="W", padx=10, pady=5)

        # weight entry
        customtkinter.CTkLabel(root, text="Weight(kg): ",
                               font=("Helvetica", 15)).grid(row=3,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        weight = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        weight.grid(row=3, column=1, sticky="W", padx=10, pady=5)

        # height entry
        customtkinter.CTkLabel(root, text="Height(cm): ",
                               font=("Helvetica", 15)).grid(row=4,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        height = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        height.grid(row=4, column=1, sticky="W", padx=10, pady=5)

        # neck entry
        customtkinter.CTkLabel(root, text="Neck(cm): ",
                               font=("Helvetica", 15)).grid(row=5,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        neck = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        neck.grid(row=5, column=1, sticky="W", padx=10, pady=5)

        # waist entry
        customtkinter.CTkLabel(root, text="Waist(cm): ",
                               font=("Helvetica", 15)).grid(row=6,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        waist = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        waist.grid(row=6, column=1, sticky="W", padx=10, pady=5)

        # hip entry
        customtkinter.CTkLabel(root, text="Hip(cm): ",
                               font=("Helvetica", 15)).grid(row=7,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        hip = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        hip.grid(row=7, column=1, sticky="W", padx=10, pady=5)

        # submit button
        customtkinter.CTkButton(
            root,
            text="Submit",
            font=("Helvetica", 15),
            command=lambda: bf_label.configure(text=self.calculate_bf(
                age.get(), gender.get(), weight.get(), height.get(), neck.get(),
                waist.get(), hip.get())),
        ).grid(row=8, column=0, sticky="W", pady=3, padx=10)

        bf_label = customtkinter.CTkLabel(
            root, text="", font=("Helvetica", 15))

        bf_label.grid(row=9, column=0, sticky="W", padx=10, pady=5)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.calculators()),
        ).grid(row=10, column=0, sticky="W", pady=3, padx=10)

    # function to calculate calories needed to maintain and lose weight
    def calculate_calories(self, age, gender, height, weight, activity, dict):

        # try except statement to prevent any edge case errors such as entering a letter instead of a number
        try:
            age = float(age)
            height = float(height)
            weight = float(weight)
        except:
            return "Invalid inputs!"

        if gender == "Male":
            bmr = ((10 * weight) + (6.25 * height) - (5 * age) + 5)
        else:
            bmr = ((10 * weight) + (6.25 * height) - (5 * age) - 161)

        bmr = round((bmr * dict[activity]), 0)

        return f"""Maintain Weight: {int(round(bmr, 0))} Calories/Day
Mild Weight Loss: {int(round(bmr*0.89, 0))} Calories/Day
Weight Loss: {int(round(bmr*0.79, 0))} Calories/Day
Extreme Weight Loss: {int(round(bmr*0.57, 0))} Calories/Day"""

    def calorie_calc(self):

        sql = "SELECT * FROM Details WHERE id = ?"
        c.execute(sql, (self.user[0], ))

        data = c.fetchone()

        # calculate
        today = datetime.date.today()
        birthdate = datetime.datetime.strptime(data[4], "%d/%m/%Y")

        db_age = today.year - birthdate.year - ((today.month, today.day) <
                                                (birthdate.month, birthdate.day))
        db_gender = data[3]

        # title
        customtkinter.CTkLabel(root,
                               text="Calorie Calculator",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10, pady=5)

        # age entry
        customtkinter.CTkLabel(root, text="Age: ",
                               font=("Helvetica", 15)).grid(row=1,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        age = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        age.grid(row=1, column=1, sticky="W", padx=10, pady=5)

        age.delete(0, "end")
        age.insert(0, db_age)

        # gender entry
        gender = customtkinter.StringVar(value=db_gender)

        customtkinter.CTkLabel(root, text="Gender: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=2,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        gender_entry = customtkinter.CTkComboBox(root,
                                                 values=["Male", "Female"],
                                                 variable=gender)

        gender_entry.grid(column=1, row=2, sticky="W", padx=10, pady=5)

        # height entry
        customtkinter.CTkLabel(root, text="Height(cm): ",
                               font=("Helvetica", 15)).grid(row=3,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        height = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        height.grid(row=3, column=1, sticky="W", padx=10, pady=5)

        # weight entry
        customtkinter.CTkLabel(root, text="Weight(kg): ",
                               font=("Helvetica", 15)).grid(row=4,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        weight = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        weight.grid(row=4, column=1, sticky="W", padx=10, pady=5)

        # activity entry
        activity = customtkinter.StringVar(
            value="1 Sedentary: little or no exercise")

        customtkinter.CTkLabel(root, text="Activity: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=5,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        # dictionary used to multiply calorie intake based on exercise weekly
        activity_dict = {
            "1 Sedentary: little or no exercise": 1.2,
            "2 Light: exercise 1-3 times/week": 1.35,
            "3 Moderate: exercise 4-5 times/week": 1.5,
            "4 Active: daily exercise or intense exercise 3-4 times/week": 1.65,
            "5 Very Active: intense exercise 6-7 times/week": 1.8,
            "6 Extra Active: very intense exercise daily, or physical job": 1.95
        }

        activity_entry = customtkinter.CTkComboBox(root,
                                                   values=activity_dict.keys(),
                                                   variable=activity,
                                                   width=350)

        activity_entry.grid(column=1, row=5, sticky="W", padx=10, pady=5)

        # submit button
        customtkinter.CTkButton(
            root,
            text="Submit",
            font=("Helvetica", 15),
            command=lambda: (calorie_label.configure(text=self.calculate_calories(
                age.get(), gender.get(), height.get(), weight.get(), activity.get(),
                activity_dict))),
        ).grid(row=6, column=0, sticky="W", pady=3, padx=10)

        # calorie label
        calorie_label = customtkinter.CTkLabel(root,
                                               text="",
                                               font=("Helvetica", 15),
                                               justify="left")
        calorie_label.grid(row=7, column=0, sticky="W", padx=10, pady=5)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.calculators()),
        ).grid(row=8, column=0, sticky="W", pady=3, padx=10)

    def calculators(self):
        # title
        customtkinter.CTkLabel(root,
                               text="Fitness & Health Calculators",
                               font=("Helvetica", 20)).grid(row=0,
                                                            column=0,
                                                            sticky="W",
                                                            padx=10, pady=5)

        # images for the buttons
        bmiImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/bmi.png"),
                                        size=(60, 60))
        bfpImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/bfp.png"),
                                        size=(60, 60))
        calorieImg = customtkinter.CTkImage(
            dark_image=Image.open("./imgs/calorie.png"), size=(60, 60))

        # BMI Button
        customtkinter.CTkButton(
            root,
            text="BMI Calculator",
            anchor="w",
            width=WIDTH//2-50,
            image=bmiImg,
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.bmi()),
        ).grid(column=0, row=1, pady=5, sticky="W", padx=10)

        # Calorie calculator button
        customtkinter.CTkButton(
            root,
            text="Calorie Calculator",
            anchor="w",
            width=WIDTH//2-50,
            image=bfpImg,
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.calorie_calc()),
        ).grid(column=0, row=2, pady=5, sticky="W", padx=10)

        # body fat calculator Button
        customtkinter.CTkButton(
            root,
            text="Body Fat Calculator",
            anchor="w",
            width=WIDTH//2-50,
            image=calorieImg,
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.bf_calc()),
        ).grid(column=0, row=3, pady=5, sticky="W", padx=10)

        # back button
        customtkinter.CTkButton(
            root,
            text="Back",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=5, column=0, sticky="W", pady=3, padx=10)

    def home(self):

        # get the users prefrence and change the GUI's mode accordingly
        sql = "SELECT * FROM Prefrences WHERE user_id = ?"
        c.execute(sql, (self.user[0], ))

        data = c.fetchone()

        if data[1] == 1:

            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

        else:
            customtkinter.set_appearance_mode("light")
            customtkinter.set_default_color_theme("blue")

        # title
        customtkinter.CTkLabel(root, text="Home",
                               font=("Helvetica", 20)).grid(column=0,
                                                            row=0,
                                                            padx=10, pady=5)

        # company label
        customtkinter.CTkLabel(root,
                               text="Health Advice Group",
                               font=("Helvetica", 20)).grid(column=1,
                                                            row=0,
                                                            padx=10)

        # welcome text
        customtkinter.CTkLabel(root,
                               text=f"Welcome {self.user[1]}!",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=1,
                                                            padx=4)

        # grab the images from the "imgs" folder
        weatherImg = customtkinter.CTkImage(
            dark_image=Image.open("./imgs/weather.png"), size=(60, 60))
        airImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/air.png"),
                                        size=(60, 60))
        adviceImg = customtkinter.CTkImage(
            dark_image=Image.open("./imgs/advice.png"), size=(60, 60))
        bmiImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/bmi.png"),
                                        size=(60, 60))
        todoImg = customtkinter.CTkImage(
            dark_image=Image.open("./imgs/todo-list.png"), size=(60, 60))
        settingsImg = customtkinter.CTkImage(
            dark_image=Image.open("./imgs/settings.png"), size=(60, 60))
        logOutImg = customtkinter.CTkImage(
            dark_image=Image.open("./imgs/log_out.png"), size=(60, 60))

        # weather forecasting button
        customtkinter.CTkButton(
            root,
            text="Weather Forecasting",
            anchor="w",
            width=WIDTH//2-50,
            image=weatherImg,
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.weather()),
        ).grid(column=0, row=2, pady=3, sticky="W", padx=10)

        # air quality button
        customtkinter.CTkButton(
            root,
            anchor="w",
            image=airImg,
            width=WIDTH//2-50,
            text="Air Quality Data",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.air_quality()),
        ).grid(column=0, row=3, pady=3, sticky="W", padx=10)

        # advice button
        customtkinter.CTkButton(
            root,
            anchor="w",
            width=WIDTH//2-50,
            image=adviceImg,
            text="Advice",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.advice()),
        ).grid(column=0, row=4, pady=3, sticky="W", padx=10)

        # Health button
        customtkinter.CTkButton(
            root,
            anchor="w",
            width=WIDTH//2-50,
            image=bmiImg,
            text="Fitness & Health Calculators",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.calculators()),
        ).grid(column=0, row=5, pady=3, sticky="W", padx=10)

        # To-do list button
        customtkinter.CTkButton(
            root,
            anchor="w",
            width=WIDTH//2-50,
            image=todoImg,
            text="To-do List",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.todo()),
        ).grid(column=0, row=6, pady=3, sticky="W", padx=10)

        # Settings button
        customtkinter.CTkButton(
            root,
            anchor="w",
            width=WIDTH//2-50,
            image=settingsImg,
            text="Settings",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.settings()),
        ).grid(column=0, row=7, pady=3, sticky="W", padx=10)

        # Log out button
        customtkinter.CTkButton(
            root,
            anchor="w",
            width=WIDTH//2-50,
            image=logOutImg,
            text="Log out",
            font=("Helvetica", 15),
            command=lambda: (self.destroy_children(root), self.login()),
        ).grid(column=0, row=8, pady=3, sticky="W", padx=10)

    def validation(self, username, password, confirm, dob, gender, login):
        if login:

            # find all entries in the database with the corrosponding username and password as entered
            sql = "SELECT * FROM Details WHERE Username = ? AND Password = ?"
            c.execute(sql, (username, password))

            # fetch the first result to prevent any duplication/errors
            self.user = c.fetchone()

            # if a user is found then display the home screen
            if self.user != None:
                self.destroy_children(root)
                self.home()
        else:

            # length check
            if len(username) > 3 and len(password) > 3:
                if password == confirm:
                    if gender != "Select an Option":
                        try:
                            birthdate = datetime.datetime.strptime(
                                dob, "%d/%m/%Y")
                            # check if the user already exists to prevent duplicate accounts
                            already_exists = "SELECT * FROM Details WHERE Username = ?"
                            already_exists = c.execute(
                                already_exists, (username, ))

                            if already_exists.fetchone() == None:

                                # insert the new user into the database
                                query = "INSERT INTO Details(Username, Password, Gender, DOB) VALUES(?,?,?,?)"
                                c.execute(
                                    query, (username, password, gender, dob))

                                sql = "SELECT * FROM Details WHERE Username = ? AND Password = ?"
                                c.execute(sql, (username, password))

                                # set the user variable to the current user who logged in
                                self.user = c.fetchone()

                                query = "INSERT INTO Prefrences(dark_mode, user_id) VALUES(?,?)"
                                c.execute(query, (1, self.user[0]))

                                # save changes
                                conn.commit()

                                self.destroy_children(root)

                                # display the home screen
                                self.home()
                            else:

                                # display error message
                                customtkinter.CTkLabel(
                                    root,
                                    font=("Helvetica", 15),
                                    text_color=("red"),
                                    text="Username already Taken!",
                                    wraplength=200,
                                ).grid(column=0, row=8, sticky="W", padx=10, pady=5)
                        except Exception as e:
                            # display error message
                            customtkinter.CTkLabel(
                                root,
                                font=("Helvetica", 15),
                                text_color=("red"),
                                text="Invalid date of birth!",
                                wraplength=200,
                            ).grid(column=0, row=9, sticky="W", padx=10, pady=5)
                            print(e)
                    else:
                        # display error message
                        customtkinter.CTkLabel(
                            root,
                            font=("Helvetica", 15),
                            text_color=("red"),
                            text="Invalid Gender!",
                            wraplength=200,
                        ).grid(column=0, row=10, sticky="W", padx=10, pady=5)
                else:
                    # display error message
                    customtkinter.CTkLabel(
                        root,
                        font=("Helvetica", 15),
                        text_color=("red"),
                        text="Passwords do not match!",
                        wraplength=200,
                    ).grid(column=0, row=11, sticky="W", padx=10, pady=5)
            else:

                # display error message
                customtkinter.CTkLabel(
                    root,
                    font=("Helvetica", 15),
                    text_color=("red"),
                    text="Username and Password need to be atleast 4 characters!",
                    wraplength=200,
                ).grid(column=0, row=12, sticky="W", padx=10, pady=5)

    def sign_up(self):

        # title
        customtkinter.CTkLabel(root, text="Register",
                               font=("Helvetica", 20)).grid(column=0,
                                                            row=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        # username and password entry boxes and labels
        customtkinter.CTkLabel(root, text="Username: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=1,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        customtkinter.CTkLabel(root, text="Password: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=2,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        customtkinter.CTkLabel(root,
                               text="Confirm Password: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=3,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        username_entry = customtkinter.CTkEntry(root, font=("Helvetica", 15))

        username_entry.grid(column=1, row=1, sticky="W", padx=10, pady=5)

        password_entry = customtkinter.CTkEntry(root,
                                                show="*",
                                                font=("Helvetica", 15))
        confirm_password_entry = customtkinter.CTkEntry(root,
                                                        show="*",
                                                        font=("Helvetica", 15))

        password_entry.grid(column=1, row=2, sticky="W", padx=10, pady=5)

        confirm_password_entry.grid(
            column=1, row=3, sticky="W", padx=10, pady=5)

        gender = customtkinter.StringVar(value="Select an Option")

        customtkinter.CTkLabel(root, text="Gender: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=4,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        gender_entry = customtkinter.CTkComboBox(root,
                                                 values=["Male", "Female"],
                                                 variable=gender)

        gender_entry.grid(column=1, row=4, sticky="W", padx=10, pady=5)

        customtkinter.CTkLabel(root,
                               text="Date of Birth: ",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=5,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        dob_entry = customtkinter.CTkEntry(root,
                                           font=("Helvetica", 15),
                                           placeholder_text="DD/MM/YYYY")

        dob_entry.grid(column=1, row=5, sticky="W", padx=10, pady=5)

        # submit button
        customtkinter.CTkButton(
            root,
            font=("Helvetica", 15),
            text="Submit",
            command=lambda: self.validation(username_entry.get(), password_entry.get(
            ), confirm_password_entry.get(), dob_entry.get(), gender.get(), False),
        ).grid(column=0, row=6, sticky="W", padx=10, pady=5)

        # option to login if the user already has an account
        customtkinter.CTkLabel(root,
                               text="Already have an account?",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=7,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        customtkinter.CTkButton(
            root,
            font=("Helvetica", 15),
            text="Login",
            command=lambda: (self.destroy_children(root), self.login()),
        ).grid(column=1, row=7, sticky="W", padx=10, pady=5)

    def login(self):

        # set to dark mode
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.user = None

        # title
        customtkinter.CTkLabel(root, text="Login",
                               font=("Helvetica", 20)).grid(column=0,
                                                            row=0,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)

        # username and password entry boxes and labels
        username_label = customtkinter.CTkLabel(root,
                                                text="Username: ",
                                                font=("Helvetica", 15))
        username_label.grid(column=0, row=1, sticky="W", padx=10, pady=5)
        password_label = customtkinter.CTkLabel(root,
                                                text="Password: ",
                                                font=("Helvetica", 15))
        password_label.grid(column=0, row=2, sticky="W", padx=10, pady=5)
        username_entry = customtkinter.CTkEntry(root, font=("Helvetica", 15))
        username_entry.grid(column=1, row=1, sticky="W", padx=10, pady=5)
        password_entry = customtkinter.CTkEntry(root,
                                                show="*",
                                                font=("Helvetica", 15))
        password_entry.grid(column=1, row=2, sticky="W", padx=10, pady=5)

        # submit button
        customtkinter.CTkButton(
            root,
            font=("Helvetica", 15),
            text="Submit",
            command=lambda: self.validation(username_entry.get(), password_entry.get(
            ), None, None, None, True),
        ).grid(column=0, row=3, sticky="W", padx=10, pady=5)

        # option to login if the user already has an account
        customtkinter.CTkLabel(root,
                               text="Dont have an Account?",
                               font=("Helvetica", 15)).grid(column=0,
                                                            row=4,
                                                            sticky="W",
                                                            padx=10,
                                                            pady=5)
        customtkinter.CTkButton(
            root,
            font=("Helvetica", 15),
            text="Register",
            command=lambda: (self.destroy_children(root), self.sign_up()),
        ).grid(column=1, row=4, sticky="W", padx=10, pady=5)


# checks that the file is executed directly from the user and not imported
if __name__ == "__main__":

    # initialize a new instance the the "Main" class
    main = Main()

    # call the "login" method
    main.login()

    # run the main loop of the GUI to listen for inputs
    root.mainloop()
