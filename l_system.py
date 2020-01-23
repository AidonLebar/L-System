import sys
import math
from datetime import datetime
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU  import *
from grammar import Grammar
from PIL import Image
from PIL import ImageOps

width = 600
height = 600
step = 10
g = Grammar()

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
    c_stack = []
    p_stack = []
    d_stack = []
    current_d = [0,1] #up
    current_p = [width//2, height//5]
    glClearColor ( 0.0, 0.0, 0.0, 1.0) ;
    glClear ( GL_COLOR_BUFFER_BIT ) ;
    glBegin(GL_LINE_STRIP)
    current_c = (1.0, 1.0, 1.0)
    glColor3f(current_c[0], current_c[1], current_c[2])
    glVertex2f(current_p[0], current_p[1])
    for c in g.l_string:
        if c not in g.i_rules:
            continue
        action = g.i_rules[c].action
        if action == "push":
            c_stack.append(current_c)
            p_stack.append([current_p[0], current_p[1]])
            d_stack.append([current_d[0], current_d[1]])
            if g.i_rules[c].param_count > 0:
                try:
                    degrees = int(g.i_rules[c].params[0])
                except ValueError:
                    g.i_rules[c].error_out("Angle parameter must be an integer.")
                current_d = rotate(current_d, -degrees)
            else:
                current_d = rotate(current_d, -90) #default right
        elif action == "pop":
            current_c = c_stack.pop()
            current_p = p_stack.pop()
            current_d = d_stack.pop()
            if g.i_rules[c].param_count > 0:
                try:
                    degrees = int(g.i_rules[c].params[0])
                except ValueError:
                    g.i_rules[c].error_out("Angle parameter must be an integer.")
                current_d = rotate(current_d, degrees)
            else:
                current_d = rotate(current_d, 90) #default left
            glEnd()
            glBegin(GL_LINE_STRIP)
            glColor3f(current_c[0], current_c[1], current_c[2])
            glVertex2f(current_p[0], current_p[1])
        elif action == "right":
            if g.i_rules[c].param_count > 0:
                try:
                    degrees = int(g.i_rules[c].params[0])
                except ValueError:
                    g.i_rules[c].error_out("Angle parameter must be an integer.")
                current_d = rotate(current_d, -degrees)
            else:
                current_d = rotate(current_d, -90)
        elif action == "left":
            if g.i_rules[c].param_count > 0:
                try:
                    degrees = int(g.i_rules[c].params[0])
                except ValueError:
                    g.i_rules[c].error_out("Angle parameter must be an integer.")
                current_d = rotate(current_d, degrees)
            else:
                current_d = rotate(current_d, 90)
        elif action == "forward":
            if g.i_rules[c].param_count > 0:
                try:
                    step_param = int(g.i_rules[c].params[0])
                except ValueError:
                    g.i_rules[c].error_out("Distance parameter must be an integer.")
                current_p[0] += current_d[0] * step_param
                current_p[1] += current_d[1] * step_param
            else:
                current_p[0] += current_d[0] * step
                current_p[1] += current_d[1] * step
            glVertex2f(current_p[0], current_p[1])
        elif action == "colour":
            try:
                red = int(g.i_rules[c].params[0])/255
                green = int(g.i_rules[c].params[1])/255
                blue = int(g.i_rules[c].params[2])/255
            except ValueError:
                g.i_rules[c].error_out("Red, Green and Blue parameters must be integers.")
            if red > 1 or green > 1 or blue > 1 or \
               red < 0 or green < 0 or blue < 0:
               g.i_rules[c].error_out("Red, Green and Blue parameters must be between 0 and 255.")
            current_c = (red, green, blue)
            glColor3f(red, green, blue)
        else:
            g.i_rules[c].error_out("Unrecognized action.")
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
    g.step(6)
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("l-system")
    glutDisplayFunc(draw)
    glutKeyboardFunc(key_func)
    glutMainLoop()
