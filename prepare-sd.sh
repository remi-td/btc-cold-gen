#!/bin/bash

set -e  # Exit on error

# Constants
SCRIPT_NAME="bitcoin_wallet.py"
SERVICE_NAME="bitcoin_wallet"
DEPENDENCIES="python3 python3-pip"

# Functions
mount_partitions() {
    # Detect and mount partitions
    echo "Detecting SD card partitions..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        BOOT_PART=$(lsblk -lp | grep "part /boot" | awk '{print $1}')
        ROOT_PART=$(lsblk -lp | grep "part /$" | awk '{print $1}')
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        BOOT_PART=$(diskutil list | grep EFI | awk '{print $6}')
        ROOT_PART=$(diskutil list | grep Apple | awk '{print $6}')
    else
        echo "Unsupported OS: $OSTYPE"
        exit 1
    fi

    if [ -z "$BOOT_PART" ] || [ -z "$ROOT_PART" ]; then
        echo "Error: Could not detect partitions."
        exit 1
    fi

    echo "Mounting boot partition ($BOOT_PART)..."
    mkdir -p /mnt/boot
    sudo mount "$BOOT_PART" /mnt/boot

    echo "Mounting root partition ($ROOT_PART)..."
    mkdir -p /mnt/root
    sudo mount "$ROOT_PART" /mnt/root
}

install_dependencies() {
    echo "Installing system dependencies..."
    sudo chroot /mnt/root apt update
    sudo chroot /mnt/root apt install -y $DEPENDENCIES
    sudo chroot /mnt/root pip3 install -r requirements.txt
}

add_script() {
    echo "Copying Python script to SD card..."
    sudo cp "$SCRIPT_NAME" /mnt/root/home/pi/
    sudo chmod +x /mnt/root/home/pi/"$SCRIPT_NAME"
}

configure_autostart() {
    echo "Configuring script to run on boot..."
    sudo bash -c "cat > /mnt/root/etc/systemd/system/$SERVICE_NAME.service <<EOF
[Unit]
Description=Bitcoin Wallet Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/$SCRIPT_NAME
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF"

    sudo chroot /mnt/root systemctl enable "$SERVICE_NAME"
}

cleanup() {
    echo "Unmounting partitions..."
    sudo umount /mnt/boot
    sudo umount /mnt/root
    rm -rf /mnt/boot /mnt/root
    echo "Done!"
}

# Main script
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 /path/to/SD/card"
    exit 1
fi

SD_CARD=$1
if [ ! -e "$SD_CARD" ]; then
    echo "Error: SD card device $SD_CARD not found."
    exit 1
fi

echo "Preparing SD card at $SD_CARD..."
mount_partitions
install_dependencies
add_script
configure_autostart
cleanup

echo "SD card preparation complete. Ready to boot!"