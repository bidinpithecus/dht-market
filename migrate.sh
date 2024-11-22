#!/bin/bash

if [ "$#" -lt 6 ]; then
  echo "Usage: $0 --ip <ip> --remote-port <remote-port> --port <port>"
  exit 1
fi

if ! [ -e db/cpfs.txt ]; then
  python3 src/generate_cpfs.py
fi

python3 src/split_in_chunks.py

lsof -n -i:$4 | tr '\n' ' ' | awk '{print $10 " " $18}' | grep "python3 \*:$4" && python3 src/populate_dht.py --ip "$2" --remote-port "$4" --port "$6"
