# LED Wall Picture

## Setup & Install on a Raspberry Pi

Install neopixel for raspberry pi
```bash
git clone https://github.com/jgarff/rpi_ws281x
cd /rpi_ws281x/python
sudo python ./setup.py install
cd ../../
```

Install and run this project
```bash
git clone https://github.com/ingo-eichhorst/led-wall-picture
cd led-wall-picture
pip install -r requirements.txt
```

## Start app

### Start with all-white for testing

```bash
sudo python picture.py
```

### Show stills

```bash
sudo python picture.py -n # or --night
                       -r # or --sunrise
                       -d # or --day
                       -o # or --off
```

### Show animation

Sunset and sunrise times are based on the city configured.


```bash
sudo python picture.py -s # or --simulate
```
