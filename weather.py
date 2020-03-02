from flask import Flask, render_template, request, send_file
import json
import requests


app = Flask(__name__)

key = "5475563c6ff5899cef48ce5c77b2ebfc"

@app.route('/', methods =['POST','GET'])
def weather():
    output = {}
    if request.method == 'POST':
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
        city = request.form.get('city')
        city = city.replace(" ","%20")
        formatted_url = url.format(city,key)
        resp = requests.get(formatted_url)
        if resp:
            data = resp.json()
            description = data['weather'][0]['description']
            temp = int(round(kelvin_to_fahrenheit(float(data['main']['temp']))))
            temp_min = int(round(kelvin_to_fahrenheit(float(data['main']['temp_min']))))
            temp_max = int(round(kelvin_to_fahrenheit(float(data['main']['temp_max']))))
            city = city.replace("%20"," ").strip()
            output = {"city" : city, "description" : description, "temp" : temp, "temp_min" : temp_min, "temp_max" : temp_max}
            return render_template('weather.html',data=output)
        else:
            return "Invalid City Name"
    return send_file("templates/index.html")


def kelvin_to_fahrenheit(temp):
    return (temp - 273.15) * (9 / 5) + 32


if __name__ == '__main__':
    app.run(debug = True)
