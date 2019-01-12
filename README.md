# LED Wall Picture

## Setup & Install on a Raspberry Pi

Install neopixel for raspberry pi
```bash
cd rpi_ws281x
sudo apt-get install build-essential python-dev git scons swig
scons
git clone https://github.com/jgarff/rpi_ws281x
cd python
sudo python ./setup.py install
cd ../..
```

Test that everything is gooing good so far run: `sudo python rpi_ws281x/examples/strandtest.py`

Install and run this project
```bash
git clone https://github.com/ingo-eichhorst/led-wall-picture
cd led-wall-picture
sudo pip install -r requirements.txt
npm install
```

## Start app via CLI

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

## Setup and run Web Server

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

Access server at: http://[ip]:5000
