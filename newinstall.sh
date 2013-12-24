WORK=$1
python=python2.7
sudo $python provision/install.py
$python create_symlinks.py $WORK
