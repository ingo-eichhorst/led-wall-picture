#!/usr/bin/env python3

import time
from neopixel import *
import argparse
import datetime
from astral import Astral

# LED strip configuration:
LED_COUNT      = 450      # Number of LED pixels.
LED_PIN        = 18       # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0        # set to '1' for GPIOs 13, 19, 41, 45 or 53
# Timing Configuration
TIMING_CITY    = 'Berlin'       # City for gathering the sunset and sunrise times
TIMING_TRANSITION_SIM = 3 * 60 * 60 # Transition time in seconds from night to sunset, sunset to day, ... (in sim mode 5 Min.)
TIMING_TRANSITION_DAY = 30 * 60 # Transition time in seconds in normal mode (24h)
SIM_DURATION = 5 * 60           # Duration of a simulated day

# Color settings for time of the day
nightColors = {
  "ground": [0,0,0],
  "horizon": [0,3,37],
  "sky": [0,3,37],
  "castle": [255,80,0],
  "moon": [184,164,153],
  "stripe": [255,80,0]
}
dayColors = {
  "castle": [150,200,200],
  "ground": [150,200,200],
  "horizon": [150,200,200],
  "sky": [150,200,200],
  "moon": [150,200,200],
  "stripe": [150,200,200]
}
sunriseColors = {
  "castle": [20,10,10],
  "ground": [20,10,10],
  "horizon": [255,40,0],
  "sky": [22,50,90],
  "moon": [22,50,90],
  "horizon": [255,40,0],
  "stripe": [255,40,0]
}

# pixel areas positions on the wall picture
areas =	{
  "sky": [[85,90],[110,175]],
  "horizon": [[45,65],[175,215]],
  "ground": [[0,45],[215,255],[265,400]],
  "moon": [[90, 110]],
  "castle": [[255, 265]],
  "stripe": [[400, 450]]
}

def monoColor(strip, color):
  if (color == 'off'):
    colorCode = Color(0,0,0)
  elif (color == 'on'):
    colorCode = Color(255,255,255)
  elif (color == 'red'):
    colorCode = Color(80,80,80)
  print('switching colors...')
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, colorCode)
  strip.show()

def nightMode(strip):
  print('switching colors...')
  for i in range(strip.numPixels()):
    # Moon
    if i > 90 and i < 110:
      strip.setPixelColor(i, Color(164,184,153))
    # Light up the castle
    elif i > 255 and i < 265:
      strip.setPixelColor(i, Color(80,255,0))
    # Make bottom dark
    elif i < 45 or i > 200:
      strip.setPixelColor(i, Color(0,0,0))
    else:
      strip.setPixelColor(i, Color(3,0,37))
  strip.show()

def sunriseMode(strip):
  print('switching colors...')
  for i in range(strip.numPixels()):
    # Ground Brown
    if i > 215:
      strip.setPixelColor(i, Color(10,20,10))
    # Sunrise
    elif i > 45 and i < 65:
      strip.setPixelColor(i, Color(40,255,0))
    elif i > 190 and i < 215:
      strip.setPixelColor(i, Color(40,255,0))
    # Low Sky
    elif i > 65 and i < 85:
      strip.setPixelColor(i, Color(50,22,90))
    elif i > 160 and i < 190:
      strip.setPixelColor(i, Color(50,22,90))
    # High Sky
    elif i > 85 and i < 160:
      strip.setPixelColor(i, Color(22,0,50))
  strip.show()

def dayMode(strip):
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(200,200,200))
  strip.show()

def colorTimer(strip, dayTime, sunrise, sunset, transition_timing):
  # seperated the day in 86400 Steps
  transitionLength = transition_timing
  # night -> dawn (surise - 30 min)
  if (dayTime <= sunrise  - transitionLength):
    print('NIGHT')
    setAllPixelsByTime(strip, nightColors, nightColors, 100)
  # night -> sunrise
  elif (dayTime <= sunrise):
    print('NIGHT -> SUNRISE')
    progress = 100 - ((sunrise - dayTime) * 100)/transitionLength
    setAllPixelsByTime(strip, nightColors, sunriseColors, progress)
  # sunrise -> day
  elif (dayTime <= sunrise + transitionLength):
    print('SUNRISE -> DAY')
    progress = 100 - ((sunrise + transitionLength - dayTime) * 100)/transitionLength
    setAllPixelsByTime(strip, sunriseColors, dayColors, progress)
  # day
  elif (dayTime <= sunset - transitionLength):
    print('DAY')
    setAllPixelsByTime(strip, dayColors, dayColors, 100)
  # day (sunset - 30 min) -> sunset
  elif (dayTime <= sunset):
    print('DAY -> SUNSET')
    progress = 100 - ((sunset - dayTime) * 100)/transitionLength
    setAllPixelsByTime(strip, dayColors, sunriseColors, progress)
  # sunset -> night
  elif (dayTime <= sunset + transitionLength):
    print('SUNSET -> NIGHT')
    progress = 100 - ((sunset + transitionLength - dayTime) * 100)/transitionLength
    setAllPixelsByTime(strip, sunriseColors, nightColors, progress)
  # night
  elif (dayTime > sunset + transitionLength):
    print('NIGHT')
    setAllPixelsByTime(strip, nightColors, nightColors, 100)

