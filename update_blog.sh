#!/bin/bash
#MASTER="stanko"
#WEB_NAME="stanko"
#PIC_NUMBER=9
#PIC_PATH="img"
#USER_NAME="stankobenes"
MASTER=$1
WEB_NAME=$2

python BlogGenerator $MASTER $WEB_NAME

if [ $# == 5 ]; then
    PIC_NUMBER=$3
    PIC_PATH=$4
    USER_NAME=$5

    python FlickrBanner $PIC_NUMBER $PIC_PATH $USER_NAME
    for ((i=0; i<$PIC_NUMBER; i++))
    do
    	convert -geometry 200x200 $PIC_PATH/pic$i.jpg -background white -flatten -transparent white -thumbnail x200 -resize '200x<' -resize 50% -gravity center -crop 100x100+0+0 +repage $PIC_PATH/pic$i.jpg 
    done

    montage $PIC_PATH/pic[0-$PIC_NUMBER-1].jpg -tile x1 -geometry +5+5 $PIC_PATH/banner.jpg
fi
