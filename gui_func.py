from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename 
import threading
import time
import numpy as np
##import tkinter.ttk
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
##############################################
master = Tk()
w, h = master.winfo_screenwidth(), master.winfo_screenheight()
#master.overrideredirect(1)
##master.geometry("%dx%d+%d+%d" % (w/4, h/5, w/2.5, h/2.5))
master.title('IDF to HydroGraph converter')

#master.iconbitmap(r'C:\Users\golu\Downloads\IMG-20200528-WA0001.ico')
#master.iconbitmap(r'IMG-20200528-WA0001.ico')
master.geometry('800x250')
master.resizable(0, 0)
#master.maxsize(500,300)


def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.3f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
def altblocks(idf,dur,dt,RP):
    aDur = np.arange(dt,dur+dt,dt)    # in minutes
    aInt = (idf[0]*RP**idf[1])/((aDur/60+idf[2])**idf[3])  # idf equation - in mm/h
    aDeltaPmm = np.diff(np.append(0,np.multiply(aInt,aDur/60.0)))
    aOrd=np.append(np.arange(1,len(aDur)+1,2)[::-1],np.arange(2,len(aDur)+1,2))
    prec = np.asarray([aDeltaPmm[x-1] for x in aOrd])
    aAltBl = np.vstack((aDur,prec))
    width = dur/len(aAltBl[0])
##    print(aAltBl)
    plt.ioff()
    master.geometry('800x700')
    
    fig, ax = plt.subplots()
    bar1 = FigureCanvasTkAgg(fig, master)
    bar1.get_tk_widget().grid(row=6, column=0, rowspan=1, columnspan=4)
    ax.bar(aAltBl[0], aAltBl[1], width=-(width+0.5), align='edge')
    ax.set_xlabel("Duration (min)", fontdict=None, labelpad=None)
    ax.set_ylabel("Precipitation (mm)", fontdict=None, labelpad=None)
    
    max_val = max(aAltBl[1])
    plt.ylim(0, max_val+0.5)
    plt.close()
#    fig, ax = plt.subplots()
#    pl = ax.bar(aAltBl[0], aAltBl[1], width=-(width+0.5), align='edge')
#    ax.set_xlabel("Duration (min)", fontdict=None, labelpad=None)
#    ax.set_ylabel("Precipitation (mm)", fontdict=None, labelpad=None)
#    
#    max_val = max(aAltBl[1])
#    plt.ylim(0, max_val+0.5)
#
#    curr_wd = os.getcwd()
#    autolabel(pl,ax)
#    fig.savefig(os.path.join(curr_wd,"Precipitation.png"))
##    fig.show()
#    
#    photo.config(file=fig)
#    
#    plt.close(fig)
    return aAltBl

def go_to_sub():
    idf = [];
    a = float(e1.get())
    b = float(e2.get())
    c = float(e3.get())
    d = float(e4.get())
    RP = float(e5.get())
    dur = float(e6.get())
    dt = float(e7.get())

    idf.append(a)
    idf.append(b)
    idf.append(c)
    idf.append(d)
    
    altblocks(idf, dur, dt, RP)
    
    
    
def go_to_quit():
    master.destroy()


######################################################
Label(master, text="IDF Characterstics", font=("Calibri 15")).grid(row=0, column=0)
Label(master, text="A: ").grid(row=1, column=0, sticky=W, padx=10)
Label(master, text="B: ").grid(row=2, column=0, sticky=W, padx=10)
Label(master, text="C: ").grid(row=3, column=0, sticky=W, padx=10)
Label(master, text="D: ").grid(row=4, column=0, sticky=W, padx=10)


equ = Label(master, text="i = (aT\u1d47)/(t+c)\u1d48\n", justify='center',
            anchor='center', font=("Calibri 15"))
equ.grid(row=5, column=0, padx=20, sticky=W)

e1 = Entry(master, width=30)
e2 = Entry(master, width=30)
e3 = Entry(master, width=30)
e4 = Entry(master, width=30)
##########################################
e1.insert(10, 6.275)
e2.insert(10, 0.126)
e3.insert(10, 0.5)
e4.insert(10, 1.128)
######################################
e1.grid(row=1, column=0,pady=5, sticky=E, padx=50)
e2.grid(row=2, column=0,pady=5, sticky=E, padx=50)
e3.grid(row=3, column=0,pady=5, sticky=E, padx=50)
e4.grid(row=4, column=0,pady=5, sticky=E, padx=50)

Label(master, text="HydroGraph Characterstics", font=("Calibri 15")).grid(row=0, column=1)
Label(master, text="T (years): ").grid(row=1, column=1, sticky=W)
Label(master, text="Duration (min): ").grid(row=2, column=1, sticky=W)
Label(master, text="Time Step (min): ").grid(row=3, column=1, sticky=W)
e5 = Entry(master, width=30)
e6 = Entry(master, width=30)
e7 = Entry(master, width=30)

e5.insert(10, 10)
e6.insert(10, 120)
e7.insert(10, 10)
###################################################
#photo = PhotoImage()
#lbl = Label(master, image=photo)
#lbl.grid(row=5, column=0, rowspan=1, columnspan=4)
##############################################
e5.grid(row=1, column=1,pady=5, sticky=E, padx=120)
e6.grid(row=2, column=1,pady=5, sticky=E, padx=120)
e7.grid(row=3, column=1,pady=5, sticky=E, padx=120)


start_btn =  Button(master, text="Submit", bg="light blue", command=go_to_sub, disabledforeground='grey')          ##   browse button for offlien mode
start_btn.grid(row=4, column=1, sticky=W, pady=5,padx=150)  

quit_btn =  Button(master, text="Quit", bg="red", command=go_to_quit, disabledforeground='grey')          ##   browse button for offlien mode
quit_btn.grid(row=4, column=1, sticky=W, pady=5,padx=100)


master.mainloop()
