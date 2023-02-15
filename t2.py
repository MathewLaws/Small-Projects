import urllib.request
import json
import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

root = tk.Tk()
root.geometry("700x800")

conn = sqlite3.connect("Database.db")

c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS Details(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          Username TEXT,
          Password TEXT
)''')

conn.commit()

city = json.loads(urllib.request.urlopen("https://ipinfo.io/").read())["city"]

loc = json.loads(urllib.request.urlopen(
    "https://ipinfo.io/").read())["loc"].split(",")


class Main:

    def __init__(self):
        self.user = None

    def destroy_children(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def weather(self):
        tk.Label(root, text="Weather").grid(row=0, column=0, sticky="W")

        self.res = urllib.request.urlopen(
            f"https://api.open-meteo.com/v1/forecast?latitude=54.90&longitude=-1.38&hourly=temperature_2m,precipitation&windspeed_unit=ms&start_date=2023-02-15&end_date=2023-02-22")
        self.weatherData = json.loads(self.res.read())

        fig, ax = plt.subplots()

        ax2 = ax.twinx()
        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        ax.set_ylabel("Temp (C)", color="g")
        ax2.set_ylabel("Precipitation (mm)", color="b")

        ax.plot(self.weatherData["hourly"]["time"],
                self.weatherData["hourly"]["temperature_2m"], "g-")
        ax2.plot(self.weatherData["hourly"]["time"],
                 self.weatherData["hourly"]["precipitation"], "b-")

        plt.xticks(
            [i for i in range(0, len(self.weatherData["hourly"]["time"]), 12)])

        plt.show()

        labels = [tk.Label(root, text=(f'{d[0]}: {d[1]}'))
                  for d in list(self.weatherData.items())[0:6]]

        for i, label in enumerate(labels):
            label.grid(column=0, row=i+1, sticky="W")

        tk.Button(root, text="Back", command=lambda: (
            self.destroy_children(root), self.home())).grid(row=len(labels)+1, column=0, sticky="W")

    def air_quality(self):
        tk.Label(root, text="Air Quality").grid(row=0, column=0, sticky="W")

        self.res = urllib.request.urlopen(
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude=54.90&longitude=-1.38&hourly=pm10,pm2_5,european_aqi&start_date=2023-02-15&end_date=2023-02-20")
        self.airData = json.loads(self.res.read())

        fig, ax = plt.subplots()

        ax2 = ax.twinx()
        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        ax.set_ylabel("µg/m3", color="g")
        ax2.set_ylabel("EAQI", color="b")

        ax.plot(self.airData["hourly"]["time"],
                self.airData["hourly"]["pm10"], "g-")

        ax.plot(self.airData["hourly"]["time"],
                self.airData["hourly"]["pm2_5"], "r-")

        ax2.plot(self.airData["hourly"]["time"],
                 self.airData["hourly"]["european_aqi"], "b-")

        plt.xticks(
            [i for i in range(0, len(self.airData["hourly"]["time"]), 12)])

        plt.show()

        labels = [tk.Label(root, text=(f'{d[0]}: {d[1]}'))
                  for d in list(self.airData.items())[0:6]]

        for i, label in enumerate(labels):
            label.grid(column=0, row=i+1, sticky="W")

        tk.Button(root, text="Back", command=lambda: (
            self.destroy_children(root), self.home())).grid(row=len(labels)+1, column=0, sticky="W")

    def advice(self):
        tk.Label(root, text="Get help").grid(column=0, row=0, sticky="W")

        tk.Button(root, text="Back", command=lambda: (
            self.destroy_children(root), self.home())).grid(row=1, column=0, sticky="W")

    def home(self):
        tk.Label(root, text="Home").grid(column=0, row=0)
        # company_label = tk.Label(root, text="Home").grid(column=0, row=0)
        tk.Label(
            root, text=f"Welcome {self.user[1]}!").grid(column=0, row=1)

        tk.Button(
            root, text="Weather Forecasting", command=lambda: (self.destroy_children(root), self.weather())).grid(column=0, row=2)
        tk.Button(
            root, text="Air Quality Data", command=lambda: (self.destroy_children(root), self.air_quality())).grid(column=0, row=3)
        tk.Button(root, text="Advice", command=lambda: (
            self.destroy_children(root), self.advice())).grid(column=0, row=4)

    def validation(self, username, password, login):
        if login:
            sql = "SELECT * FROM Details WHERE Username = ? AND Password = ?"
            c.execute(sql, (username, password))
            self.user = c.fetchone()

            if self.user != None:
                # print(self.user)
                self.destroy_children(root)
                self.home()
        else:
            if len(username) > 3 and len(password) > 3:
                already_exists = "SELECT * FROM Details WHERE Username = ?"
                already_exists = c.execute(already_exists, (username,))
                if already_exists.fetchone() == None:
                    query = "INSERT INTO Details(Username, Password) VALUES(?,?)"
                    c.execute(query, (username, password))
                    conn.commit()

                    sql = "SELECT * FROM Details WHERE Username = ? AND Password = ?"
                    c.execute(sql, (username, password))
                    self.user = c.fetchone()
                    # print(self.user)

                    self.destroy_children(root)
                    self.home()
                else:
                    tk.Label(
                        root, text="Username already Taken!").grid(column=0, row=5)
            else:
                tk.Label(
                    root, text="Username and Password need to be atleast 4 characters!").grid(column=0, row=6)

    def sign_up(self):
        tk.Label(root, text="Register").grid(column=0, row=0)

        username_label = tk.Label(root, text="Username: ")
        username_label.grid(column=0, row=1)
        password_label = tk.Label(root, text="Password: ")
        password_label.grid(column=0, row=2)
        username_entry = tk.Entry(root)
        username_entry.grid(column=1, row=1)
        password_entry = tk.Entry(root)
        password_entry.grid(column=1, row=2)

        tk.Button(root, text="Submit", command=lambda: self.validation(
            username_entry.get(), password_entry.get(), False)).grid(column=0, row=3)
        tk.Label(
            root, text="Already have an Account?").grid(column=0, row=4)
        tk.Button(root, text="Login", command=lambda: (
            self.destroy_children(root), self.login())).grid(column=1, row=4)

    def login(self):
        tk.Label(root, text="Login").grid(column=0, row=0)

        username_label = tk.Label(root, text="Username: ")
        username_label.grid(column=0, row=1)
        password_label = tk.Label(root, text="Password: ")
        password_label.grid(column=0, row=2)
        username_entry = tk.Entry(root)
        username_entry.grid(column=1, row=1)
        password_entry = tk.Entry(root)
        password_entry.grid(column=1, row=2)

        tk.Button(root, text="Submit", command=lambda: self.validation(
            username_entry.get(), password_entry.get(), True)).grid(column=0, row=3)
        tk.Label(
            root, text="Dont have an Account?").grid(column=0, row=4)
        tk.Button(root, text="Register", command=lambda: (
            self.destroy_children(root), self.sign_up())).grid(column=1, row=4)


if __name__ == "__main__":
    main = Main()
    main.login()
    root.mainloop()
