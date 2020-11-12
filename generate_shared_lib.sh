#!/bin/bash

base_dir=$(dirname $(realpath $0))
cavc_dir=$base_dir/libcpp/CavalierContours
cavc_build_dir=$base_dir/libcpp/build
dst_dir=$base_dir/cavaliercontours/lib

mkdir -p $cavc_build_dir
cd $cavc_build_dir
cmake $cavc_dir
make -j$(nproc) CavalierContours
mkdir -p $dst_dir
cp libCavalierContours.so $dst_dir
echo "libCavalierContours.so generated into "$dst_dir
