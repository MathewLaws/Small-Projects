import json
import turtle
import urllib.request
import time

url = "http://api.open-notify.org/astros.json"

response = urllib.request.urlopen(url)
result = json.loads(response.read())

print(f"people in space {result['number']}")

people = result["people"]

for p in people:
    print(p["name"], "in", p["craft"])

print()

url = "http://api.open-notify.org/iss-now.json"

response = urllib.request.urlopen(url)
result = json.loads(response.read())

location = result["iss_position"]
iss_lat = float(location["latitude"])
iss_long = float(location["longitude"])
print(f"latitude: {iss_lat}")
print(f"longitude: {iss_long}")

screen = turtle.Screen()
screen.setup(720, 360)
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic("map.gif")

screen.register_shape("rocketship.gif")
iss = turtle.Turtle()
iss.shape("rocketship.gif")
iss.setheading(90)
iss.penup()

lat = 54.896230
long = -1.409024

location = turtle.Turtle()
location.penup()
location.goto(long, lat)
location.dot(5)
location.ht()

url = 'http://api.open-notify.org/iss-pass.json?lat=' + str(lat) + '&lon=' + str(long)
response = urllib.request.urlopen(url)
result = json.loads(response.read())

over = result['response'][1]['risetime']
location.write(time.ctime(over))


iss.goto(iss_long, iss_lat)


