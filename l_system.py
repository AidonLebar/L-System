import sys
import math
from datetime import datetime
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU  import *
from grammar import grammar
from PIL import Image
from PIL import ImageOps

width = 600
height = 600
step = 10
g = grammar()

def rotate(dir, angle):
    angle = math.radians(angle)
    x = (math.cos(angle)*dir[0]) - (math.sin(angle)*dir[1])
    y = (math.sin(angle)*dir[0]) + (math.cos(angle)*dir[1])
    return [x,y]

def draw():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    p_stack = []
    d_stack = []
    current_d = [0,step] #up
    current_p = [width//2, height//2]
    glClearColor ( 0.0, 0.0, 0.0, 1.0) ;
    glClear ( GL_COLOR_BUFFER_BIT ) ;
    glBegin(GL_LINE_STRIP)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(current_p[0], current_p[1])
    for c in g.l_string:
        if c not in g.i_rules.keys():
            continue
        action = g.i_rules[c]
        if action == "push":
            p_stack.append([current_p[0], current_p[1]])
            d_stack.append([current_d[0], current_d[1]])
            current_d = rotate(current_d, -90) #right 
        elif action == "pop":
            current_p = p_stack.pop()
            current_d = d_stack.pop()
            current_d = rotate(current_d, 90) #left
            glEnd()
            glBegin(GL_LINE_STRIP)       
            glColor3f(1.0, 1.0, 1.0);       
            glVertex2f(current_p[0], current_p[1])
        if action == "right":
            current_d = rotate(current_d, -90)
        elif action == "left":
            current_d = rotate(current_d, 90)
        elif action == "forward":
            current_p[0] += current_d[0]
            current_p[1] += current_d[1]
            glVertex2f(current_p[0], current_p[1])
    glEnd()
    glutSwapBuffers()
    
def key_func(key, x, y):
    if key == b'\x03' or key == b'q':
        exit()
    if key == b's':
        now = datetime. now()
        time = now.strftime("%H-%M-%S")
        print("Saving image as {}.png".format(time))
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (width, height), data)
        image = ImageOps.flip(image)
        image.save("{}.png".format(time), "PNG")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide grammar file.")
        exit()
    file = sys.argv[1]
    g.parse(file)
    g.step(10)
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("l-system")
    glutDisplayFunc(draw)
    glutKeyboardFunc(key_func)
    glutMainLoop()
