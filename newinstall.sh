WORK=$1
python=python
if [ -e "/etc/arch-release" ]
then
    python=python2.7
fi
sudo $python provision/install.py
$python create_symlinks.py $WORK
