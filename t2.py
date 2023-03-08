# import the required modules
import urllib.request
import json
import tkinter as tk
import tkinter.font
import sqlite3
import matplotlib.pyplot as plt

# create the GUI
root = tk.Tk()

# resize the GUI to fit
root.geometry("700x800")

# change background colour
root.configure(bg="#7CB9E8")

font1 = tkinter.font.Font(family="Helvetica", size=10, weight="bold")

# connect to the database
conn = sqlite3.connect("Database.db")

c = conn.cursor()

# create the database if it does not already exist with a username and password field
c.execute(
    """
          CREATE TABLE IF NOT EXISTS Details(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          Username TEXT,
          Password TEXT
)"""
)

# save changes
conn.commit()

# get the user's location from their IP address
city = json.loads(urllib.request.urlopen("https://ipinfo.io/").read())["city"]

loc = json.loads(urllib.request.urlopen("https://ipinfo.io/").read())["loc"].split(",")


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
        tk.Label(root, text="Weather", bg="#7CB9E8", font=font1).grid(
            row=0, column=0, sticky="W"
        )

        # send a request to a weather API
        self.res = urllib.request.urlopen(
            f"https://api.open-meteo.com/v1/forecast?latitude=54.90&longitude=-1.38&hourly=temperature_2m,precipitation&windspeed_unit=ms&start_date=2023-02-15&end_date=2023-02-22"
        )
        # format the data using JSON for ease of use
        self.weatherData = json.loads(self.res.read())

        print(self.weatherData)

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

        # plot the dates in increments of 12
        plt.xticks([i for i in range(0, len(self.weatherData["hourly"]["time"]), 12)])

        # format ticks
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment="right",
            fontweight="light",
            fontsize="x-small",
        )

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
        ).grid(row=len(labels) + 1, column=0, sticky="W")

    def air_quality(self):
        # title
        tk.Label(root, text="Air Quality", bg="#7CB9E8", font=font1).grid(
            row=0, column=0, sticky="W"
        )

        # send a request to a weather API
        self.res = urllib.request.urlopen(
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude=54.90&longitude=-1.38&hourly=pm10,pm2_5,european_aqi&start_date=2023-02-15&end_date=2023-02-20"
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
        ax.plot(self.airData["hourly"]["time"], self.airData["hourly"]["pm10"], "g-")

        ax.plot(self.airData["hourly"]["time"], self.airData["hourly"]["pm2_5"], "r-")

        ax2.plot(
            self.airData["hourly"]["time"], self.airData["hourly"]["european_aqi"], "b-"
        )

        # plot the dates in increments of 12
        plt.xticks([i for i in range(0, len(self.airData["hourly"]["time"]), 12)])

        # format ticks
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment="right",
            fontweight="light",
            fontsize="x-small",
        )

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
        ).grid(row=len(labels) + 1, column=0, sticky="W")

    def advice(self):

        # back button
        tk.Button(
            root,
            text="Back",
            command=lambda: (self.destroy_children(root), self.home()),
        ).grid(row=1, column=0, sticky="W")

    def home(self):
        # title
        tk.Label(root, text="Home", bg="#7CB9E8", font=font1).grid(column=0, row=0)

        # company label
        company_label = tk.Label(
            root, text="Health Advice Group", bg="#7CB9E8", font=font1
        ).grid(column=1, row=0, padx=(10, 0))

        # welcome text
        tk.Label(root, text=f"Welcome {self.user[1]}!", bg="#7CB9E8", font=font1).grid(
            column=0, row=1
        )

        # weather forecasting button
        tk.Button(
            root,
            text="Weather Forecasting",
            font=font1,
            bg="#50C878",
            command=lambda: (self.destroy_children(root), self.weather()),
        ).grid(column=0, row=2)

        # air quality button
        tk.Button(
            root,
            text="Air Quality Data",
            font=font1,
            bg="#50C878",
            command=lambda: (self.destroy_children(root), self.air_quality()),
        ).grid(column=0, row=3)

        # advice button
        tk.Button(
            root,
            text="Advice",
            font=font1,
            bg="#50C878",
            command=lambda: (self.destroy_children(root), self.advice()),
        ).grid(column=0, row=4)

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
                already_exists = c.execute(already_exists, (username,))

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
                    tk.Label(root, text="Username already Taken!").grid(column=0, row=5)
            else:

                # display error message
                tk.Label(
                    root, text="Username and Password need to be atleast 4 characters!"
                ).grid(column=0, row=6)

    def sign_up(self):

        # title
        tk.Label(root, text="Register", bg="#7CB9E8", font=font1).grid(column=0, row=0)

        # username and password entry boxes and labels
        username_label = tk.Label(root, text="Username: ", bg="#7CB9E8", font=font1)
        username_label.grid(column=0, row=1)
        password_label = tk.Label(root, text="Password: ", bg="#7CB9E8", font=font1)
        password_label.grid(column=0, row=2)
        username_entry = tk.Entry(root)
        username_entry.grid(column=1, row=1)
        password_entry = tk.Entry(root)
        password_entry.grid(column=1, row=2)

        # submit button
        tk.Button(
            root,
            text="Submit",
            font=font1,
            bg="#50C878",
            command=lambda: self.validation(
                username_entry.get(), password_entry.get(), False
            ),
        ).grid(column=0, row=3)

        # option to login if the user already has an account
        tk.Label(root, text="Already have an Account?", bg="#7CB9E8", font=font1).grid(
            column=0, row=4
        )
        tk.Button(
            root,
            bg="#50C878",
            font=font1,
            text="Login",
            command=lambda: (self.destroy_children(root), self.login()),
        ).grid(column=1, row=4)

    def login(self):

        # title
        tk.Label(root, text="Login", bg="#7CB9E8", font=font1).grid(column=0, row=0)

        # username and password entry boxes and labels
        username_label = tk.Label(root, text="Username: ", bg="#7CB9E8", font=font1)
        username_label.grid(column=0, row=1)
        password_label = tk.Label(root, text="Password: ", bg="#7CB9E8", font=font1)
        password_label.grid(column=0, row=2)
        username_entry = tk.Entry(root)
        username_entry.grid(column=1, row=1)
        password_entry = tk.Entry(root)
        password_entry.grid(column=1, row=2)

        # submit button
        tk.Button(
            root,
            font=font1,
            bg="#50C878",
            text="Submit",
            command=lambda: self.validation(
                username_entry.get(), password_entry.get(), True
            ),
        ).grid(column=0, row=3)

        # option to login if the user already has an account
        tk.Label(root, text="Dont have an Account?", bg="#7CB9E8", font=font1).grid(
            column=0, row=4
        )
        tk.Button(
            root,
            font=font1,
            bg="#50C878",
            text="Register",
            command=lambda: (self.destroy_children(root), self.sign_up()),
        ).grid(column=1, row=4)


# checks that the file is executed directly from the user and not imported
if __name__ == "__main__":

    # initialize a new instance the the "Main" class
    main = Main()

    # call the "login" method
    main.login()

    # run the main loop of the GUI to listen for inputs
    root.mainloop()
