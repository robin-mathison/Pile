#!/usr/bin/env sh

# get CPU temp
CPU_TEMP_RAW=$(cat /sys/class/thermal/thermal_zone0/temp)
CPU_TEMP=$(echo "scale=2; $CPU_TEMP_RAW/1000" | bc)

# allow two places after decimal point in math and pipe CPU temp to bc
echo "CPU temperature (C): $CPU_TEMP"

GPU_TEMP=$(vcgencmd measure_temp | cut -d "=" -f 2 | cut -d "'" -f 1)
echo "GPU temperature (C): $GPU_TEMP"
