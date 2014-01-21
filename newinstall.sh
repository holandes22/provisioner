DISTRO=$1
WORK=$2
python=/usr/bin/python2.7
sudo $python provision/install.py $DISTRO
$python create_symlinks.py $WORK
