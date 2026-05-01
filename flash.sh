#!/bin/bash
# Uploads all src/*.py files to the Pico in one go.
# Usage: ./flash.sh
#
# Requirements: pip3 install mpremote
# Close Thonny before running — it holds the serial port.

set -e

echo "Flashing files to Pico..."

for f in src/*.py; do
    # Skip secrets_example.py — only real secrets.py should go on the device
    [[ "$(basename $f)" == "secrets_example.py" ]] && continue

    echo "  → $(basename $f)"
    mpremote fs cp "$f" ":$(basename $f)"
done

echo "Done. Rebooting Pico..."
mpremote reset
