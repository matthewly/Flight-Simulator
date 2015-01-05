# CS418 MP2
# Author: Matthew Ly

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


polysize = 0.05 #resolution
sealevel = 0.0 #water level

pitch = 0.05 #pitching speed
roll = 0.05 #rolling speed
movespeed = 0.007 #moving speed

#up vector
up_x = 0.0 #x component
up_y = 1.0 #y component
up_z = 0.0 #z component

#eyepoint
eye_x = 0.40 #x component
eye_y = 0.05 #y component
eye_z = 0.30 #z component

#lookat point
lookat_x = 0.00 #x component
lookat_y = 0.00 #y component
lookat_z = 0.00 #z component

#draw mountains randomly
def mountain(x0, y0, z0, x1, y1, z1, x2, y2, z2, s):
    if s < polysize:
        x01 = x1 - x0
        y01 = y1 - y0
        z01 = z1 - z0

        x12 = x2 - x1
        y12 = y2 - y1
        z12 = z2 - z1

        x20 = x0 - x2
        y20 = y0 - y2
        z20 = z0 - z2

        nx = y01 * (-z20) - (-y20) * z01
        ny = z01 * (-x20) - (-z20) * x01
        nz = x01 * (-y20) - (-x20) * y01

        den = math.sqrt(nx*nx + ny*ny + nz*nz)

        if den > 0.0:
            nx /= den
            ny /= den
            nz /= den

        glNormal3f(nx, ny, nz)
        glBegin(GL_TRIANGLES)
        glVertex3f(x0, y0, z0)
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
        glEnd()

        return

    x01 = 0.5 * (x0 + x1)
    y01 = 0.5 * (y0 + y1)
    z01 = 0.5 * (z0 + z1)

    x12 = 0.5 * (x1 + x2)
    y12 = 0.5 * (y1 + y2)
    z12 = 0.5 * (z1 + z2)

    x20 = 0.5 * (x2 + x0)
    y20 = 0.5 * (y2 + y0)
    z20 = 0.5 * (z2 + z0)

    s *= 0.5

    random.seed(x01)
    random.seed(y01)
    z01 += 0.3*s*(2.0*(random.random()/1.0) - 1.0)
    random.seed(x12)
    random.seed(y12)
    z12 += 0.3*s*(2.0*(random.random()/1.0) - 1.0)
    random.seed(x20)
    random.seed(y20)
    z20 += 0.3*s*(2.0*(random.random()/1.0) - 1.0)

    mountain(x0,y0,z0,x01,y01,z01,x20,y20,z20,s)
    mountain(x1,y1,z1,x12,y12,z12,x01,y01,z01,s)
    mountain(x2,y2,z2,x20,y20,z20,x12,y12,z12,s)
    mountain(x01,y01,z01,x12,y12,z12,x20,y20,z20,s)


def init(): # init data and setup OpenGL environment here
    white = [1.0, 1.0, 1.0, 1.0]
    lpos = [0.0, 1.0, 0.0, 0.0]

    #enable 2 light sources
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    #set up different aspects of lighting
    glLightfv(GL_LIGHT0, GL_POSITION, lpos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, white)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, white)
    glLightfv(GL_LIGHT0, GL_SPECULAR, white)

    glClearColor(0.5, 0.5, 1.0, 0.0) #blue background color
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()


def display():
    tanamb = [0.2, 0.15, 0.1, 1.0]
    tandiff = [0.4, 0.3, 0.2, 1.0]

    seaamb = [0.0, 0.0, 0.2, 1.0]
    seadiff = [0.0, 0.0, 0.8, 1.0]
    seaspec = [0.5, 0.5, 1.0, 1.0]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity() #clear the matrix

    moveForward() #constantly call function to move eye forward some speed

    #viewing transformation
    gluLookAt(eye_x, eye_y, eye_z, lookat_x, lookat_y, lookat_z, up_x, up_y, up_z)

    glTranslatef(0.0, -0.15, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glTranslatef(-0.5, -0.5, 0.0) #modeling transformation

    #color the mountain
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, tanamb)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, tandiff)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, tandiff)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 10.0)

    mountain(0.0,0.0,0.0, 1.0,0.0,0.0, 0.0,1.0,0.0, 1.0)
    mountain(1.0,1.0,0.0, 0.0,1.0,0.0, 1.0,0.0,0.0, 1.0)

    #draw color the sea
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, seaamb)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, seadiff)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, seaspec)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 10.0)

    glNormal3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(0.0, 0.0, sealevel)
    glVertex3f(1.0, 0.0, sealevel)
    glVertex3f(1.0, 1.0, sealevel)
    glVertex3f(0.0, 1.0, sealevel)
    glEnd()

    glutSwapBuffers()
    glFlush()

    glutPostRedisplay()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, 1.0, 0.01, 10.0)
    glMatrixMode(GL_MODELVIEW)

