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

# Running the code
The code must be run in a Raspberry Pi with light and temperature sensors and a push button.
In a few lines what the code does is:
- Pi get data from the sensors
- Write the data as Events in a Pattern
- Get the Pattern into a MIDI file
- Send the MIDI file via FTP to a PC
- Erase the MIDI file from the Pi

It is important to have your computer set as a server:
- Windows: Install FileZilla, configure it and set rule on firewall
- Linux: Just follow instructions from https://www.atlantic.net/community/howto/install­an­ftp­server/
and
https://www.benscobie.com/fixing­500­oops­vsftpd­refusing­to­run­with­writable­root-inside­chroot/
