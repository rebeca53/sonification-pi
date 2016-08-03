# sonification-pi
A sonification code that converts sensors data into MIDI files. 

# About us
This project was developed during the 2016 CubeSat Bootcamp Summer Program  at Capitol Technology University (Laurel, MD). This specific project was oriented by Professor Antunes.
The team is:
Rebeca Nunes Rodrigues
Rodrigo J. de Bem
Marcelo Moreira Nicoletti
Felipe Alexandre L. de Abreu

# About the project
Data sonification is a useful technique that enable multitasking while "reading" data. It consists on converting numbers into sound. This project intends to apply sonification to PiSat data. In specific, get sensors data from a Raspberry Pi and convert into midi files. The MIDI files are then sent to a PC Linux (the "ground station") via FTP. It is a nearly Real Tie Process.
### The MIDI files
It is a way to store sound in a small space. It is a command based file and the commands are called Events.
Events can be described by:
- Velocity: the amplitude or how "strong" a piano key is pressed.
- Pitch: the frequency, i.e., which key of a piano, a Do (C) or a Mi (E)?
- Tick: the start time or the relative time when the event ocurred. The actual event is equal to the tick + sum of all previous events ticks.

### python-midi library
The library we used to the MIDI part is the python-midi. You can find it at https://github.com/vishnubob/python-midi .<br />

# Running the code
The code must be run in a Raspberry Pi with light and temperature sensors and a push button.
In a few lines what the code does is:
In a loop:
- Pi get data from the sensors
- Write the data as Events in a Pattern
- Get the Pattern into a MIDI file
Everytime a interrupt (caused by a push button) happens:
- Send the MIDI file via FTP to a PC
- Erase the MIDI file from the Pi

It is important to have your computer set as a server:
- Windows: Install FileZilla, configure it and set rule on firewall
- Linux: Just follow instructions from https://www.atlantic.net/community/howto/install­an­ftp­server/
and
https://www.benscobie.com/fixing­500­oops­vsftpd­refusing­to­run­with­writable­root-inside­chroot/
