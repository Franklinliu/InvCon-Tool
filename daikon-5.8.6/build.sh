#!/bin/bash
export DAIKONDIR=$(pwd)
# make -C $DAIKONDIR clean-everything
source $DAIKONDIR/scripts/daikon.bashrc
make -C $DAIKONDIR rebuild-everything
