WORK=$1
sudo python provision/install.py
python create_symlinks.py $WORK
