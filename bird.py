from tkinter import *
import math as m
import random

boids = []
SCREEN_SIZE = 700
NUM_BOIDS = 50
BOID_SIZE = 5
MAX_SPEED = 10

for i in range(100):
    boids.append({
        'x': random.random() * SCREEN_SIZE,
        'y': random.random() * SCREEN_SIZE,
        'vx': 0,
        'vy': 0,
    })


win = Tk()
cv = Canvas(win, width = SCREEN_SIZE, height = SCREEN_SIZE, bg="black")
cv.pack()


def draw():
    cv.delete('all')
    for i in range(len(boids)):
        cv.create_rectangle(
            boids[i]['x'] - BOID_SIZE/2,
            boids[i]['y'] - BOID_SIZE/2,
            boids[i]['x'] + BOID_SIZE/2,
            boids[i]['y'] + BOID_SIZE/2,
            fill='white')

def move():
    for i in range(len(boids)):
        rule1(i)
        rule2(i)
        rule3(i)

        b = boids[i]
        speed = m.sqrt(b['vx']**2 + b['vy']**2)
        if speed >= MAX_SPEED:
            r = MAX_SPEED / speed
            b['vx'] *= r
            b['vy'] *= r

        if (b['x'] < 0 and b['vx'] < 0) or (b['x'] > SCREEN_SIZE and b['vx'] > 0):
            b['vx'] *= -1
        if (b['y'] < 0 and b['vy'] < 0) or (b['y'] > SCREEN_SIZE and b['vy'] > 0):
            b['vy'] *= -1

        b['x'] += b['vx']
        b['y'] += b['vy']



def rule1(index):
    c = {'x':0, 'y':0}
    for i in range(len(boids)):
        if i != index:
            c['x'] += boids[i]['x']
            c['y'] += boids[i]['y']

    c['x'] /= len(boids) - 1
    c['y'] /= len(boids) - 1
    boids[index]['vx'] += (c['x']-boids[index]['x']) / 100
    boids[index]['vy'] += (c['y']-boids[index]['y']) / 100


def rule2(index):
    for i in range(len(boids)):
        if i != index:
            d = getDistance(boids[i], boids[index])
            if d < 5:
                boids[index]['vx'] -= boids[i]['x'] - boids[index]['x']
                boids[index]['vy'] -= boids[i]['y'] - boids[index]['y']

def rule3(index):
    pv = {'x':0, 'y':0}
    for i in range(len(boids)):
        if i != index:
            pv['x'] += boids[i]['vx']
            pv['y'] += boids[i]['vy']

    pv['x'] /= len(boids) - 1
    pv['y'] /= len(boids) - 1
    boids[index]['vx'] += (pv['x']-boids[index]['vx']) / 16
    boids[index]['vy'] += (pv['y']-boids[index]['vy']) / 16

def getDistance(b1, b2):
    x = b1['x'] - b2['x']
    y = b1['y'] - b2['y']
    return m.sqrt(x**2 + y**2)


def game_loop():
    draw()
    move()
    win.after(10, game_loop)

game_loop()
win.mainloop()
