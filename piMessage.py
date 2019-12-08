from lcd1602a.lcd1602a import *
import httplib2
import urllib
import json
from datetime import datetime

def heWeatherNow(city):
    key = "your key"
    url = "https://free-api.heweather.net/s6/weather?"
    myurl = url + "&lang=en&location=" + urllib.parse.quote(city) + "&key=" + key
    try:
        httpClient = httplib2.Http()
        response, content = httpClient.request(myurl)
        result = json.loads(content)
        weatherMessage = result['HeWeather6'][0]
        location = weatherMessage['basic']['location']
        temperature = weatherMessage['now']['tmp']
        weatherNow = weatherMessage['now']['cond_txt']
        r = (location, temperature, weatherNow)
    except:
        r = None
    finally:
        return r

def displayTimeMessage():
    weekday = datetime.now().strftime("%A")
    dateAndTime = datetime.now().strftime("%Y-%m-%d %H:%M")
    clearScreen()
    writeString(weekday + "\n" + dateAndTime)

def displayCoreTemperature():
    temperature = round(float(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000, 1)
    clearScreen()
    writeString("CPU Temperature:\n" + str(temperature))
    writeCharacterCode(0xdf)
    writeCharacter("C")

def displayWeatherMessage(city):
    weatherMessage = heWeatherNow(city)
    clearScreen()
    writeString(weatherMessage[0] + "  " + weatherMessage[1])
    writeCharacterCode(0xdf)
    writeCharacter('C')
    setCursor(0, 1)
    writeString(weatherMessage[2])

def displayWeatherMessagePer10Min():
    l = [h for h in range(0, 60, 10)]
    minute = int(datetime.now().strftime('%M'))
    if minute in l:
        displayWeatherMessage("澄海")

if __name__ == "__main__":
    try:
        while True:
            displayTimeMessage()
            sleep(20)
            displayCoreTemperature()
            sleep(3)
            displayWeatherMessagePer10Min()
            sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()

