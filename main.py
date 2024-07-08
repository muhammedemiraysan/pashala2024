import select
import sys
import time
from machine import Pin
# Set up the poll object
led = Pin(25, Pin.OUT)
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)
# Loop indefinitely
while True:
    # Wait for input on stdin
    poll_results = poll_obj.poll(1) # the '1' is how long it will wait for message before looping again (in microseconds)
    if poll_results:
        # Read the data from stdin (read data coming from PC)
        data = sys.stdin.readline().strip()
        # Write the data to the input file
        if data == "1":
            led.on()
            print("ledon")
        if data == "0":
            led.off()
            print("ledoff")
    else:
        # do something if no message received (like feed a watchdog timer)
        continue
