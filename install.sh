# Thankfully, Google provided clear and simple instructions for installing the grpc
# tool chain, so only a beautifully short installation script is necessary.

#####################################################
# Install dependencies
#####################################################

sudo apt-get update
sudo apt-get install build-essential autoconf libtool
sudo apt-get install python-all-dev python-virtualenv

#####################################################
# Install python libraries
#####################################################
sudo pip install protobuf==3.0.0b2
sudo pip install grpcio
sudo pip install requests

#####################################################
# Compilations from source
# We perform all compilations in a tmp dir
#####################################################

mkdir /tmp/cs262install
pushd /tmp/cs262install

#####################################################
# Install protoc 3.0.0
#####################################################

# Note that the cs50 appliance is 32 bits. Change to 64 bit in obvious fashion
if [ "$(protoc --version)" != "libprotoc 3.0.0" ]
then
  wget https://github.com/google/protobuf/releases/download/v3.0.0-beta-2/protoc-3.0.0-beta-2-linux-x86_32.zip
  unzip protoc-3.0.0-beta-2-linux-x86_32.zip
  sudo mv ./protoc /usr/bin/protoc
fi

#####################################################
# Install grpc
#####################################################

git clone https://github.com/grpc/grpc.git
pushd grpc # pwd = /tmp/cs262install/grpc
git submodule update --init

# Install protobuf (this needs to be a separate step...)
pushd third_party/protobuf
./autogen.sh
./configure
make && sudo make install
popd

# Finally build the rest of the system
sudo make && sudo make install

popd # pwd = /tmp/cs262install
popd # pwd initial directory

rm -rf /tmp/cs262install

# Finally, for some odd reason (on my cs50 appliance), this directory is r/w/x only by root
# so make it read-writeable
sudo chmod -R ugo+rX /usr/local/lib/python2.7/dist-packages/
