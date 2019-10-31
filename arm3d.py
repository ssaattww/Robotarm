import math
import numpy as np
import matplotlib.pyplot as plt
import copy#use for deepcopy
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

low = 0
up  = 2*math.pi

def update(val):
    m_size = 2

    deg1 = theta1.val
    deg2 = theta2.val
    deg3 = theta3.val
    print("[",deg1,',',deg2,',',deg3,"]")
    x1 = L1 * np.cos(deg1)
    y1 = L1 * np.sin(deg1)
    x2 = x1 + L2 * np.cos(deg1+deg2)
    y2 = y1 + L2 * np.sin(deg1+deg2)
    x3 = x2 + L3 * np.cos(deg1+deg2+deg3)
    y3 = y2 + L3 * np.sin(deg1+deg2+deg3)
    x = [0.0, x1, x2, x3]
    y = [0.0, y1, y2, y3]
    col = False
    
    #Repeat for the number of arms
    for i in range(len(x)-1):
        a = coordinate2d()
        a.xs = x[i]
        a.ys = y[i]
        a.xd = x[i+1]
        a.yd = y[i+1]            
        #Repeat for the number of obstacles
        for j in objects:
            col = collision(a,j)
            if col == True:
                break
        if col == True:
            break
    if col:#If The arm was a collision
        plots.set_color("green")
        cfg_ax.scatter(deg1,deg2,deg3,color="r")
    else:
        plots.set_color("red")
        cfg_ax.scatter(deg1,deg2,deg3,color="b")
    
    ax.axis('equal')
    ax.set_xlim(-11,11)
    ax.set_ylim(-11,11)
    
    cfg_ax.axis('equal')
    cfg_ax.set_xlim(low*1.05, up*1.05)
    cfg_ax.set_ylim(low*1.05, up*1.05)

    #update the plots
    plots.set_data(x,y)

    fig.canvas.draw_idle()

class coordinate2d:
    def __init__(self,xs=0,ys=0,xd=0,yd=0):
        self.xs = xs
        self.ys = ys
        self.xd = xd
        self.yd = yd
    def get(self):
        return[[self.xs,self.ys],[self.xd,self.yd]]
    def print(self):
        print('{:.5g}'.format(self.xs)," ",'{:.5g}'.format(self.ys)," ",'{:.5g}'.format(self.xd)," ",'{:.5g}'.format(self.yd),end="")    

def collision(_a,_b):
    a = copy.deepcopy(_a)
    b = copy.deepcopy(_b)
    aa = copy.deepcopy(_a)
    bb = copy.deepcopy(_b)
    #Determine if two straight lines intersect a-b and c-d
    #     c
    #     |
    #a----------b
    #     |
    #     d
    #
    #    b_s
    #     |
    #a_s----------a_d
    #     |
    #    b_d
    #
    
    #Move point [a] to the origin.
    a.xd -= _a.xs
    a.yd -= _a.ys
    b.xs -= _a.xs
    b.ys -= _a.ys
    b.xd -= _a.xs
    b.yd -= _a.ys
    #Caluculate vector product between a-b and a-c,a-d.
    temp1 = a.xd*b.ys - a.yd*b.xs
    temp2 = a.xd*b.yd - a.yd*b.xd

    #Move point [c] to the origin.
    aa.xs -= _b.xs
    aa.ys -= _b.ys
    aa.xd -= _b.xs
    aa.yd -= _b.ys
    bb.xd -= _b.xs
    bb.yd -= _b.ys

    #Caluculate vector product between c-d and c-b,c-d
    temp3 = bb.xd*aa.ys - bb.yd*aa.xs
    temp4 = bb.xd*aa.yd - bb.yd*aa.xd

    #if vector product result has same sign non-collision.
    if temp1*temp2 <= 0.0 and temp3*temp4 <= 0.0:
        return True #collision
    else:
        return False

if __name__ == '__main__':
    #init figure and axes
    fig = plt.figure(figsize=(10,5))

    ax = fig.add_subplot(121)
    cfg_ax = fig.add_subplot(122,projection='3d')

    #Adjust because slider and graph collide.
    plt.subplots_adjust(left=0.25, bottom=0.30)

    ax.axis('equal')
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)

    cfg_ax.set_xlim(low*1.05, up*1.05)
    cfg_ax.set_ylim(low*1.05, up*1.05)
    cfg_ax.set_zlim(low*1.05, up*1.05)
    cfg_ax.axis('equal')

    #link`s length
    L1 = 2.0
    L2 = 2.0
    L3 = 2.0

    #joint`s angles
    deg1 = 0
    deg2 = 0
    deg3 = 0

    #init obstacles
    objects = [coordinate2d(-6.0,2.0,-5.0,-2.0),coordinate2d(2.0,1.0,2.0,-1.0)]
    oxs = []
    oys = []
    oxd = []
    oyd = []
    for i in objects:
        oxs.append(i.xs)
        oxd.append(i.xd)
        oys.append(i.ys)
        oyd.append(i.yd)

    #init slider 
    theta1 = Slider(plt.axes([0.25,0.0,0.65,0.03]), 'theta1', low, up, valinit=deg1)
    theta2 = Slider(plt.axes([0.25,0.05,0.65,0.03]), 'theta2', low, up, valinit=deg2)
    theta3 = Slider(plt.axes([0.25,0.1,0.65,0.03]), 'theta3', low, up, valinit=deg3)

    #link1
    x1 = L1 * np.cos(deg1)
    y1 = L1 * np.sin(math.radians(deg1))

    #link2
    x2 = x1 + L2 * np.cos(deg1+deg2)
    y2 = y1 + L2 * np.sin(deg1+deg2)

    #link3
    x3 = x2 + L3 * np.cos(deg1+deg2+deg3)
    y3 = y2 + L3 * np.sin(deg1+deg2+deg3)

    x = [0.0, x1, x2, x3]
    y = [0.0, y1, y2, y3]

    #Plot
    plots, = ax.plot(x,y,"r-")

    for x_s,y_s,x_d,y_d in zip(oxs,oys,oxd,oyd):
        ax.plot([x_s,x_d],[y_s,y_d],"g-")
    
    theta1.on_changed(update)
    theta2.on_changed(update)
    theta3.on_changed(update)

    plt.show()

