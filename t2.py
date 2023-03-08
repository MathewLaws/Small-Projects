# import the required modules
import urllib.request
import json
import tkinter as tk
import tkinter.font
import sqlite3
import matplotlib.pyplot as plt
import datetime

# create the GUI
root = tk.Tk()

# resize the GUI to fit
root.geometry("700x700")

# change background colour
root.configure(bg="#7CB9E8")

# create new font
font1 = tkinter.font.Font(family="Helvetica", size=10, weight="bold")
title_font = tkinter.font.Font(family="Helvetica", size=15, weight="bold")

# connect to the database
conn = sqlite3.connect("Database.db")

# initialize a cursor to traverse the database records
c = conn.cursor()

# create the database if it does not already exist with a username and password field
c.execute("""
          CREATE TABLE IF NOT EXISTS Details(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          Username TEXT,
          Password TEXT
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

    def weather(self):
        # title
        tk.Label(root, text="Weather", bg="#7CB9E8", font=title_font).grid(row=0,
                                                                           column=0,
                                                                           sticky="W")

        # send a request to a weather API
        self.res = urllib.request.urlopen(
            f"https://api.open-meteo.com/v1/forecast?latitude={loc[0]}&longitude={loc[1]}&hourly=temperature_2m,precipitation&windspeed_unit=ms&start_date={start_date}&end_date={weather_end_date}"
        )
        # format the data using JSON for ease of use
        self.weatherData = json.loads(self.res.read())

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
            self.weatherData["hourly"]["time"],
            self.weatherData["hourly"]["temperature_2m"],
            "g-",
        )
        ax2.plot(
            self.weatherData["hourly"]["time"],
            self.weatherData["hourly"]["precipitation"],
            "b-",
        )

        # plot the dates in increments of 24 (everyday)
        ax.set_xticks(
            [i for i in range(0, len(self.weatherData["hourly"]["time"]), 24)])

        # format ticks
        ax.tick_params(axis='x', rotation=20, labelsize=8)

        # display the plot
        plt.show()

        # display the rest of the data (time, location, etc)
        labels = [
            tk.Label(root, text=(f"{d[0]}: {d[1]}"), bg="#7CB9E8", font=font1)
            for d in list(self.weatherData.items())[0:6]
        ]

        for i, label in enumerate(labels):
            label.grid(column=0, row=i + 1, sticky="W")

        # back button
        tk.Button(
            root,
            text="Back",
            bg="#50C878",
            font=font1,
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=len(labels) + 1, column=0, sticky="W", pady=3)

    def air_quality(self):
        # title
        tk.Label(root, text="Air Quality", bg="#7CB9E8",
                 font=title_font).grid(row=0, column=0, sticky="W")

        # send a request to a weather API
        self.res = urllib.request.urlopen(
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={loc[0]}&longitude={loc[1]}&hourly=pm10,pm2_5,european_aqi&start_date={start_date}&end_date={airQuality_end_date}"
        )
        # format the data using JSON for ease of use
        self.airData = json.loads(self.res.read())

        # create a plot
        fig, ax = plt.subplots()

        # create two y-axis labels, one for micrograms per cubic meter of air and one for European Air Quality Index
        ax2 = ax.twinx()
        # set the first y-axis label to micrograms per cubic meter of air
        ax.set_ylabel("µg/m3", color="g")
        # set the second y-axis label to European Air Quality Index
        ax2.set_ylabel("EAQI", color="b")

        # plot the hourly data for the specified time period
        pm10 = ax.plot(self.airData["hourly"]["time"],
                       self.airData["hourly"]["pm10"], "g-")

        pm2_5 = ax.plot(self.airData["hourly"]["time"],
                        self.airData["hourly"]["pm2_5"], "r-")

        ax2.plot(self.airData["hourly"]["time"],
                 self.airData["hourly"]["european_aqi"], "b-")

        # create a legend
        ax.legend(["pm10", "pm2.5", "EAQI"])

        # plot the dates in increments of 24 (everyday)
        ax.set_xticks(
            [i for i in range(0, len(self.airData["hourly"]["time"]), 24)])

        # format ticks
        # format ticks
        ax.tick_params(axis='x', rotation=20, labelsize=8)

        # display the plot
        plt.show()

        # display the rest of the data (time, location, etc)
        labels = [
            tk.Label(root, text=(f"{d[0]}: {d[1]}"), bg="#7CB9E8", font=font1)
            for d in list(self.airData.items())[0:6]
        ]

        for i, label in enumerate(labels):
            label.grid(column=0, row=i + 1, sticky="W")

        # back button
        tk.Button(
            root,
            text="Back",
            bg="#50C878",
            font=font1,
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=len(labels) + 1, column=0, sticky="W", pady=3)

    def show_hide_label(self, object):
        if object[1]:
            object[0].grid_remove()
        else:
            object[0].grid(row=object[2], column=0, sticky="W")

        object[1] = not object[1]
        return object

    def advice(self):

        # title
        tk.Label(root, text="Advice", bg="#7CB9E8", font=title_font).grid(row=0,
                                                                          column=0,
                                                                          sticky="W")

        # advice on the corona virus
        coronaLabel = [
            tk.Label(
                root,
                text="""If you have any of the main symptoms of coronovirus it's important that you get tested as soon as possible:

A high temperature
A new continuous cough
A loss or change to your sense of smell or taste""",
                font=font1,
                justify="left",
                wraplength=700,
            ),
            False,
            2,
        ]

        # button to reveal the advice
        tk.Button(
            root,
            text="Corona Virus",
            bg="#ED7104",
            font=font1,
            command=lambda: (self.show_hide_label(coronaLabel)),
        ).grid(row=1, column=0, sticky="W")

        # advice on the flu virus
        fluLabel = [
            tk.Label(
                root,
                text="""Flu can affect people in different ways and can be more serious than you think. The flu vaccination is offered free of charge to people who are at most risk from the effects of the virus to protect them from catching flu and developing serious complications. Find out who is eligible for a free flu jab.

Contact your GP or pharmacist if you think you, or someone you care for, should be eligible for a free flu jab. There's further information about flu and the flu vaccine on the NHS website.""",
                font=font1,
                justify="left",
                wraplength=700,
            ),
            False,
            4,
        ]

        # button to reveal the advice
        tk.Button(
            root,
            text="Flu",
            bg="#ED7104",
            font=font1,
            command=lambda: (self.show_hide_label(fluLabel)),
        ).grid(row=3, column=0, sticky="W")

        # advice on cold weather
        coldLabel = [
            tk.Label(
                root,
                text="""It is important to keep warm in winter both inside and outdoors. Keeping warm can help to prevent colds, flu and more serious health problems.

Eating regularly helps keep you warm so try to have at least one hot meal a day along with regular hot drinks.

Keep your house warm and your bedroom window closed especially on cold winter nights, as breathing cold air can be bad for your health as it increases the risk of chest infections.

Try to keep moving when you are indoors, try not to sit still for more than an hour or so. Break up your time spent being inactive by walking around your home or standing up from your chair when you are on the phone.

If you are heading outside for a walk or maybe some gardening, wear several layers of light clothes. Remember that several thin layers of clothing will keep you warmer than one thick layer as the layers trap warm air.""",
                font=font1,
                justify="left",
                wraplength=700,
            ),
            False,
            6,
        ]

        # button to reveal advice
        tk.Button(
            root,
            text="Cold Weather",
            bg="#ED7104",
            font=font1,
            command=lambda: (self.show_hide_label(coldLabel)),
        ).grid(row=5, column=0, sticky="W")

        # back button
        tk.Button(
            root,
            text="Back",
            bg="#50C878",
            font=font1,
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=7, column=0, sticky="W", pady=3)

    # function to calculate the bmi after the details are entered
    def calculate_bmi(self, h, w):
        return (float(w)/float(h))/float(h)

    def bmi(self):
        # title
        tk.Label(root, text="BMI Calculator", bg="#7CB9E8",
                 font=title_font).grid(row=0, column=0, sticky="W")

        # height entry
        tk.Label(root, text="Height(m): ", font=font1, bg="#7CB9E8").grid(
            row=1, column=0, sticky="W")
        height = tk.Entry(root)
        height.grid(row=1, column=1, sticky="W")

        # weight entry
        tk.Label(root, text="Weight(KG): ", font=font1, bg="#7CB9E8").grid(
            row=2, column=0, sticky="W")
        weight = tk.Entry(root)
        weight.grid(row=2, column=1, sticky="W")

        # submit button
        tk.Button(
            root,
            text="Submit",
            bg="#50C878",
            font=font1,
            command=lambda: (bmi_label.config(
                text=f"You have a BMI of {round(self.calculate_bmi(height.get(), weight.get()), 2)}")),
        ).grid(row=3, column=0, sticky="W")

        # bmi label
        bmi_label = tk.Label(root, text="", font=font1, bg="#7CB9E8")
        bmi_label.grid(row=4, column=0, sticky="W")

        # back button
        tk.Button(
            root,
            text="Back",
            bg="#50C878",
            font=font1,
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=5, column=0, sticky="W", pady=3)

    def home(self):
        # title
        tk.Label(root, text="Home", bg="#7CB9E8",
                 font=title_font).grid(column=0, row=0)

        # company label
        tk.Label(root, text="Health Advice Group", bg="#7CB9E8",
                 font=font1).grid(column=1, row=0, padx=(10, 0))

        # welcome text
        tk.Label(root, text=f"Welcome {self.user[1]}!", bg="#7CB9E8",
                 font=font1).grid(column=0, row=1)

        # weather forecasting button
        tk.Button(
            root,
            text="Weather Forecasting",
            font=font1,
            bg="#50C878",
            justify="left",
            command=lambda: (self.destroy_children(root), self.weather()),
        ).grid(column=0, row=2, pady=3, sticky="W")

        # air quality button
        tk.Button(
            root,
            text="Air Quality Data",
            font=font1,
            bg="#50C878",
            justify="left",
            command=lambda: (self.destroy_children(root), self.air_quality()),
        ).grid(column=0, row=3, pady=3, sticky="W")

        # advice button
        tk.Button(
            root,
            text="Advice",
            font=font1,
            bg="#50C878",
            justify="left",
            command=lambda: (self.destroy_children(root), self.advice()),
        ).grid(column=0, row=4, pady=3, sticky="W")

        # BMI button
        tk.Button(
            root,
            text="BMI Calculator",
            font=font1,
            bg="#50C878",
            justify="left",
            command=lambda: (self.destroy_children(root), self.bmi()),
        ).grid(column=0, row=5, pady=3, sticky="W")

    def validation(self, username, password, login):
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

                # check if the user already exists to prevent duplicate accounts
                already_exists = "SELECT * FROM Details WHERE Username = ?"
                already_exists = c.execute(already_exists, (username, ))

                if already_exists.fetchone() == None:

                    # insert the new user into the database
                    query = "INSERT INTO Details(Username, Password) VALUES(?,?)"
                    c.execute(query, (username, password))

                    # save changes
                    conn.commit()

                    sql = "SELECT * FROM Details WHERE Username = ? AND Password = ?"
                    c.execute(sql, (username, password))

                    # set the user variable to the current user who logged in
                    self.user = c.fetchone()

                    self.destroy_children(root)

                    # display the home screen
                    self.home()
                else:

                    # display error message
                    tk.Label(root, font=font1, bg="#7CB9E8", fg="red", text="Username already Taken!", justify="left").grid(
                        column=0, row=5, sticky="W")
            else:

                # display error message
                tk.Label(
                    root,
                    justify="left",
                    font=font1, bg="#7CB9E8",
                    fg="red",
                    text="Username and Password need to be atleast 4 characters!").grid(
                    column=0, row=6, sticky="W")

    def sign_up(self):

        # title
        tk.Label(root, text="Register", bg="#7CB9E8", font=title_font).grid(column=0,
                                                                            row=0, sticky="W")

        # username and password entry boxes and labels
        username_label = tk.Label(root,
                                  text="Username: ",
                                  bg="#7CB9E8",
                                  font=font1,
                                  justify="left")
        username_label.grid(column=0, row=1, sticky="W")
        password_label = tk.Label(root,
                                  text="Password: ",
                                  bg="#7CB9E8",
                                  font=font1,
                                  justify="left")
        password_label.grid(column=0, row=2, sticky="W")
        username_entry = tk.Entry(root, justify="left")
        username_entry.grid(column=1, row=1, sticky="W")
        password_entry = tk.Entry(root, show="*", justify="left")
        password_entry.grid(column=1, row=2, sticky="W")

        # submit button
        tk.Button(
            root,
            text="Submit",
            font=font1,
            bg="#50C878",
            justify="left",
            command=lambda: self.validation(username_entry.get(), password_entry.get(
            ), False),
        ).grid(column=0, row=3, sticky="W")

        # option to login if the user already has an account
        tk.Label(root, text="Already have an Account?", bg="#7CB9E8",
                 font=font1, justify="left").grid(column=0, row=4, sticky="W")
        tk.Button(
            root,
            bg="#50C878",
            font=font1,
            text="Login",
            justify="left",
            command=lambda: (self.destroy_children(root), self.login()),
        ).grid(column=1, row=4, sticky="W")

    def login(self):

        # title
        tk.Label(root, text="Login", bg="#7CB9E8", font=title_font, justify="left").grid(column=0,
                                                                                         row=0, sticky="W")

        # username and password entry boxes and labels
        username_label = tk.Label(root,
                                  text="Username: ",
                                  bg="#7CB9E8",
                                  font=font1, justify="left")
        username_label.grid(column=0, row=1, sticky="W")
        password_label = tk.Label(root,
                                  text="Password: ",
                                  bg="#7CB9E8",
                                  font=font1, justify="left")
        password_label.grid(column=0, row=2, sticky="W")
        username_entry = tk.Entry(root, justify="left")
        username_entry.grid(column=1, row=1, sticky="W")
        password_entry = tk.Entry(root, show="*", justify="left")
        password_entry.grid(column=1, row=2, sticky="W")

        # submit button
        tk.Button(
            root,
            font=font1,
            bg="#50C878",
            text="Submit",
            justify="left",
            command=lambda: self.validation(username_entry.get(), password_entry.get(
            ), True),
        ).grid(column=0, row=3, sticky="W")

        # option to login if the user already has an account
        tk.Label(root, text="Dont have an Account?", bg="#7CB9E8",
                 font=font1, justify="left").grid(column=0, row=4, sticky="W")
        tk.Button(
            root,
            font=font1,
            bg="#50C878",
            text="Register",
            justify="left",
            command=lambda: (self.destroy_children(root), self.sign_up()),
        ).grid(column=1, row=4, sticky="W")


# checks that the file is executed directly from the user and not imported
if __name__ == "__main__":

    # initialize a new instance the the "Main" class
    main = Main()

    # call the "login" method
    main.login()

    # run the main loop of the GUI to listen for inputs
    root.mainloop()
