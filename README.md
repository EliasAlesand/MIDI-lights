# MIDI-lights
Small Python program to visualize MIDI files on an addressable NeoPixel LED Strip via a Raspberry Pi.
## Usage
Usage of this program requires a Raspberry Pi and a [NeoPixel LED strip](https://www.adafruit.com/category/168).  
Confirmed to work with Python 2.7.9, a Raspberry Pi 3 Model B and a 144 LED NeoPixel.

Useful links for wiring:  
https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring  
https://learn.adafruit.com/adafruit-neopixel-uberguide/best-practices   

Follow [this guide](https://learn.adafruit.com/neopixels-on-raspberry-pi/software) to download the necessary package to control the LED strip from the Raspberry Pi and try the examples to make sure that the LED strip is wired and works correctly. If the LED lights are flickering, try editing `/boot/config.txt` and add the lines `hdmi_force_hotplug=1` and `hdmi_force_edid_audio=1`.


Run the program with the command:  
`sudo python MIDI-lights.py -s 'midi filename'`

There are some optional flags:
* ```-b``` - Sets LED brightness. Integer value in the range 0-255. Default value is 50.
* ```-p``` - Sets the pace that the MIDI file is read. Default value is 1. 2 will double the pace and 0.5 will halve the pace etc.
* ```-d``` - Debug flag. If present, each MIDI message will be printed to standard output. No value required.  

Some customization require code changes:  
* The dictionary `MIDI_TO_LED` maps MIDI notes to specific LED lights on the strip. The setup in the source code maps MIDI notes to LED
 lights such that they line up with keys on a physical piano.
* Each MIDI channel is assigned a color that will show up on the LED lights. In the source code they are set to some arbitrarily chosen colors in the dictionary `COLORS` and can be changed to the users preference.
## Dependencies
[rpi_ws281x](https://github.com/jgarff/rpi_ws281x) is used to control the LED strip from the Raspberry Pi.  
[Mido](https://github.com/olemb/mido) is used to convert MIDI files to easy to work with objects.

## Future additions
Support to take real time input from a MIDI source.

## Contact
elias.alesand@gmail.com
