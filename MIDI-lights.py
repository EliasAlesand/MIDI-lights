import time
from neopixel import *
import argparse
import mido


# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

MIDI_TO_LED = dict()

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)


# Main program
if __name__ == '__main__':
	# Process arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--song', action='store', dest='song',help='song file', default='songs/canon.mid') # MIDI file
	parser.add_argument('-d', '--debug', action='store_true', help='Print midi messages') # Prints MIDI messages to standard output
	parser.add_argument('-b', '--brightness', action='store',dest='brightness', help='set LED brightness (0-255), default 50', default=50) # Set brightness
	parser.add_argument('-p', '--pace', action='store',dest='pace', help='set song pace multiplier, 1 is normal speed, 2 is double etc.', default=1) # Set song pace
	args = parser.parse_args()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	# Mapping midi notes to LEDs. Set to your own preference. Standard piano notes correspond to MIDI numbers 21-108
	for i in range(27,44):
		MIDI_TO_LED[i]=(i-27)*2
	for i in range(44,72):
		MIDI_TO_LED[i]=(i-27)*2-1
	for i in range(71,100):
		MIDI_TO_LED[i]=(i-27)*2-2
	b = int(args.brightness)
	# Channel colors. Set to your own preference.
	COLORS = {0:Color(b,0,0),1:Color(b/3,2*b/3,0),2:Color(0,0,b),3:Color(b/2,b/2,0),4:Color(b/2,0,b/2),5:Color(0,b/2,b/2)}
	print ('Press Ctrl-C to quit.')
	try:
		midi = mido.MidiFile(args.song)
		if args.debug:
			print(midi.tracks)
		# Set tracks to different channels to distinguish between left/right hand if the MIDI file keeps them in different tracks
		for i in range (0,len(midi.tracks)):
			for msg in midi.tracks[i]:
				if not msg.is_meta:
					msg.channel = i
		for msg in midi:
			try:
				time.sleep(msg.time*(1/float(args.pace)))
				if args.debug:
					print(msg)
				if msg.type == 'note_on':
					if msg.velocity >0: # Sometimes a 'note_on' message with velocity 0 is used instead of a 'note_off' message.
						color = COLORS[msg.channel]
						key = MIDI_TO_LED[msg.note]
						strip.setPixelColor(key,color)
						strip.show()
					else:
						key = MIDI_TO_LED[msg.note]
						strip.setPixelColor(key,Color(0,0,0))
						strip.show()

				if msg.type  == 'note_off':
					key = MIDI_TO_LED[msg.note]
					strip.setPixelColor(key,Color(0,0,0))
					strip.show()
			except Exception as e:
				print(e)
			
	except KeyboardInterrupt: # Turn off all LEDs on keyboard interrupt
		colorWipe(strip, Color(0,0,0), 10)
