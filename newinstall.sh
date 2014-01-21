WORK=$1
DISTRO=$2
ACTIONS=$3
python=/usr/bin/python2.7
sudo $python provision/install.py $DISTRO $ACTIONS
$python create_symlinks.py $WORK
