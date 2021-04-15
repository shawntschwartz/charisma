##Adapted from programming_fever
##https://medium.com/programming-fever/color-detection-using-opencv-python-6eec8dcde8c7

##Imports
import cv2
import numpy as np
import pandas as pd
import os
import sys
from tkinter import Tk # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from pdf2image import convert_from_path ##from Shawn: you'll need to install poppler with home-brew or from poppler's website (`brew install poppler`)

##force window to be at the top of all other windows upon loading
root = Tk()
root.lift()
root.wm_attributes('-topmost', 1)  
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print("opening {}".format(filename))

img_path = filename

##check format of filename and convert if PDF
pdf_status = False
if img_path.endswith(".pdf"):
    pdf_status = True
    images_converted = convert_from_path(img_path)
    images_converted[0].save(filename + '.jpg', 'JPEG')
    img_path = filename + '.jpg'

img = cv2.imread(img_path)
print('Original Dimensions : ', img.shape)

##scale images to 1000 pixels
scale_factor = 1000 / img.shape[1]
width = int(img.shape[1] * scale_factor)
height = int(img.shape[0] * scale_factor)
dim = (width, height)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
print('Rescaled Dimensions : ', img.shape)

##user instructions
print("PRESS 'q' TO QUIT WHILE IN THE WINDOW!")

clicked = False
r = g = b = xpos = ypos = 0



def test_black(df):
	return((((df['H'].ge(0) & df['H'].le(360))) & ((df['S'].ge(0) & df['S'].le(100))) & ((df['V'].ge(0) & df['V'].le(30)))))
 

def test_white(df):
	return((((df['H'].ge(0) & df['H'].le(360))) & ((df['S'].ge(0) & df['S'].le(19))) & ((df['V'].ge(86) & df['V'].le(100)))))
 

def test_grey(df):
	return((((df['H'].ge(0) & df['H'].le(360))) & ((df['S'].ge(0) & df['S'].le(25))) & ((df['V'].ge(31) & df['V'].le(40)))) | (((df['H'].ge(0) & df['H'].le(360))) & ((df['S'].ge(0) & df['S'].le(19))) & ((df['V'].ge(41) & df['V'].le(60)))) | (((df['H'].ge(0) & df['H'].le(360))) & ((df['S'].ge(0) & df['S'].le(19))) & ((df['V'].ge(61) & df['V'].le(75)))) | (((df['H'].ge(0) & df['H'].le(360))) & ((df['S'].ge(0) & df['S'].le(15))) & ((df['V'].ge(76) & df['V'].le(85)))))
 

def test_brown(df):
	return((((df['H'].ge(0) & df['H'].le(54)) | (df['H'].ge(300) & df['H'].le(360))) & ((df['S'].ge(26) & df['S'].le(100))) & ((df['V'].ge(31) & df['V'].le(40)))) | (((df['H'].ge(0) & df['H'].le(54)) | (df['H'].ge(300) & df['H'].le(360))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(41) & df['V'].le(60)))) | (((df['H'].ge(16) & df['H'].le(54))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(61) & df['V'].le(75)))))
 

def test_red(df):
	return((((df['H'].ge(0) & df['H'].le(15)) | (df['H'].ge(300) & df['H'].le(360))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(61) & df['V'].le(75)))) | (((df['H'].ge(0) & df['H'].le(19)) | (df['H'].ge(300) & df['H'].le(360))) & ((df['S'].ge(16) & df['S'].le(100))) & ((df['V'].ge(76) & df['V'].le(85)))) | (((df['H'].ge(0) & df['H'].le(19)) | (df['H'].ge(300) & df['H'].le(360))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(86) & df['V'].le(100)))))
 

def test_orange(df):
	return((((df['H'].ge(20) & df['H'].le(45))) & ((df['S'].ge(16) & df['S'].le(100))) & ((df['V'].ge(76) & df['V'].le(85)))) | (((df['H'].ge(20) & df['H'].le(35))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(86) & df['V'].le(100)))))
 

