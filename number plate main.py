import cv2
import pytesseract
import numpy as np
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
my_w =tk.Tk()

my_w.geometry("400x300")
my_w.title('Input file')
my_font=('times',18,'bold')
l1 = tk.Label(my_w,text='Upload file',width=30,font=my_font)
l1.grid(row=1,column=1)
b1 = tk.Button(my_w,text='Upload file',width=10,command=lambda:upload_file())
b1.grid(row=2,column=1)

def upload_file():
    global file_path
    file_path=filedialog.askopenfilename()

#KEEP THE WINDOW OPEN
my_w.mainloop()


name=(os.path.basename(file_path).split('/')[-1])

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
States={"AN":"Andaman and Nicobar","AP":"Andhra Pradesh","AR":"Arunachal Pradesh",
        "AS":"Assam","BR":"Bihar","CH":"Chandigarh","CG":"Chattisgarh"
        ,"DN":"Dadra and Nagar Haveli","DD":"Daman and Diu","DL":"Delhi"
        ,"GA":"Goa","GJ":"Gujarat","HR":"Haryana","HP":"Himachal Pradesh",
        "JK":"Jammu Kashmir","JH":"Jharkhand","KA":"Karnataka","KL":"Kerala",
        "LD":"Lakshadweep","MP":" Madhya Pradesh","MH":"Maharashtra",
        "MN":"Manipur","ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland",
        "OR":"Orissa","PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan",
        "SK":"Sikkim","TN":"Tamil Nadu","TR":"Tripura","UP":"Uttar Pradesh",
        "UK":"Uttrakhand","WB":"West Bengal"}

def plate_num(img_name):
    global read
    img = cv2.imread(img_name)
    #CONVERTING COLOURED IMAGE INTO GREY
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    nplate = cascade.detectMultiScale(gray,1.1,5)
    for (x,y,w,h) in nplate:
        #CROPING THE NUMBER PLATE FROM IMAGE
        a,b = (int(0.02*img.shape[0]),int(0.025*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b, :]
        #IMAGE PROCESSING USING OBJECT CHARACTER RECOGNITION(OCR)
        kernel = np.ones((1,1),np.uint8)
        plate = cv2.dilate(plate, kernel, iterations=1)
        plate = cv2.erode(plate, kernel, iterations=1)
        plate_gray= cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
        (thresh,plate) = cv2.threshold(plate_gray, 127, 255,cv2.THRESH_TOZERO)

        read= pytesseract.image_to_string(plate)
        number=read
        if(read[0:1]=="-"):
            state = read[1:3]
            number = read[1:13]
        else:
            state= read[0:2]
            
        try:
            print("The State from where car belongs to is:",States[state])
          
        except:
            print("State not recognised")
        print(read[1:13])
        cv2.rectangle(img,(x,y-10),(x+w,y+h),(51,51,255), 2)
        cv2.rectangle(img,(x,y-40),(x+w,y),(51,51,255),-1)
        cv2.putText(img,number,(x,y-10),cv2.FONT_HERSHEY_COMPLEX,0.8,(222,55,89),2)
        cv2.imshow('Plate',plate)

#SHOWING THE RESULT
    cv2.imshow('Result',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

plate_num(name)       





        
        
        
        
    
        
        






