"""
EAVirtualInternship Task 1!
Vaxman!
All code modifications are between multiple #'s
All Credit to github:Hbokmann for the pacman source code, github repo 1 from the Python Task Page on Forage

Thank you for taking the time to check my project
Hope you have a great day!

Cheers! :)

PS. To make the game a bit more challenging, I'll be making a few more changes in addition to the base requirements already met

EDIT 1: Base Requirements all met!
"""

from random import choice
from random import randint
from turtle import *
from timeit import default_timer as timer
from threading import Timer
from time import sleep

from freegames import floor, vector

#################################################################################################################
#Currently not in use in this version, I'll be iterating over this to add a challenge to the game since it's a bit too easy right now
Challenge = False
#################################################################################################################
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
#################################################################################################################
#Timers, 4 originally, directly proportionate to the number of enemies in game, to allow for ease of access when deleting them
ghost_timers = [0,0,0,0]
#################################################################################################################
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')



################################################################################################################# ------------------------------> OMIT SECTION
#The Double function checks the time of each monster at each point compared to the current time, and once it hits the 30 second mark,
#Calls the doubler function, which instantiates the number of enemies currently present, basically doubling
#The emtpy list j acts like a bool value to prevent the function from running more than once in a second
#The doubler function only runs if j is empty, and a number is appended in j as soon as we enter doubler, thereby preventing it
#from running multiple times a second
# j = []

# def doubler():
#     for i in range(len(ghosts)):
#         print(i)
#         ghosts.append([vector(-180, 160), vector(randint(5, 15), 0)])
#         ghost_timers.append(0)
#     j.append(0)
#
#
# def cdouble():
#     ghosts.append([vector(-180, 160), vector(randint(5, 15), 0)])

def double():
    pass
    # j1 = timer()
    # if len(ghosts) <= 32:
    #     for i in range(len(ghost_timers)):
    #         if int(j1 - ghost_timers[i]) % 5 == 0 and len(j) == 0:
    #             ghosts.append([vector(-180, 160), vector(randint(5, 15), 0)])
    #             ghost_timers.append(0)
                # if Challenge:
                #     print(len(ghosts))
                #     doubler()
                #     print(len(ghosts))
            # if int(timer() - ghost_timers[i])&1 == 1:
            #     j.clear()

        # print("Ghost " + str(i) + " " + str(timer() - ghost_timers[i]))
    # ghosts.append([vector(-180, 160), vector(randint(5,15), 0)])

#################################################################################################################
def move():
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()
#################################################################################################################
#Code for vaxman destroying the ghosts, basically pops out the respective ghost and timer
#This is why the ghost timer and ghost are kept proportionate to each other
    for i in ghosts:
        for point in i:
            if abs(pacman - point) < 20:
                print(ghosts.index(i))
                ghost_timers.pop(ghosts.index(i))
                ghosts.remove(i)



    ontimer(move, 100)
    double()
#Timer appended to ghost timer every 30 seconds for the alive enemies, and we append a ghost for every living enemy, hence doubling it
#They currently all spawn at one place, but I'll change this very soon and make them replicate next to the respective ghost
#Relatively easy to code, but I'm modifying the game since I'm having too much fun with this
    for i in range(len(ghost_timers)):
        print("Ghost "+str(i)+" "+str(timer() - ghost_timers[i]))
        if timer() - ghost_timers[i] >= 30:
            ghosts.append([vector(-180, 160), vector(randint(5, 15), 0)])
            ghost_timers[i] = timer()
            ghost_timers.append(timer())


#################################################################################################################
#If the number of ghosts reaches 4 times the original value, the application will simply close
    if len(ghosts) >= 128:
        quit()
#################################################################################################################

def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()