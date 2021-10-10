#!/bin/bash
NPWD=$(
    cd "$(dirname "$0")"
    pwd
)
export NPWD
# env
title='title name'
description='desc text'
playlist='playlist'
tags='tag1,tag2'
videos_file='xxxx.mp4'

init(){
    # dailymotion
    pip3 install --upgrade dailymotion
    # tumblr
    pip3 install --upgrade pytumblr
    # youtube
    pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client
    cd $NPWD/youtube
    git clone https://github.com/tokland/youtube-upload.git
    cp upload.py youtube-upload/youtube_upload/main.py

}

dailymotion_upload(){
    # dailymotion
    cd dailymotion
    python3 dm.py -c $NPWD/config.ini -f $videos_file -t "$title" --tags "$tags" --debug --channel lifestyle
    cd $NPWD
}
youtube_upload(){
    # youtube
    cd youtube/youtube-upload
    PYTHONPATH=. python3 bin/youtube-upload -t "$title" -d "$description" --privacy=private --playlist="$playlist"  --embeddable=False --client-secrets="$NPWD/youtube/acerjui-daily-note.json" --credentials-file="$NPWD/youtube/acerjui-daily-note-cred.json" --playlist-sh="$NPWD/youtube/acerjui-daily-note-playlist.sh" --debug "$videos_file" --tags "$tags"
    cd $NPWD
}

tumblr_upload(){
    # tumblr
    cd tumblr
    # python3 tm.py -t "$title" --post-body 'test body text' --tags "$tags" --state private -c config.ini -f $videos_file
    python3 tm.py -t "$title" --tags "$tags" --state private -c $NPWD/config.ini -f $videos_file
    cd $NPWD
}

set -x -e

case $1 in 
    init)
        init
    ;;
    dm)
        dailymotion_upload
    ;;
    tm)
        tumblr_upload
    ;;
    yt)
        youtube_upload
    ;;
    all)
        dailymotion_upload
        tumblr_upload
        youtube_upload
    ;;
    *)
        echo 'init/dm/tm/yt/all'
    ;;
esac
