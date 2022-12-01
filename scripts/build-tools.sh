#!/bin/bash
# Script to build tools required to run Bao on CVA6-based SoC.
# $1 - path to build tools
# Example:
# source ./build-tools.sh ./build
CURR_DIR=`pwd`
if [ "$1" -eq "" ];
then
    BUILD_ROOT_DIR=$(realpath -s ./build)
else
    BUILD_ROOT_DIR=$(realpath -s $1)
fi
LINUX_TOOLCHAIN=riscv64-glibc-ubuntu-20.04-nightly-2022.11.23-nightly
LINUX_TOOLCHAIN_DIR=$BUILD_ROOT_DIR/riscv
BARE_TOOLCHAIN=riscv64-unknown-elf-gcc-10.1.0-2020.08.2-x86_64-linux-ubuntu14
BARE_TOOLCHAIN_DIR=$BUILD_ROOT_DIR/$BARE_TOOLCHAIN
# Check if BUILD_ROOT_DIR already exists
if [ ! -e "$BUILD_ROOT_DIR" ];
then
    mkdir -p $BUILD_ROOT_DIR
fi

# Check if toolchain is already installed
if [ -e "$LINUX_TOOLCHAIN_DIR" ];
then
    echo "RISC-V toolchain already installed in $LINUX_TOOLCHAIN_DIR"
else
    echo "Installing RISC-V Linux toolchain in $LINUX_TOOLCHAIN_DIR"
    wget https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/2022.11.23/$LINUX_TOOLCHAIN.tar.gz $LINUX_TOOLCHAIN_DIR -O "${LINUX_TOOLCHAIN}.tar.gz"
    tar -xvf "${LINUX_TOOLCHAIN}.tar.gz" -C ${BUILD_ROOT_DIR}
fi

# Check if Bare toolchain is already installed
if [ -e "$BARE_TOOLCHAIN_DIR" ];
then
    echo "RISC-V toolchain already installed in $BARE_TOOLCHAIN_DIR"
else
    echo "Installing RISC-V Bare toolchain in $BARE_TOOLCHAIN_DIR"
    wget https://static.dev.sifive.com/dev-tools/freedom-tools/v2020.08/$BARE_TOOLCHAIN.tar.gz $BARE_TOOLCHAIN_DIR -O "${BARE_TOOLCHAIN}.tar.gz"
    tar -xvf "${BARE_TOOLCHAIN}.tar.gz" -C ${BUILD_ROOT_DIR}
fi

# Insert toolchain in path
echo "Adding RISC-V Bare and Linux toolchain to PATH"

export PATH=$PATH:$LINUX_TOOLCHAIN_DIR/bin
export PATH=$PATH:$BARE_TOOLCHAIN_DIR/bin