def getTimeOfDayInSeconds ():
  currentTime = datetime.datetime.now()
  return (currentTime.hour * 60 * 60) + (currentTime.minute * 60) + currentTime.second

def getSunTimes ():
  city_name = TIMING_CITY
  a = Astral()
  a.solar_depression = 'civil'
  city = a[city_name]
  timezone = city.timezone
  sun = city.sun(date=datetime.datetime.now(), local=True)
  sunriseSeconds = ((sun['sunrise']).hour * 60 * 60) + ((sun['sunrise']).minute * 60)
  sunsetSeconds = ((sun['sunset']).hour * 60 * 60) + ((sun['sunset']).minute * 60)
  return sunriseSeconds, sunsetSeconds

def getTimeOfDayInSecondsSimulated(dayDuration):
  currentTime = datetime.datetime.now()
  partsOfDay = 86400 / dayDuration
  currentTimeSeconds = (currentTime.hour * 60 * 60) + (currentTime.minute * 60) + currentTime.second
  currentPart = currentTimeSeconds / dayDuration
  currentTimeSecondsSimulated = currentTimeSeconds - currentPart * dayDuration
  simulatedDayTime = currentTimeSecondsSimulated * partsOfDay
  return simulatedDayTime

def simulateDay(strip, sim_activate, transition_timing):
  while True:
    if (sim_activate == True):
      secondsInDay = getTimeOfDayInSecondsSimulated(SIM_DURATION)
    else:
      secondsInDay = getTimeOfDayInSeconds()
    print('------------------------')
    print('Seconds of day passed: ' + str(secondsInDay))
    sunrise, sunset = getSunTimes()
    print('Sunrise: ' + str(sunrise) + '; Sunset: ' + str(sunset))
    colorTimer(strip, secondsInDay, sunrise, sunset, transition_timing)
    time.sleep(1)

def setAllPixelsByTime(strip, lastColors, nextColors, transitionProgress):
  if (transitionProgress > 100):
    transitionProgress = 100
  print('Transition progress: ' + str(transitionProgress))
  lastColor = [0,0,0]
  for pixel in range(strip.numPixels()):
    colors = getColorForPixel(lastColors, nextColors, pixel, transitionProgress)
    strip.setPixelColor(pixel, Color(int(colors[1]),int(colors[0]),int(colors[2])))
    lastColor = colors
  print('Color of last Pixel: ' + str(lastColor))
  strip.show()

def getTransitionColor(start,end,progress):
  transitionColor = ((end-start)*progress/100)+start
  return transitionColor

def getAreaPosition(pixel):
  selectedArea = "ground"
  for area, coordinatesList in areas.items():
    for coordinates in coordinatesList:
      if (pixel > coordinates[0] and pixel < coordinates[1]):
        selectedArea = area
  return selectedArea

def getColorForPixel(lastColorMap, nextColorMap, pixel, transitionProgress):
  area = getAreaPosition(pixel)
  lastColor = lastColorMap[area]
  nextColor = nextColorMap[area]
  colorArray = [
    getTransitionColor(lastColor[0],nextColor[0],transitionProgress),
    getTransitionColor(lastColor[1],nextColor[1],transitionProgress),
    getTransitionColor(lastColor[2],nextColor[2],transitionProgress)
  ]
  return colorArray

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', '--night', action='store_true', help='night mode')
  parser.add_argument('-r', '--sunrise', action='store_true', help='sunrise mode')
  parser.add_argument('-d', '--day', action='store_true', help='day mode')
  parser.add_argument('-s', '--simulate', action='store_true', help='simulate day')
  parser.add_argument('-q', '--quicksim', action='store_true', help='simulate day in 5 minutes')
  parser.add_argument('-f', '--off', action='store_true', help='switch off')
  parser.add_argument('-o', '--on', action='store_true', help='switch on')
  parser.add_argument('-e', '--red', action='store_true', help='switch red')
  args = parser.parse_args()

  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()

  if args.night:
    nightMode(strip)
  elif args.sunrise:
    sunriseMode(strip)
  elif args.day:
    dayMode(strip)
  elif args.simulate:
    simulateDay(strip, False, TIMING_TRANSITION_DAY)
  elif args.quicksim:
    simulateDay(strip, True, TIMING_TRANSITION_SIM)
  elif args.off:
    monoColor(strip, 'off')
  elif args.on:
    monoColor(strip, 'on')
  elif args.red:
    monoColor(strip, 'red')