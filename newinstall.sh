WORK=$1
python=/usr/bin/python2.7
sudo $python provision/install.py
$python create_symlinks.py $WORK
