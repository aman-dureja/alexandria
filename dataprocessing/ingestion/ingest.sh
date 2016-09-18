#!/usr/bin/env bash

# MAKE SURE YOU HAVE EXECUTE PERMISSIONS

TOP_DIR=${1}
SECOND_DIR=${2}
FILE_NAME=${3}

cd ./raw

if [ ! -d "$TOP_DIR" ]; then
    mkdir $TOP_DIR
fi

cd $TOP_DIR

for i in {1..3}
do
    if [ ! -d "0" ]; then
        mkdir 0
    fi
    cd 0
done

if [ ! -d "$SECOND_DIR" ]; then
    mkdir $SECOND_DIR
fi

cd $SECOND_DIR

curl -s http://gutenberg.readingroo.ms/$TOP_DIR/0/0/0/$SECOND_DIR/$FILE_NAME >> $FILE_NAME