def test_yellow(df):
	return((((df['H'].ge(46) & df['H'].le(61))) & ((df['S'].ge(16) & df['S'].le(100))) & ((df['V'].ge(76) & df['V'].le(85)))) | (((df['H'].ge(36) & df['H'].le(61))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(86) & df['V'].le(100)))))
 

def test_green(df):
	return((((df['H'].ge(55) & df['H'].le(165))) & ((df['S'].ge(26) & df['S'].le(100))) & ((df['V'].ge(31) & df['V'].le(40)))) | (((df['H'].ge(55) & df['H'].le(165))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(41) & df['V'].le(60)))) | (((df['H'].ge(55) & df['H'].le(165))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(61) & df['V'].le(75)))) | (((df['H'].ge(62) & df['H'].le(165))) & ((df['S'].ge(16) & df['S'].le(100))) & ((df['V'].ge(76) & df['V'].le(85)))) | (((df['H'].ge(62) & df['H'].le(165))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(86) & df['V'].le(100)))))
 

def test_blue(df):
	return((((df['H'].ge(166) & df['H'].le(266))) & ((df['S'].ge(26) & df['S'].le(100))) & ((df['V'].ge(31) & df['V'].le(40)))) | (((df['H'].ge(166) & df['H'].le(266))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(41) & df['V'].le(60)))) | (((df['H'].ge(166) & df['H'].le(266))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(61) & df['V'].le(75)))) | (((df['H'].ge(166) & df['H'].le(266))) & ((df['S'].ge(16) & df['S'].le(100))) & ((df['V'].ge(76) & df['V'].le(85)))) | (((df['H'].ge(166) & df['H'].le(266))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(86) & df['V'].le(100)))))
 

def test_purple(df):
	return((((df['H'].ge(267) & df['H'].le(299))) & ((df['S'].ge(26) & df['S'].le(100))) & ((df['V'].ge(31) & df['V'].le(40)))) | (((df['H'].ge(267) & df['H'].le(299))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(41) & df['V'].le(60)))) | (((df['H'].ge(267) & df['H'].le(299))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(61) & df['V'].le(75)))) | (((df['H'].ge(267) & df['H'].le(299))) & ((df['S'].ge(16) & df['S'].le(100))) & ((df['V'].ge(76) & df['V'].le(85)))) | (((df['H'].ge(267) & df['H'].le(299))) & ((df['S'].ge(20) & df['S'].le(100))) & ((df['V'].ge(86) & df['V'].le(100)))))

##identify color
def colorID(h,s,v):
	color = None
	d = {'H': [h], 'S': [s], 'V': [v]}
	df = pd.DataFrame(data=d)
	choices = ['black', 'white', 'grey', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'purple']
	conditions = [test_black(df), test_white(df), test_grey(df), test_brown(df), test_red(df), test_orange(df), test_yellow(df), test_green(df), test_blue(df), test_purple(df)]
	color = np.select(conditions, choices, default=None)
	print('the color is {}'.format(color[0]))
	return(color)

def rgb_to_hsv_2(r,g,b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return round(h), round(s), round(v)

##function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
cv2.namedWindow('Charisma - Color Detection Diagnostics Tool')
cv2.setMouseCallback('Charisma - Color Detection Diagnostics Tool',draw_function)

##main window activity
while(1):

    cv2.imshow("Charisma - Color Detection Diagnostics Tool",img)
    if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (980,60), (b,g,r), -1) 

        h,s,v = rgb_to_hsv_2(r,g,b)

        hsvcolor = colorID(h,s,v)
        
        #Creating text string to display( Color name and RGB values )
        if(hsvcolor != None):
            text = "{} H={:.0f} S={:.0f} V={:.0f} ({},{})".format(hsvcolor[0].capitalize(), h, s, v, xpos, ypos)
        else:
            text = "{} H={:.0f} S={:.0f} V={:.0f} ({},{})".format("ERROR: NO COLOR FOUND", h, s, v, xpos, ypos)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #for very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

## delete temp jpg file (from pdf if exists)
if pdf_status == True and os.path.exists(img_path):
    os.remove(img_path)
    
cv2.destroyAllWindows()