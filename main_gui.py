from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import numpy as np
import cv2
import line
import region_selector as rs
import automatic_traffic_analysis as automatic

def openfilename():
    filename = filedialog.askopenfilename(title ='Open Image')
    return filename

def display_img(img,r,c):
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image = img)
    panel.image = img
    panel.place(x=r,y=c)

def open_video():
    x = openfilename()
    try:
        vid = cv2.VideoCapture(x)
    except:
        vid = cv2.VideoCapture(x)
    count=0
    while count!=1:
        _, img = vid.read()
        #cv2.imshow("image",img)
        count+=1
    cv2.imwrite("saved.jpg",img)
    line.image_select("saved.jpg",x)
    
def open_video2():
    x = openfilename()
    try:
        vid = cv2.VideoCapture(x)
    except:
        vid = cv2.VideoCapture(x)
    count=0
    while count!=1:
        _, img = vid.read()
        #cv2.imshow("image",img)
        count+=1
    cv2.imwrite("saved.jpg",img)
    rs.image_select("saved.jpg",x)
    
def open_video3():
    x = openfilename()
    automatic.mainfunc(x)

def close():
    root.destroy()

root = Tk()

# Set Title as Image Loader
root.title("Smart Traffic Management")


# Set the resolution of window
root.geometry("500x400")

# Allow Window to be resizable
root.resizable(width = True, height = True)

l1 = Label(root,text="SMART TRAFFIC MANAGEMENT")
l1.place(x=150,y=40)
btn = Button(root, text ='Select Video', command = open_video).place(x = 350, y = 100 )
l2 = Label(root,text="Traffic Light Violation Detection")
l2.place(x=50,y=100)
btn2 = Button(root, text ='Select Video', command = open_video2).place(x = 350, y = 140 )
l2 = Label(root,text="Traffic Density Calculation")
l2.place(x=50,y=140)
btn3 = Button(root, text ='Select Video', command = open_video3).place(x = 350, y = 180 )
l2 = Label(root,text="Automatic Traffic Analysis")
l2.place(x=50,y=180)

btn3=Button(root, text="Quit", command=close).place(x=250,y=250)
    
root.mainloop()