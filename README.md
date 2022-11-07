# CVA6 H-Extension Guide
This guide provides a fully step by step tutorial on how to run a one core CVA6 based system with H-extension in a Genesys2 FPGA.
# Table of Contents
- [CVA6 H-Extension Guide](#cva6-h-extension-guide)
- [Table of Contents](#table-of-contents)
- [0) Prologue](#0-prologue)
- [1) Software](#1-software)
  - [1.1) Bare-Metal Application](#11-bare-metal-application)
  - [1.2) CVA6 SDK Linux](#12-cva6-sdk-linux)
  - [1.3) Bao](#13-bao)
  - [1.4) OpenSBI](#14-opensbi)
- [2) Openpiton](#2-openpiton)
  - [2.1) Generate Bitstream Openpiton](#21-generate-bitstream-openpiton)
  - [2.2) Booting on Genesys2](#22-booting-on-genesys2)
  - [Used tool versions](#used-tool-versions)

# 0) Prologue

First setup ARCH and your RISC-V toolchain prefix:

`export ARCH=riscv`\
`export CROSS_COMPILE=toolchain-prefix-`\
`export RISCV=path/to/riscv-tools`

For all software use *riscv64-unknown-elf-* gcc 10.1.0 2020.08.2, from [toolchain](https://static.dev.sifive.com/dev-tools/freedom-tools/v2020.08/riscv64-unknown-elf-gcc-10.1.0-2020.08.2-x86_64-linux-ubuntu14.tar.gz).

Specifically for building opensbi, I had to use a different toolchain riscv64-unknown-linux-gnu-, which I downloaded from [linux toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain/releases/tag/2021.08.11).

Next, install the [RISC-V Tools](https://github.com/riscv/riscv-tools) and make sure the `RISCV` environment variable points to where your RISC-V installation is located.

Repeat these every time you start a new terminal.

Start each step from the top-level directory.

For every path starting with */path/to/* substitute it by the corresponding absolute path in your machine.

Finally, initialize the repo and all the submodules by running:

`git submodule update --init`

# 1) Software

## 1.1) Bare-Metal Application

To build the bare-metal guest for the cva6:

`cd bao-baremetal-guest`\
`make CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=openpiton`

## 1.2) CVA6 SDK Linux

To build linux using the **cva6 sdk** run:

`cd cva6-sdk`\
`git submodule update --init --recursive`
`make uImage`

> **_:notebook: Note:_** The following steps shall be done using the *riscv64-unknown-elf-* toolchain.

Next, build the cva6 device tree:

`cd ../linux`\
`dtc cva6-openpiton-bao-minimal.dts > cva6-openpiton-bao-minimal.dtb`\
`dtc cva6-openpiton-bao-full.dts > cva6-openpiton-bao-full.dtb`\
`dtc cva6-openpiton-full.dts > cva6-openpiton-full.dtb`

And build the final image by concatening the minimal bootloader, linux and device tree binaries:

`cd lloader`

Run the following commands to build the system for single-core linux:

`make CROSS_COMPILE=riscv64-unknown-elf- ARCH=rv64 IMAGE=../../cva6-sdk/install64/Image DTB=../cva6-openpiton-bao-minimal.dtb TARGET=linux-rv64-openpiton`

Run the following commands to build the system for dual-core linux:

`make CROSS_COMPILE=riscv64-unknown-elf- ARCH=rv64 IMAGE=../../cva6-sdk/install64/Image DTB=../cva6-openpiton-bao-full.dtb TARGET=linux-rv64-openpiton`

## 1.3) Bao

> **_:notebook: Note:_** The following steps shall be done using the *riscv64-unknown-elf-* toolchain and as so, the toolchain should be on the *PATH*.
> 
To build **bao** for cva6:

`cd bao-hypervisor`

Copy the provided configs to bao's directory:

`cp -r ../bao/configs/* ./configs`

In the configs you want to use, in the *configs/xxxconfig/config.c* files, setup the absolute path for the
vm images. For example:

For the **openpiton-baremetal** config:

**VM_IMAGE(baremetal_image, path/to/bao-baremetal-guest/build/openpiton/baremetal.bin);**

or

For the **openpiton-linux** config:

**VM_IMAGE(linux_image, /path/to/linux/lloader/linux-rv64-openpiton-zcu.bin);**

Next there is a example on how to compile bao with linux and/or baremetal config for openpiton:

`make CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=openpiton CONFIG=openpiton-linux CONFIG_BUILTIN=y`

or

`make CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=openpiton CONFIG=openpiton-baremetal CONFIG_BUILTIN=y`

For dual-core configuration running just Linux or Linux and a baremetal applications run the following commands:

`make CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=openpiton-dual CONFIG=openpiton-linux-dual CONFIG_BUILTIN=y`

or

`make CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=openpiton-dual CONFIG=openpiton-linux-baremetal CONFIG_BUILTIN=y`


## 1.4) OpenSBI
> **_:notebook: Note:_** The following steps shall be executed using the *riscv64-linux-* toolchain.

First, cd into the **opensbi** folder:

`cd opensbi`

Next, to compile **opensbi** with the **bao** and **baremetal application** or **linux** for the chosen target platform, just run the following command according to your target application:

Examples:

To build **opensbi**with **bao** and **baremetal application** for fpga run:

`make CROSS_COMPILE=riscv64-unknown-linux-gnu- PLATFORM=fpga/openpiton FW_PAYLOAD=y FW_PAYLOAD_PATH=../bao-hypervisor/bin/openpiton/builtin-configs/openpiton-baremetal/bao.bin`

To build **opensbi** with **bao** and **linux** for fpga run:

`make CROSS_COMPILE=riscv64-unknown-linux-gnu- PLATFORM=fpga/openpiton FW_PAYLOAD=y FW_PAYLOAD_PATH=../bao-hypervisor/bin/openpiton/builtin-configs/openpiton-linux/bao.bin`

To build **opensbi** with just **linux** with one core configuration run:

`make CROSS_COMPILE=riscv64-unknown-linux-gnu- PLATFORM=fpga/openpiton FW_PAYLOAD=y FW_PAYLOAD_PATH=../cva6-sdk/install64/Image`

To build **opensbi** with just **linux** with dual core configuration run:

`make CROSS_COMPILE=riscv64-unknown-linux-gnu- PLATFORM=fpga/openpiton FW_PAYLOAD=y FW_PAYLOAD_PATH=../cva6-sdk/install64/Image FW_FDT_PATH=../linux/cva6-openpiton-full.dtb`

> **_:notebook: Note:_** The command above builds a image for a dual core configuration, to run in a single core configuration some changes are required on the device tree.
# 2) Openpiton

First, setup openpiton as instructed in the submodule **openpiton/README**.
Next, just checkout to the hyp cva6 repo by running the following commands:

`cd openpiton/piton/design/chip/tile/ariane`\
`git remote add minho-pulp https://github.com/minho-pulp/cva6.git`\
`git checkout minho-pulp/wip/hyp`\
`git fetch minho-pulp wip/hyp`\
`git checkout minho-pulp/wip/hyp`\
`git submodule update --init --recursive`

## 2.1) Generate Bitstream Openpiton

The bitfile for a 1x1 tile cva6 configuration for the Genesys2 board can be built using the following command:

`protosyn -b genesys2 -d system --core=ariane --uart-dmw ddr`

For a 2x1 configuration run:

`protosyn -b genesys2 -d system --core=ariane --uart-dmw ddr --x_tiles=2`

## 2.2) Booting on Genesys2

To prepare the SD card with a Opensbi image you need to format it with
[`sgdisk`](https://wiki.archlinux.org/index.php/GPT_fdisk)
then write the image with
[`dd`](https://wiki.archlinux.org/index.php/Dd).
1. `$ sudo fdisk -l`
    Search *carefully* for the corresponding disk label of the SD card,
    e.g. `/dev/sda`
2. `$ sudo sgdisk --clear --new=1:2048:67583 --new=2 --typecode=1:3000 --typecode=2:8300 /dev/sda`
    Create a new [GPT](https://en.wikipedia.org/wiki/GUID_Partition_Table)
    partition table and two partitions:
    1st partition 32MB (ONIE boot),
    2nd partition rest (Linux root).
3. `$ sudo dd if=/path/to/opensbi/build/platform/fpga/openpiton/fw_payload.bin of=/dev/sda1 oflag=sync bs=1M`
    Write the Opensbi payload `fw_payload.bin` file to the first partition.
    E.g. where your disk label is `/dev/sda` use `/dev/sda1` (append a `1`).
4. Insert the SD card into the FPGA development board.
5. Connect a mini-USB cable to the port labelled `UART` and power on the board
   which allows the interfaces such as `/dev/ttyUSB0` to become available.
6. Open a console with
   115200/8N1.
   E.g. something like
   `screen /dev/ttyUSB0 115200`
   or
   `sudo minicom -D /dev/ttyUSB2`
   If there are multiple ttyUSB devices just open a console to each of them.
7. Connect a micro-USB cable to the port labelled `JTAG` and connect from within
   the Vivado Hardware Manager.
8. Program the device with the generated bitfile, which Vivado should find
   automatically.
   Once programming is finished (around 10s) reset will be immediately lifted
   and you should see the Application boot process being reported on the UART console.

## Used tool versions

- riscv64-unknown-elf-gcc version 10.1.0 (SiFive GCC 8.3.0-2020.08.2)
- riscv64-unknown-linux-gnu-gcc version 11.1.0
- Vivado 2018.2
- dtc 1.5.0
