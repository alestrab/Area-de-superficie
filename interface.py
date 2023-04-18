from tkinter import *
import tkinter.ttk as ttk
import numpy as np
from tkinter.filedialog import askopenfilename
from sys import exit
import matplotlib.pyplot as plt
from PIL import Image
from regions import PixCoord, PolygonPixelRegion

def open_imag():
    global dots
    global plot_dots
    global line_dots
    global surface
    filename = askopenfilename()
    if filename=='':
        exit()
    plt.clf()
    dots=[]
    line_dots=[]
    surface=True
    area_surf_text.set('')
    area_text.set('')
    dist_text.set('')
        
    instructions_txt.configure(text='Desenhe pontos ao redor da região a ter sua área estimada. \n Pressione \'c\' para concluir.')    
    img = np.asarray(Image.open(filename))
    plt.axis('off')
    plt.imshow(img,zorder=0)
    plt.connect("button_press_event", mouse_event)
    plt.connect("key_press_event", keyboard_event)
    plt.connect("close_event", on_close)
    plt.show()

def on_close(event):
    root.quit()
    root.destroy()


    
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
        exit('remove_point-Erro ao Retirar Ponto')      
        
def mouse_event(event):
    global dots
    global plot_dots
    global line_dots
    global surface
    #events:
    #1 - Left button
    #2 - Middle button
    #3 - Right button
    finished = (not surface) and (len(np.array(line_dots))==2) and (dist_text.get()!='')
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
                if surface|((not surface)&(len(np.array(point_list))<2)):
                    add_point(point_list,x,y)
            points = np.array(point_list)
            #Remove nearest point
            if (button==3)&(len(points)>0):
                remove_point(point_list,x,y)
            points = np.array(point_list)
            #Plot new points
            if len(points)>0:
                plt.ion()
                plot_dots = plt.plot(points[:,0],points[:,1],color,zorder=1)
                plt.ioff()
    
def keyboard_event(event):
    global dots
    global plot_dots
    global line_dots
    global surface
    #events:
    #c/C - Finish drawing 
    finished = (not surface) and (len(np.array(line_dots))==2)
    
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
        elif finished:
            finish_area(line_dots)
            

def area_surface(points):
    vertices = PixCoord(x=points[:,0], y=points[:,1])
    reg = PolygonPixelRegion(vertices=vertices)
    reg.plot(facecolor='#FF0000', fill=True,zorder=2,
                 label='Polygon')
    new_text = str(np.round(reg.area,1))
    area_text.set(new_text)
    instructions_txt.configure(text='Selecione dois pontos indicando um comprimento conhecido.\n Pressione \'c\' para concluir.')

def finish_area(length):
    dist=np.array(length)
    dist_pixel = np.linalg.norm(dist[1]-dist[0])
    new_text = str(np.round(dist_pixel,1))    
    dist_text.set(new_text)
    evaluate_area()

def evaluate_area():
    l=lenght_ref_l.get()
    try:
        l = float(l)
        n = l/float(lenght_pix_l.get())
        new_text = str(np.round(float(area_pix_l.get())*(n**2),1))
        area_surf_text.set(new_text)
        instructions_txt.configure(text='Área da Região Estimada.')
    except:
        new_text = '-'
        area_surf_text.set(new_text)
        lenght_u_t.current(0)
        instructions_txt.configure(text='Coloque o Comprimento do Segmento de Referência.')
    return True

   

def area_custom(event):
    unit = lenght_u_t.get()
    if unit !='-':
        area_surf_u.configure(text=unit+'²')
    else:
        area_surf_u.configure(text='-'  )
        
        
#Points to evaluate length
dots=[]
line_dots=[]
surface=True

#Tkinter interface
root = Tk()
root.wm_title("Area de Superficies")

area = Frame(master=root)
area.pack(side=TOP,expand=1)

instructions = Frame(master=root)
instructions.pack(side=TOP,expand=1)


fig,ax = plt.subplots(figsize=(5, 4), dpi=200,num='Imagem-Area de Superficies')

img_op = Button(master=area, text="Inserir Imagem", command=open_imag,bg='blue',bd=3,height=4,fg='white',width=12)
img_op.pack(side=LEFT,padx=(10,50),expand=1)

area_t = Frame(master=area)
area_t.pack(side=LEFT,expand=1)

area_l = Frame(master=area)
area_l.pack(side=LEFT,expand=1)

lenght_ref_t = Label(area_t,text='Comprimento de Referência: ')
lenght_ref_t.pack(side=TOP,expand=1)

lenght_pix_t = Label(area_t,text='Comprimento de Referência: ')
lenght_pix_t.pack(side=TOP,expand=1)

area_pix_t = Label(area_t,text='Região Preenchida: ')
area_pix_t.pack(side=TOP,expand=1)

area_surf_t = Label(area_t,text='Área da Região Preenchida: ')
area_surf_t.pack(side=TOP,expand=1)

lenght_ref_l = Entry(area_l,width=10,state='normal',validate="focusout", validatecommand=evaluate_area)
lenght_ref_l.pack(side=TOP)

dist_text = StringVar()
lenght_pix_l = Entry(area_l,width=10,state='readonly',textvariable=dist_text)
lenght_pix_l.pack(side=TOP)

area_text = StringVar()
area_pix_l = Entry(area_l,width=10,state='readonly',textvariable=area_text)
area_pix_l.pack(side=TOP)

area_surf_text = StringVar()
area_surf_l = Entry(area_l,width=10,state='readonly',textvariable=area_surf_text)
area_surf_l.pack(side=TOP)


area_u = Frame(master=area)
area_u.pack(side=LEFT,expand=1,padx=(10,0))
        
lenght_u_t = ttk.Combobox(master=area_u,width=4,state="readonly")
lenght_u_t['values'] = ['-','m','cm','mm']
lenght_u_t.current(0)
lenght_u_t.pack(side=TOP,expand=1)
lenght_u_t.bind('<<ComboboxSelected>>', area_custom)

lenght_pix_u = Label(area_u,text='Pixels')
lenght_pix_u.pack(side=TOP,expand=1)

area_pix_u = Label(area_u,text='Pixels')
area_pix_u.pack(side=TOP,expand=1)

area_surf_u = Label(area_u,text='-')
area_surf_u.pack(side=TOP,expand=1)

def _quit():
    plt.close('all')
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


quit = Button(master=area, text="Sair", command=_quit,bg='red',bd=3,height=4,padx=10,fg='white',width=10)
quit.pack(side=LEFT,padx=(100,10))


instructions_txt = Label(text='Insira uma imagem para iniciar o programa.',master=instructions)
instructions_txt.pack(side=LEFT,padx=(10,10))

commands = Frame(master=instructions)
commands.pack(side=LEFT)

commands_title = Label(text='Comandos',master=commands)
commands_title.pack(side=TOP)
commands_lft = Label(text='Botão Esquerdo - Selecionar Ponto.',master=commands)
commands_lft.pack(side=TOP,padx=(10,10))

commands_rgt = Label(text='Botão Direito - Remover Ponto mais Próximo.',master=commands)
commands_rgt.pack(side=TOP,padx=(10,10))

commands_c = Label(text='c - Concluir Etapa.',master=commands)
commands_c.pack(side=TOP,padx=(10,10))


def on_closing():
    plt.close('all')
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

mainloop()