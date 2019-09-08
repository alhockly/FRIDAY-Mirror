#Smart Mirror

I had another project called FRIDAY-JAVA, this is basically that but re-written in python and with a GUI


This project will probably be moved over x86 hardware due to incompatibilities and the fact that the rpi isn't really powerful enough for voice recognition and driving a display

#Steps#
1. install libraries
	sudo pip3 install selenium selenium-requests numpy eel forex-python simpleaudio kamene netaddr geocoder pyaudio SpeechRecognition

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


##Start Mirror##
1. ssh in and `export DISPLAY=:0.0`
2. start FRIDAY-Mirror.py
3. open browser to http://localhost:8000/web/main.html

