import picar_4wd as fc
import sys
import tty
import termios
import math
import asyncio
import time
from picar_4wd.servo import Servo
from picar_4wd.pwm import PWM
from picar_4wd.pin import Pin
from picar_4wd.ultrasonic import Ultrasonic
import numpy as np
import matplotlib.pyplot as plt
import time as sleep

power_val = 50
key = 'status'
print("If you want to quit.Please press q")
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def get_distance_at(angle):
    servo = Servo(PWM("P0"), offset=10)
    servo.set_angle(angle)
    time.sleep(0.04)
    us = Ultrasonic(Pin('D8'), Pin('D9'))
    distance = us.get_distance()
    angle_distance = [angle, distance]
    return distance
a=get_distance_at(0)
print(a)

map1 = np.zeros((100,100))
for angle in range(-90,90,1):
    distance = get_distance_at(angle)
    print('dis',distance)
    x =round(math.cos((angle+90)*math.pi/180)*distance)
    y =round(math.sin((angle+90)*math.pi/180)*distance)
    time.sleep(0.05)
    if -50 <=x and x<=50 and y<=100 and y>0:
        map1[x+50][y] = 1
        plt.plot(x,y,'*')
        print('x',x,'y',y)
    
map2=np.rot90(map1)
print(map2)

# 
plt.xlim([-50,50])
plt.ylim([0,100])
plt.savefig("squares.png")
np.savetxt('text.txt', map1, fmt='%s')
np.savetxt('text.txt', map2, fmt='%s')
plt.show()
# def Keyborad_control():
#     while True:
#         global power_val
#         key=readkey()
#         if key == 'w':
#             fc.forward(power_val)
#             angel_d = get_distance_at(30)
#             print(angel_d)
            # if int(distant1.get_distance()) <=100:
            #     fc.stop()

        # if key=='6':
        #     if power_val <=90:
        #         power_val += 10
        #         print("power_val:",power_val)
        # elif key=='4':
        #     if power_val >=10:
        #         power_val -= 10
        #         print("power_val:",power_val)
        # if key=='w':
        #     fc.forward(power_val)
        # elif key=='a':
        #     fc.turn_left(power_val)
        # elif key=='s':
        #     fc.backward(power_val)
        # elif key=='d':
        #     fc.turn_right(power_val)
        # else:
        #     fc.stop()
        # if key=='q':
        #     print("quit")
        #     break
# if __name__ == '__main__':
#     Keyborad_control()