def slant(flag):
    global up_x
    global up_y
    global up_z

    #up vector
    x1 = up_x - eye_x
    y1 = up_y - eye_y
    z1 = up_z - eye_z

    global lookat_x
    global lookat_y
    global lookat_z

    #lookat vector
    x0 = lookat_x - eye_x
    y0 = lookat_y - eye_y
    z0 = lookat_z - eye_z

    #lookat and up crossproduct
    x = y0*z1 - z0*y1
    y = x1*z0 - x0*z1
    z = x0*y1 - y0*x1


    if flag == True: #slant upwards
        cosine = math.cos(pitch)
        sine = math.sin(pitch)

    else: #slant downwards
        cosine = math.cos(-1*pitch)
        sine = math.sin(-1*pitch)


    up_x = eye_x + x1*(math.pow(x,2)*(1-cosine)+cosine) + y1*(x*y*(1-cosine)-z*sine) + z1*(x*z*(1-cosine)+y*sine)
    up_y = eye_y + x1*(x*y*(1-cosine)+z*sine) + y1*(math.pow(y,2)*(1-cosine)+cosine) + z1*(y*z*(1-cosine)-x*sine)
    up_z = eye_z + x1*(x*z*(1-cosine)-y*sine) + y1*(y*z*(1-cosine)+x*sine) + z1*(math.pow(z,2)*(1-cosine)+cosine)

    lookat_x = eye_x + x0*(math.pow(x,2)*(1-cosine)+cosine) + y0*(x*y*(1-cosine)-z*sine) + z0*(x*z*(1-cosine)+y*sine)
    lookat_y = eye_y + x0*(x*y*(1-cosine)+z*sine) + y0*(math.pow(y,2)*(1-cosine)+cosine) + z0*(y*z*(1-cosine)-x*sine)
    lookat_z = eye_z + x0*(x*z*(1-cosine)-y*sine) + y0*(y*z*(1-cosine)+x*sine) + z0*(math.pow(z,2)*(1-cosine)+cosine)


def twist(flag):
    #lookat vector
    x = lookat_x - eye_x
    y = lookat_y - eye_y
    z = lookat_z - eye_z

    #normalize lookat vector
    x = x/math.sqrt(x*x+y*y+z*z)
    y = y/math.sqrt(x*x+y*y+z*z)
    z = z/math.sqrt(x*x+y*y+z*z)

    global up_x
    global up_y
    global up_z
    x0 = up_x - eye_x
    y0 = up_y - eye_y
    z0 = up_z - eye_z

    if flag == True: #rotate clockwise
        cosine = math.cos(roll)
        sine = math.sin(roll)

    else: #rotate counter clockwise
        cosine = math.cos(roll*-1)
        sine = math.sin(roll*-1)

    up_x = eye_x + x0*(math.pow(x,2)*(1-cosine)+cosine) + y0*(x*y*(1-cosine)-z*sine) + z0*(x*z*(1-cosine)+y*sine)
    up_y = eye_y + x0*(x*y*(1-cosine)+z*sine) + y0*(math.pow(y,2)*(1-cosine)+cosine) + z0*(y*z*(1-cosine)-x*sine)
    up_z = eye_z + x0*(x*z*(1-cosine)-y*sine) + y0*(y*z*(1-cosine)+x*sine) + z0*(math.pow(z,2)*(1-cosine)+cosine)


def moveForward():
    global lookat_x
    global lookat_y
    global lookat_z
    global eye_x
    global eye_y
    global eye_z

    eye_x += (lookat_x - eye_x)*movespeed
    eye_y += (lookat_y - eye_y)*movespeed
    eye_z += (lookat_z - eye_z)*movespeed

    lookat_x += (lookat_x - eye_x)*movespeed
    lookat_y += (lookat_y - eye_y)*movespeed
    lookat_z += (lookat_z - eye_z)*movespeed

    global up_x
    global up_y
    global up_z
    up_x += (lookat_x - eye_x)*movespeed
    up_y += (lookat_y - eye_y)*movespeed
    up_z += (lookat_z - eye_z)*movespeed


def keyboard(key, x, y):
    #put your keyboard control here
    global sealevel
    global polysize
    if key == chr(61): # '=' key to raise sea level
        sealevel += 0.01
        print "sea level ++"

    if key == chr(45): # '-' key to lower sea level
        sealevel -= 0.01
        print "sea level --"

    if key == chr(102): # 'f' key to increase resolution
        polysize *= 0.5

    if key == chr(99): # 'c' key to decrease resolution
        polysize *= 2.0

    if key == chr(27): # esc key to quit
        print "demonstration finished."
        sys.exit(0)

def arrowKeys(key,x,y):
    if key == GLUT_KEY_UP:
        slant(True)
        print "up"

    if key == GLUT_KEY_DOWN:
        slant(False)
        print "down"

    if key == GLUT_KEY_RIGHT:
        twist(True)
        print "right"

    if key == GLUT_KEY_LEFT:
        twist(False)
        print "left"

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("MP1")
    #set up for double-buffering & RGB color
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    init() #setting up user data & OpenGL environment

    glutDisplayFunc(display) #called when drawing
    glutReshapeFunc(reshape) #called when change window size
    glutKeyboardFunc(keyboard) #called when received keyboard interaction
    glutSpecialFunc(arrowKeys) #called when using arrow keys

    glutMainLoop() # start the main message-callback loop
