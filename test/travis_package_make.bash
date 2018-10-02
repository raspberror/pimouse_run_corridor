#!/bin/bash -xve

#sync and make
rsync -av ./ ~/catkin_ws/src/pimouse_run_corridor/

cd ~/catkin_ws/src
git clone --depth=1 https://github.com/raspberror/pimouse_ros.git

cd ~/catkin_ws
catkin_make

# Copyright 2016 Ryuichi Ueda
# Released under the BSD License.
# To make line numbers be identical with the book, this statement is written here. Don't move it to the header.
