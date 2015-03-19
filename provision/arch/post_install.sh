#!/bin/bash

set -e  # Abort on first error

function usage()
{
cat <<-ENDOFMESSAGE

$0 [OPTIONS]

options:

    -m Model.
    -h Display this message.

ENDOFMESSAGE
exit 1
}

UNMUTE_CMD="amixer sset Master unmute"

while getopts "hm:" opt; do
  case $opt in
    m)
      echo "Running model $OPTARG" >&2
      if [ "$OPTARG" = "x1" ]; then
        echo "systemctl enable dhcpcd.service"
        echo "systemctl start dhcpcd.service"
        # UNMUTE_CMD="amixer -c1 sset Master unmute"
      fi
      ;;
    h)
      usage
      ;;
    \?)
      usage
      ;;
  esac
done


pacman -S gnome sudo xorg-server xorg-server-utils xorg-xinit mesa openssh wget alsa-utils ttf-dejavu file-roller xf86-input-synaptics xf86-video-intel
useradd -m -g users -G lp,wheel,network,video,audio,storage -s /bin/bash pablo
$UNMUTE_CMD
systemctl enable gdm.service
systemctl enable NetworkManager.service
systemctl enable sshd.service
