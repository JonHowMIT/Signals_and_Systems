#################################################
# PURPOSE: Draw a spinning wheel
import turtle
import numpy as np
import time
#################################################

# CONFIGURATION
N = 8
T = 10/360  # basic speed
f = N/T
size = 30

fs = f # sample at same rate
f_alias = f - fs*np.round(f/fs,0)
speed = f_alias

fs = 0.99*f # sample slightly slower
f_alias = f - fs*np.round(f/fs,0)
speed0 = f_alias

fs = 1.01*f # sample slightly faster
f_alias1 = f - fs*np.round(f/fs,0)
speed1 = f_alias1

# Configure the drawing tools
spoke1 = turtle.Turtle()
spoke2 = turtle.Turtle()
spoke3 = turtle.Turtle()
spoke4 = turtle.Turtle()
spokes = [spoke1,spoke2,spoke3,spoke4]

_ = 0
for spoke in spokes:
 spoke.speed(0)
 spoke.shape('square')
 spoke.shapesize(stretch_wid=size,stretch_len=1)
 spoke.left(45*_)
 _ += 1

# MAIN PROGRAM
# Configure for drawing the rim
rim = turtle.Pen()
rim.width(20)
rim.speed(0)
rim.up()
rim.forward(size*10)
rim.down()
rim.left(90)

# Rim drawing

rim.circle(size*10)

# Spinning wheel
t0 = time.time()
while (time.time() - t0 < 5):
    for spoke in spokes:
        spoke.left(speed)

t0 = time.time()
while (time.time() - t0 < 10):
    for spoke in spokes:
        spoke.left(speed0)

t0 = time.time()
# Spinning wheel
while (time.time() - t0 < 10):
    for spoke in spokes:
        spoke.left(speed1)

#turtle.exitonclick()