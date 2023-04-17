import numpy as np
from tkinter.filedialog import askopenfilename
import sys
import matplotlib.pyplot as plt
from PIL import Image
from regions import PixCoord, PolygonPixelRegion
        
def add_point(list,x,y):
    list.append([x,y])
    
def remove_point(list,x,y):
    points = np.array(list)
    dist = np.zeros(len(points))
    try:
        for i in range(len(points)):
            dist[i] = np.linalg.norm(points[i]-[x,y])
        min_arg = np.argmin(dist)
        list.pop(min_arg)
    except:
        sys.exit('remove_point-Remover ponto do grafico')      
        
def area_surface(points):
    vertices = PixCoord(x=points[:,0], y=points[:,1])
    reg = PolygonPixelRegion(vertices=vertices)
    patch = reg.plot(facecolor='#FF0000', fill=True,zorder=2,
                 label='Polygon')

def finish_area(point_area,length):
    global dist_pixel
    global area
    global finished
    points = np.array(point_area)
    vertices = PixCoord(x=points[:,0], y=points[:,1])
    reg = PolygonPixelRegion(vertices=vertices)
    dist=np.array(length)
    dist_pixel = np.linalg.norm(dist[1]-dist[0])
    area = reg.area
    finished=True

def mouse_event(event):
    global dots
    global plot_dots
    global line_dots
    global surface
    #events:
    #1 - Left button
    #2 - Middle button
    #3 - Right button
    if not finished:
        if surface:
            point_list = dots
            color = '.r-'
        else:
            point_list = line_dots
            color = '.b-'
        
        if ((event.xdata!=None)&(event.ydata!=None)):
            points = np.array(point_list)
            if len(points)>0:
                #Remove previous plot
                plt.ion()
                for hance in plot_dots:
                    hance.remove()
                plt.ioff
            x, y, button = int(event.xdata), int(event.ydata), event.button
            #Add new point
            if button==1:
                if surface|(not surface)&(len(np.array(point_list))<2):
                    add_point(point_list,x,y)
            points = np.array(point_list)
            #Remove nearest point
            if (button==3)&(len(points)>0):
                remove_point(point_list,x,y)
            points = np.array(point_list)
            #Plot new points
            if len(points)>0:
                plot_dots = plt.plot(points[:,0],points[:,1],color)
    
def keyboard_event(event):
    global dots
    global plot_dots
    global line_dots
    global surface
    #events:
    #c/C - Finish drawing 
    if not finished:
        key = event.key
        if ((key=='c')|(key=='C')):
            points = np.array(dots)
            area_surface(points)
            if surface&(len(points)>2):
                surface=False
                plt.ion()
                for hance in plot_dots:
                    hance.remove()
                plt.ioff
            elif (not surface)&(len(line_dots)==2):
                finish_area(dots,line_dots)
                plt.close()
            
#Points to evaluate length
dots=[]
line_dots=[]
surface=True
area=0
dist_pixel=0
finished=False
#Global variables
def process_image():
    global fig,ax,dots,line_dots,surface,area,dist_pixel
    fig,ax = plt.subplots()
    #Vertices of surface
    dots=[]
    #Points to evaluate length
    line_dots=[]

    surface=True
    area=0
    dist_pixel=0
    plt.axis('off')
    plt.connect('button_press_event', mouse_event)
    plt.connect('key_press_event', keyboard_event)
    plt.show()
    return area,dist_pixel