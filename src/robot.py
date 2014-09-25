import time
from sr import *

print "Hello, world!"

R = Robot()

# This is the configuration for Elizabeth.
# TODO: make this generic
BOARD_RIGHT = R.motors["SR0HL17"]
BOARD_LEFT = R.motors["SR0YK1C"]

WHEEL_FRONT_LEFT = BOARD_LEFT.m1 # positive is towards the front of the robot
WHEEL_FRONT_RIGHT = BOARD_RIGHT.m0 # positive is towards the front of the robot
WHEEL_BACK = BOARD_RIGHT.m1 # positive is to the right of the robot

# enable the brakes
WHEEL_FRONT_LEFT.use_brake = True
WHEEL_FRONT_RIGHT.use_brake = True
WHEEL_BACK.use_brake = True

WHEEL_FRONT_LEFT_CALIBRATION = -1
WHEEL_FRONT_RIGHT_CALIBRATION = -1
WHEEL_BACK_CALIBRATION = 1

def set_motors(front_left, front_right, back):
    WHEEL_FRONT_LEFT.power = int(front_left * WHEEL_FRONT_LEFT_CALIBRATION)
    WHEEL_FRONT_RIGHT.power = int(front_right * WHEEL_FRONT_RIGHT_CALIBRATION)
    WHEEL_BACK.power = int(back * WHEEL_BACK_CALIBRATION)

def forward(speed):
    set_motors(speed, speed, 0)

def reverse(speed):
    forward(-speed)

def stop():
    forward(0)

def rotate(speed):
    set_motors(speed, -speed, speed)

def can_see_block():
    ACCEPTABLE_MARKER_TYPES = (MARKER_TOKEN_TOP,
                               MARKER_TOKEN_BOTTOM,
                               MARKER_TOKEN_SIDE)
    markers = R.see()
    return any(marker.info.marker_type in ACCEPTABLE_MARKER_TYPES
                for marker in R.see())

## FIXME: debug while we don't have a marker
#search_count = 0
#def can_see_block():
#    global search_count
#    search_count += 1
#    return search_count % 5 == 0

def state_search():
    rotate(30)
    time.sleep(0.4)
    stop()
    time.sleep(0.8)
    return state_advance if can_see_block() else state_search

def state_advance():
    forward(30)
    time.sleep(1)
    stop()
    time.sleep(0.8)
    return state_advance if can_see_block() else state_backoff

def state_backoff():
    reverse(20)
    time.sleep(2)
    stop()
    rotate(-50)
    time.sleep(2)
    stop()
    return state_search

current_state = state_search
while True:
    current_state = current_state()

