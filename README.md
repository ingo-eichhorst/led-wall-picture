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
                       -q # or --quicksim (simulates one day every 5 minutes)
```

## Web-App

Install Node
```bash
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v
```

Run on boot and restart on crash with pm2
```bash
sudo npm i -g pm2
sudo pm2 startup
sudo pm2 start server.js
sudo pm2 save
```