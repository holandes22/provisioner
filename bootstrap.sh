#!/bin/sh

# Give an SSH dir path where the RSA keys are stored
# For example: sh bootstrap.sh ssh --work
set -e
SRC_SSH_DIR=$1
TGT_SSH_DIR=$HOME/.ssh
WORK=$2

mkdir $TGT_SSH_DIR
cp -r $SRC_SSH_DIR/* $TGT_SSH_DIR
chmod 400 $TGT_SSH_DIR/*

if [ -e "/etc/arch-release" ]; then
    sudo pacman -Sy --noconfirm git python2-yaml openssh
elif [ -e "/etc/redhat-release" ]; then
    echo "No need to install deps"
else
    sudo add-apt-repository --yes ppa:git-core/ppa
    sudo apt-get update
    sudo apt-get install --yes git python-yaml
fi

cd $HOME
git clone git@github.com:holandes22/provisioner
cd $HOME/provisioner
sh newinstall.sh $WORK
