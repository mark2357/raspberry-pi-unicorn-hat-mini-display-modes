# Raspberry pi Unicorn Hat Mini Display Modes

This project runs several different leds effects that can be controlled via a basic web interface. These scripts are designed to run on a raspberry pi zero with a unicorn hat mini hat.

## Modes
Using the web interface and you can switch between the different display modes.
You can set the default display mode in the config file

### asx stock text mode
Display information about specified stocks. It displays the asx code and current stock price, if the stock has gone up since the start of the day the text is display as green if the price has gone down the text will be displayed as red.
The Stock data is scraped from the asx website so the data is delayed.

#### mode config settings
|Name|Type|Description|
|---|---|---|
|UPDATE_INTERVAL|number|the number of seconds before the data is updated from the webpage|
|STOCK_CODES|Array of strings| the stock codes to scrape and display|
|SHORTEN_TEXT|boolean| if the text should be shortened to just show the asx code and price|


### clock mode
Displays the current time in 24 or 12 hour time with either plain white or colored text.

#### mode config settings
|Name|Type|Description|
|---|---|---|
|HOUR_12_TIME|boolean| if 12 hour time should be used instead of 24 hour time
|PLAIN_COLOR|boolean| if a plain white color is used for the text or if the wide range of colors are used|
|COLOR_ROTATION_SPEED|number| how fast the colors wave rotates around the center point of the led screen |
|COLOR_PAN_SPEED|number| how fast the colors move vertically or horizontally across the screen |
|COLOR_SPACING|number| how fast the hue (color) changes based on the screen position 


### color wave mode
Displays circular colored waves that move outward from origin points on the screen.

#### mode config settings
|Name|Type|Description|
|---|---|---|
|NUMBER_OF_POINTS|number| the number of wave points / origin that are created at the same time (new points are created once the waves finish moving off screen)


### covid 19 new cases text
Displays the number of covid 19 cases for the day and previous day for the Australian state of Victoria.
The data is scraped from https://covidlive.com.au/vic

#### mode config settings
|Name|Type|Description|
|---|---|---|
|UPDATE_INTERVAL|number|the number of seconds before the data is updated from the webpage|


### custom text
Custom text mode allows the user to display custom text on screen that is repeated, the custom text can be set via the web page / interface and a default text can be set in the config

#### mode config settings
|Name|Type|Description|
|---|---|---|
|INITIAL_CUSTOM_TEXT|string|the initial test that should be shown if the text is set as the initial custom text|


### numbers fact text
Displays random number facts from the number facts api
webpage can be found here: http://numbersapi.com
specific API: http://numbersapi.com/random


### pixel rain
Displays a changing colored background with several pixels moving down the screen 

#### mode config settings
|Name|Type|Description|
|---|---|---|
|NUMBER_OF_PIXELS|number|the number of seconds before the data is updated from the webpage|
|UPDATE_POSITION_EVERY_X_FRAMES|number|the number of frames between |
|COLOR_ROTATION_SPEED|number|the speed at which the background color changes hue|


### poke random info text
Displays text with random information about pokemon
using the python module random-pokemon-info
which gets data from the web api https://pokeapi.co/


## accessing the web interface / webpage
The web interface can be accessed on port 8080 of the raspberry pi
You can access the web page from any standard web browser
e.g. from the url x.x.x.x:8080 with the four x are replaced with is replaced with the ip address of the raspberry pi



## dependencies

python 3 (will not work correctly with python 2.7)

### python modules
the following python modules are required
requests
requests-cache
pillow
unicornhatmini
web.py

random-pokemon-info (custom module I created available from https://github.com/mark2357/random-pokemon-info)


## setup
copy the ```config_example.ini``` and rename it config.ini

install the dependencies modules by running the following command

```
pip install requests requests-cache pillow unicornhatmini web.py
```

to install random-pokemon-info please follow the installation instructions here: https://github.com/mark2357/random-pokemon-info

## running scripts
There are several script that are designed to be run via the command line.

### running the project
The module can be run by calling the run.py script
```
python3 run.py
```

### webserver only
You can run the webserver without running the led display. This is useful for development of the web interface on a standard computer.

```
python3 webserver_only.py
```

### forcefully stopping the script
This is useful if you have setup the script to run automatically at startup e.g. via crontab.

```
bash stop_run.sh
```

## settings
The possible settings can be found the config.ini file
once these values are changed the script must be restarted for it's effects to take effect.


### general settings
General settings that effect all the modes or none of the modes.

|Name|Type|Description|
|---|---|---|
|BRIGHTNESS|number| the brightness of the screen 0 - 1 value range recommend to keep at a low value|
|ROTATION|number| should be either 0, 180 specifies if the screen should be rotated |
|INITIAL_MODE_ID|string| should be one of the value below, specifies which mode the script should start on

valid mode id values:
- asx_stock_text_mode
- clock_mode
- color_wave_mode
- covid_19_new_cases_text_mode
- custom_text_mode
- numbers_fact_text_mode
- pixel_rain_mode
- poke_random_info_text_mode


### settings in each mode
These settings are available for each mode.

|Name|Type|Description|
|---|---|---|
|ENABLED|number| if the mode is enabled if this is set to false the mode will not be visible in the web interface and cannot be set as a default mode|
|FPS|number| the target fps for this mode, a higher framerate will make the mode run faster |
