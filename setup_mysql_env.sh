#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Update package lists
echo "##########################################"
echo "######### Updating package lists #########"
echo "##########################################"
apt-get update -y


# Install required dependencies
echo "####################################################"
echo "######### Installing required dependencies #########"
echo "####################################################"
apt-get install -y pkg-config wget lsb-release ca-certificates gnupg

# Download and install MySQL APT repository configuration
echo "#################################################################"
echo "######### Installing MySQL APT repository configuration #########"
echo "#################################################################"
wget -q https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
export DEBIAN_FRONTEND=noninteractive
dpkg -i mysql-apt-config_0.8.29-1_all.deb

# Update package lists again after adding MySQL repository
echo "#################################################################"
echo "######### Installing MySQL APT repository configuration #########"
echo "#################################################################"
apt-get update -y

# Install MySQL development libraries and required build tools
echo "###################################################################################"
echo "######### Installing MySQL development libraries and required build tools #########"
echo "###################################################################################"
apt-get install -y libmysqlclient-dev 
apt-get install -y python3-dev default-libmysqlclient-dev build-essential


# Install GUI packages
echo "###########################################"
echo "######### Installing GUI packages #########"
echo "###########################################"
apt-get -y install python3-tk
apt-get -y install python3-pyqt5

# Cleanup
echo "###############################"
echo "######### Cleaning up #########"
echo "###############################"
rm -f mysql-apt-config_0.8.29-1_all.deb

echo "#######################################################"
echo "######### Installation completed successfully #########"
echo "#######################################################"