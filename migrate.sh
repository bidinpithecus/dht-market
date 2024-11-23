#!/bin/bash

print_usage() {
  echo "Usage: $0 --ip <ip> --remote-port <remote-port> --port <port>"
  exit 1
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --ip) IP="$2"; shift ;;
    --remote-port) REMOTE_PORT="$2"; shift ;;
    --port) PORT="$2"; shift ;;
    *) echo "Unknown parameter: $1"; print_usage ;;
  esac
  shift
done

# Wrong parameters
if [ -z "$IP" ] || [ -z "$REMOTE_PORT" ] || [ -z "$PORT" ]; then
  print_usage
  exit 1
fi

# Step 1: Generate cpfs if not already generated
if [ ! -f db/cpfs.txt ]; then
  if [ ! -f src/generate_cpfs.py ]; then
    echo "Error: Missing script 'src/generate_cpfs.py'. Exiting."
    exit 1
  fi
  python3 src/generate_cpfs.py
fi

# Step 2: Load environment variables
if [ -f .env ]; then
  source .env
else
  echo "Error: '.env' file not found. Exiting."
  exit 1
fi

# Step 3: Split cpfs into chunks if not already split
should_split=false
for i in $(seq 1 "$LOJAS"); do
  if [ ! -f db/chunk$i.txt ]; then
    should_split=true
    break
  fi
done

if $should_split; then
  if [ ! -f src/split_in_chunks.py ]; then
    echo "Error: Missing script 'src/split_in_chunks.py'. Exiting."
    exit 1
  fi
  python3 src/split_in_chunks.py
fi

# Step 4: Run migration if server is running
if lsof -n -i:"$REMOTE_PORT" | tr '\n' ' ' | awk '{print $10 " " $18}' | grep -q "python3 \*:$REMOTE_PORT"; then
  if [ ! -f src/populate_dht.py ]; then
    echo "Error: Missing script 'src/populate_dht.py'. Exiting."
    exit 1
  fi
  python3 src/populate_dht.py --ip "$IP" --remote-port "$REMOTE_PORT" --port "$PORT"
else
  echo "Server is not running on port $REMOTE_PORT. Migration skipped."
fi
