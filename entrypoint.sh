#!/bin/sh

ENTRY=bot/main.py

if [ "$ENV" == "DEV" ]; then
    python $ENTRY &
    inotifywait -mrq -e modify -e create -e delete --include '.*\.py$' bot/ |
    while read -r path event file; do
        echo "Detected file changes: $path/$file. Restarting...";
        pkill python;
        sleep 2;
        python $ENTRY &
    done
else
    python $ENTRY
fi
