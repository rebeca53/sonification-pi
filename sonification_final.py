import glob, os 
import spidev 
import time 
import datetime 
import RPi.GPIO as GPIO 
import midi
import ftplib

# Open SPI bus
spi = spidev.SpiDev() 
spi.open(0,0)

# Set up the BCM port numbering scheme
GPIO.setmode(GPIO.BCM)

# GPIO 17 set up as inputs, pulled up to avoid flase detection. Connect 
# to GND on button press. So we'll be setting up falling edge detection 
# for it
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configuring a new connection with the pc in use using its ip address
# It is supposed that both pi and pc are in the same network
ftp = ftplib.FTP("10.0.102.175")
print 'Welcome to the FTP Server:', ftp.getwelcome()

# Now we have to login in the FTP server with the user's name and password
ftp.login("felipe alexandre")
# Change from the directory /Pi Sonification (set in the server) to 
# /Pi Sonification\Midi_data_transfer
ftp.cwd("Midi_data_transfer")

# Function to read SPI data from MCP3008 chip Channel must be an integer 
# 0-7
def ReadChannel(channel):
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

# Interrupt function to send '.mid' files and delete them
def DownLink(channel):
	print ("falling edge detected on 17")
	filelist = glob.glob("*.mid")
	print (filelist)
	for f in filelist:
		print ('STOR '+f)
		ftp.storbinary('STOR '+f, open(f, 'rb'))
		os.remove(f)

# When a falling edge is detected on port 17, regardless of whatever 
# else is happening in the program, the function DownLink will be run 
# Bouncing is corrected
GPIO.add_event_detect(17, GPIO.FALLING, callback=DownLink, bouncetime = 300)

# Define sensor channels
light_channel = 0 
temp_channel = 1

# Define delay between readings
delay = 0.5

# Define number of notes per mid file
LIMIT = 70 
eot = midi.EndOfTrackEvent(tick=1) 

while True:
        count = 0
        pattern = midi.Pattern()
        light_track = midi.Track()
        temp_track = midi.Track()
        pattern.append(light_track)
        pattern.append(temp_track)
        l_prev = 0
        t_prev = 0
        while (count < LIMIT):
                # Read the light sensor data
                light_level = ReadChannel(light_channel)/10
                # Read the temperature sensor data
                temp_level = ReadChannel(temp_channel)/5
                
		# Adding notes to track of LIGHT
                if light_level == l_prev:
                        light_track.append(midi.NoteOnEvent(tick=0,channel=0,data=[light_level,75]))
                else:
                        light_track.append(midi.NoteOffEvent(tick=100,pitch = l_prev))
                        light_track.append(midi.NoteOnEvent(tick=101,channel=0,data=[light_level,75]))
                l_prev = light_level
                
		# Adding notes to track of TEMPERATURE
                if t_prev == temp_level:
                        temp_track.append(midi.NoteOnEvent(tick=0,channel=0,data=[temp_level,75]))
                else:
                        temp_track.append(midi.NoteOffEvent(tick=100, pitch=t_prev))
                        temp_track.append(midi.NoteOnEvent(tick=101, channel=0, data=[temp_level,75]))
                t_prev = temp_level

                #Print out results
                print("---------------------------------")
                print("Light : {}".format(light_level))
                print("Temp: {}".format(temp_level))
                time.sleep(delay)
                count +=2
        light_track.append(eot)
        temp_track.append(eot)
        
        print("\n Creating file ===================== \n")
	ts = time.time()
	fileName = 'Time_'+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%Hh%Mm%Ss')+'.mid'
        print (fileName)
        midi.write_midifile(fileName, pattern)
#        open(datetime.datetime.now().strftime("%I:%M:%S")+'.mid', 'a').close()
        
GPIO.cleanup() # clean up GPIO on exit
