#!/usr/bin/env bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

# build docker container
if [[ $(pgrep dockerd) ]]; then
    cd docker
    docker build --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --build-arg HTTP_PROXY=${http_proxy} --build-arg HTTPS_PROXY=${https_proxy} -t fact/firmware-qemu-exec:latest .
    cd ..
else
    echo "Error: docker daemon not running! Could not build docker image"
    exit 1
fi

# get files for testing dynamically linked binary
if [[ ! -e test/data/test_tmp_dir/lib/libc.so.6 ]]; then
    mkdir tmp
    cd tmp
    wget http://de.archive.ubuntu.com/ubuntu/pool/universe/c/cross-toolchain-base-ports/libc6-mips-cross_2.23-0ubuntu3cross1_all.deb
    ar x libc6-mips-cross_2.23-0ubuntu3cross1_all.deb
    tar xvf data.tar.xz
    mkdir ../test/data/test_tmp_dir/lib
    mkdir ../test/data/test_tmp_dir_2/fact_extracted/lib
    cp usr/mips-linux-gnu/lib/libc-2.23.so ../test/data/test_tmp_dir/lib/libc.so.6
    cp usr/mips-linux-gnu/lib/ld-2.23.so ../test/data/test_tmp_dir/lib/ld.so.1
    mv usr/mips-linux-gnu/lib/libc-2.23.so ../test/data/test_tmp_dir_2/fact_extracted/lib/libc.so.6
    mv usr/mips-linux-gnu/lib/ld-2.23.so ../test/data/test_tmp_dir_2/fact_extracted/lib/ld.so.1
    cd ..
    rm -r tmp
else
    echo "skipping download of test files (already found)"
fi

exit 0
