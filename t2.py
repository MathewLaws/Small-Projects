# import the required modules
import urllib.request
import json
import tkinter as tk
import tkinter.font
import sqlite3
import matplotlib.pyplot as plt
import datetime
import customtkinter
from PIL import Image, ImageTk

# create the GUI
root = customtkinter.CTk()

# resize the GUI to fit
root.geometry("700x700")

# change background colour
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

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
    customtkinter.CTkLabel(root, text="Weather",
                           font=("Helvetica", 20)).grid(row=0,
                                                        column=0,
                                                        sticky="W", padx=10)

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
      customtkinter.CTkLabel(root,
                             text=(f"{d[0]}: {d[1]}"),
                             font=("Helvetica", 15))
      for d in list(self.weatherData.items())[0:6]
    ]

    for i, label in enumerate(labels):
      label.grid(column=0, row=i + 1, sticky="W", padx=10)

    # back button
    customtkinter.CTkButton(
      root,
      text="Back",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.home()),
    ).grid(row=len(labels) + 1, column=0, sticky="W", pady=3, padx=10)

  def air_quality(self):
    # title
    customtkinter.CTkLabel(root, text="Air Quality",
                           font=("Helvetica", 20)).grid(row=0,
                                                        column=0,
                                                        sticky="W", padx=10)

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
      customtkinter.CTkLabel(root,
                             text=(f"{d[0]}: {d[1]}"),
                             font=("Helvetica", 15))
      for d in list(self.airData.items())[0:6]
    ]

    for i, label in enumerate(labels):
      label.grid(column=0, row=i + 1, sticky="W", padx=10)

    # back button
    customtkinter.CTkButton(
      root,
      text="Back",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.home()),
    ).grid(row=len(labels) + 1, column=0, sticky="W", pady=3, padx=10)

  def show_hide_label(self, object):
    if object[1]:
      object[0].grid_remove()
    else:
      object[0].grid(row=object[2], column=0, sticky="W", padx=10)

    object[1] = not object[1]
    return object

  def advice(self):

    # title
    customtkinter.CTkLabel(root, text="Advice",
                           font=("Helvetica", 20)).grid(row=0,
                                                        column=0,
                                                        sticky="W", padx=10)

    # advice on the corona virus
    coronaLabel = [
      customtkinter.CTkLabel(
        root,
        text=
        """If you have any of the main symptoms of coronovirus it's important that you get tested as soon as possible:

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
    ).grid(row=1, column=0, sticky="W", padx=10)

    # advice on the flu virus
    fluLabel = [
      customtkinter.CTkLabel(
        root,
        text=
        """Flu can affect people in different ways and can be more serious than you think. The flu vaccination is offered free of charge to people who are at most risk from the effects of the virus to protect them from catching flu and developing serious complications. Find out who is eligible for a free flu jab.

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
    ).grid(row=3, column=0, sticky="W", padx=10)

    # advice on cold weather
    coldLabel = [
      customtkinter.CTkLabel(
        root,
        text=
        """It is important to keep warm in winter both inside and outdoors. Keeping warm can help to prevent colds, flu and more serious health problems.

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
    ).grid(row=5, column=0, sticky="W", padx=10)

    # back button
    customtkinter.CTkButton(
      root,
      text="Back",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.home()),
    ).grid(row=7, column=0, sticky="W", pady=3, padx=10)

  # function to calculate the bmi after the details are entered
  def calculate_bmi(self, h, w):
    if h == "" or w == "":
      return "Fields are empty!"
    try:
      h = float(h)
      w = float(w)
    except:
      return "Invalid datatype!"
    
    res = (w / h) / h

    return f"BMI: {res}"

  def bmi(self):
    # title
    customtkinter.CTkLabel(root, text="BMI Calculator",
                           font=("Helvetica", 20)).grid(row=0,
                                                        column=0,
                                                        sticky="W",
                                                        padx=10)

    # height entry
    customtkinter.CTkLabel(root, text="Height(m): ",
                           font=("Helvetica", 15)).grid(row=1,
                                                        column=0,
                                                        sticky="W",
                                                        padx=10)
    height = customtkinter.CTkEntry(root, font=("Helvetica", 15))
    height.grid(row=1, column=1, sticky="W", padx=10)

    # weight entry
    customtkinter.CTkLabel(root, text="Weight(KG): ",
                           font=("Helvetica", 15)).grid(row=2,
                                                        column=0,
                                                        sticky="W",
                                                        padx=10)
    weight = customtkinter.CTkEntry(root, font=("Helvetica", 15))
    weight.grid(row=2, column=1, sticky="W", padx=10)

    # submit button
    customtkinter.CTkButton(
      root,
      text="Submit",
      font=("Helvetica", 15),
      command=lambda: (bmi_label.configure(
        text=self.calculate_bmi(height.get(), weight.get())
      )),
    ).grid(row=3, column=0, sticky="W", padx=10)

    # bmi label
    bmi_label = customtkinter.CTkLabel(root, text="", font=("Helvetica", 15))
    bmi_label.grid(row=4, column=0, sticky="W", padx=10)

    # back button
    customtkinter.CTkButton(
      root,
      text="Back",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.home()),
    ).grid(row=5, column=0, sticky="W", pady=3, padx=10)

  def switch_mode(self, value):
    if value.get() == "on":
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
                                                        padx=10, pady=3)

    dark_mode = customtkinter.StringVar(value="on")
    
    customtkinter.CTkSwitch(root, text="Dark mode", command= lambda: self.switch_mode(dark_mode),
                                   variable=dark_mode, onvalue="on", offvalue="off").grid(row=1,column=0,sticky="W",padx=10, pady=3)
    
    # back button
    customtkinter.CTkButton(
      root,
      text="Back",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.home()),
    ).grid(row=5, column=0, sticky="W", pady=3, padx=10)
    
  
  def home(self):
    # title
    customtkinter.CTkLabel(root, text="Home",
                           font=("Helvetica", 20)).grid(column=0,
                                                        row=0,
                                                        padx=10)

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

    weatherImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/weather.png"), size=(60,60))
    airImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/air.png"), size=(60,60))
    adviceImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/advice.png"), size=(60,60))
    bmiImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/bmi.png"), size=(60,60))
    settingsImg = customtkinter.CTkImage(dark_image=Image.open("./imgs/settings.png"), size=(60,60))

    # weather forecasting button
    customtkinter.CTkButton(
      root,
      text="Weather Forecasting",
      anchor="w",
      image = weatherImg,
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.weather()),
    ).grid(column=0, row=2, pady=3, sticky="W", padx=10)

    # air quality button
    customtkinter.CTkButton(
      root,
      anchor="w",
      image = airImg,
      text="Air Quality Data",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.air_quality()),
    ).grid(column=0, row=3, pady=3, sticky="W", padx=10)

    # advice button
    customtkinter.CTkButton(
      root,
      anchor="w",
      image = adviceImg,
      text="Advice",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.advice()),
    ).grid(column=0, row=4, pady=3, sticky="W", padx=10)

    # BMI button
    customtkinter.CTkButton(
      root,
      anchor="w",
      image = bmiImg,
      text="BMI Calculator",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.bmi()),
    ).grid(column=0, row=5, pady=3, sticky="W", padx=10)

    # Settings button
    customtkinter.CTkButton(
      root,
      anchor="w",
      image = settingsImg,
      text="Settings",
      font=("Helvetica", 15),
      command=lambda: (self.destroy_children(root), self.settings()),
    ).grid(column=0, row=6, pady=3, sticky="W", padx=10)

    
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
          customtkinter.CTkLabel(root,
                   font=("Helvetica", 15),
                   text_color=("red"),
                   text="Username already Taken!", wraplength=200).grid(column=0, row=5, sticky="W", padx=10)
      else:
        
        # display error message
        customtkinter.CTkLabel(
          root,
          font=("Helvetica", 15),
          text_color=("red"),
          text="Username and Password need to be atleast 4 characters!", wraplength=200).grid(
            column=0, row=6, sticky="W", padx=10)

  def sign_up(self):

    # title
    customtkinter.CTkLabel(root, text="Register",
                           font=("Helvetica", 20)).grid(column=0,
                                                        row=0,
                                                        sticky="W", padx=10)

    # username and password entry boxes and labels
    username_label = customtkinter.CTkLabel(root,
                                            text="Username: ",
                                            font=("Helvetica", 15))
    username_label.grid(column=0, row=1, sticky="W", padx=10)
    password_label = customtkinter.CTkLabel(root,
                                            text="Password: ",
                                            font=("Helvetica", 15))
    password_label.grid(column=0, row=2, sticky="W", padx=10)
    username_entry = customtkinter.CTkEntry(root, font=("Helvetica", 15))
    username_entry.grid(column=1, row=1, sticky="W", padx=10)
    password_entry = customtkinter.CTkEntry(root,
                                            show="*",
                                            font=("Helvetica", 15))
    password_entry.grid(column=1, row=2, sticky="W", padx=10)

    # submit button
    customtkinter.CTkButton(
      root,
      font=("Helvetica", 15),
      text="Submit",
      command=lambda: self.validation(username_entry.get(), password_entry.get(
      ), False),
    ).grid(column=0, row=3, sticky="W", padx=10)

    # option to login if the user already has an account
    customtkinter.CTkLabel(root,
                           text="Already have an account?",
                           font=("Helvetica", 15)).grid(column=0,
                                                        row=4,
                                                        sticky="W", padx=10)
    customtkinter.CTkButton(
      root,
      font=("Helvetica", 15),
      text="Register",
      command=lambda: (self.destroy_children(root), self.login()),
    ).grid(column=1, row=4, sticky="W", padx=10)

  def login(self):

    # title
    customtkinter.CTkLabel(root, text="Login",
                           font=("Helvetica", 20)).grid(column=0,
                                                        row=0,
                                                        sticky="W", padx=10)

    # username and password entry boxes and labels
    username_label = customtkinter.CTkLabel(root,
                                            text="Username: ",
                                            font=("Helvetica", 15))
    username_label.grid(column=0, row=1, sticky="W", padx=10)
    password_label = customtkinter.CTkLabel(root,
                                            text="Password: ",
                                            font=("Helvetica", 15))
    password_label.grid(column=0, row=2, sticky="W", padx=10)
    username_entry = customtkinter.CTkEntry(root, font=("Helvetica", 15))
    username_entry.grid(column=1, row=1, sticky="W", padx=10)
    password_entry = customtkinter.CTkEntry(root,
                                            show="*",
                                            font=("Helvetica", 15))
    password_entry.grid(column=1, row=2, sticky="W", padx=10)

    # submit button
    customtkinter.CTkButton(
      root,
      font=("Helvetica", 15),
      text="Submit",
      command=lambda: self.validation(username_entry.get(), password_entry.get(
      ), True),
    ).grid(column=0, row=3, sticky="W", padx=10)

    # option to login if the user already has an account
    customtkinter.CTkLabel(root,
                           text="Dont have an Account?",
                           font=("Helvetica", 15)).grid(column=0,
                                                        row=4,
                                                        sticky="W", padx=10)
    customtkinter.CTkButton(
      root,
      font=("Helvetica", 15),
      text="Register",
      command=lambda: (self.destroy_children(root), self.sign_up()),
    ).grid(column=1, row=4, sticky="W", padx=10)


# checks that the file is executed directly from the user and not imported
if __name__ == "__main__":

  # initialize a new instance the the "Main" class
  main = Main()

  # call the "login" method
  main.login()

  # run the main loop of the GUI to listen for inputs
  root.mainloop()
