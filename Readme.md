#Smart Mirror

I had another project called FRIDAY-JAVA, this is basically that but re-written in python and with a GUI


![alt text](https://raw.githubusercontent.com/alhockly/FRIDAY-Mirror/master/Servingsuggestion.jpg)


This project will probably be moved over x86 hardware due to incompatibilities and the fact that the rpi isn't really powerful enough for voice recognition and driving a display

#Steps#
1. install libraries
	sudo pip3 install selenium selenium-requests numpy eel forex-python simpleaudio kamene netaddr geocoder pyaudio SpeechRecognition

(PortAudio is a C library required for pyaudio, on windows you;ll have to install from here: https://people.csail.mit.edu/hubert/pyaudio/packages/ ??)
	
	On linux/rpi install from apt-get as below

	sudo apt-get update &&
	sudo apt-get upgrade &&
	sudo apt-get install portaudio19-dev tcpdump flac libatlas-base-dev python-pyaudio python3-pyaudio sox libpcre3 libpcre3-dev libatlas-base-dev -y
	

2.Compile a supported swig version (3.0.10 or above) and snowboy for python3
	wget https://sourceforge.net/projects/swig/files/swig/swig-3.0.10/swig-3.0.10.tar.gz &&
	tar -xvzf swig-3.0.10.tar.gz &&
	cd swig-3.0.10/ &&   
	./configure --prefix=/usr                  \
			--without-clisp                    \
			--without-maximum-compile-warnings &&
	sudo make &&
	sudo make install &&
	sudo install -v -m755 -d /usr/share/doc/swig-3.0.10 &&
	sudo cp -v -R Doc/* /usr/share/doc/swig-3.0.10 &&
	cd ..

	git clone https://github.com/Kitt-AI/snowboy &&
	cd snowboy/swig/Python3 && make

3. Hardware stuff
	You can use pretty much any monitor that is flat(ish). Im using a decapitated laptop screen with LVDS driver seperate. 2 way 		acrylic can be glued on top but I used command velcro strips so that I can take this thing apart when I move or need the parts.
	If the monitor you use has poor black values then I highly reccomend placing a 0.9 ND gel filter between the monitor and the 		acrylic to reduce emitted light (especially in the dark). if 0.9 filter is expensive you can also use a 0.3 nd and 0.6 nd filter 	together. The exact filter nessessary does depend on the screen being used so bare that in mind

##Start Mirror##
1. ssh in and `export DISPLAY=:0.0`
2. start FRIDAY-Mirror.py
3. open browser to http://localhost:8000/web/main.html

