sudo apt-get install python3-matplotlib python3-numpy
sudo apt-get install python3-pip

# install pygame for python3 (see http://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3)
cd ~/Downloads/
sudo apt-get install mercurial
hg clone https://bitbucket.org/pygame/pygame
cd pygame
sudo apt-get install python3-dev python3-numpy libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev
python3 setup.py build
sudo apt-get remove mercurial

sudo apt-get install python3-scipy python3-jsonpickle python3-gmpy2 python3-pandas python3-PyQt4