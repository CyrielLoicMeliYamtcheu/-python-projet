#coding:utf-8

import io
import socket
import struct
#from PIL import Image
import matplotlib.pyplot as pl
import tkinter.messagebox
import tkinter.filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import tkinter as tk
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
from PIL import Image
from PIL import ImageTk
import numpy as np
from pylab import *




##def imageOpen():
##    global fenetre, myimage
##    
##    frame_form=Frame(fenetre,bg='#9999FF')
##    
##    canvas = Canvas(frame_form,width = 100,height = 100,highlightthickness = 0)
##    
##    #myimage = ImageTk.PhotoImage(file = 'icone.bmp')
##    canvas.config(height = myimage.height(), width = myimage.width())
##    canvas.create_image(0,0,image = myimage, anchor = NW)
##    canvas.pack()
##    frame_form.pack(padx = 20, pady = 20)

def fen(photo):

        
    #creation de la fenetre
    fenetre=Tk()
    fenetre.title("Mon application")
    fenetre.geometry("820x580")
    fenetre.minsize(580,460)
    fenetre.config(background='#9999FF')

    #creation d'un menu
    menu=Menu(fenetre)

    #creation d'un premier menu
    file_menu=Menu(menu,tearoff=0)
    file_menu.add_command(label="RVB")
    file_menu.add_command(label="Hyperspectral")
    menu.add_cascade(label="Type d'image",menu=file_menu)

    #creation du second menu
    file_menu1=Menu(menu,tearoff=0)
    file_menu1.add_command(label="Individuelle")
    file_menu1.add_command(label="Groupee")
    menu.add_cascade(label="Selection d'image",menu=file_menu1)

    #creation du troisieme menu
    file_menu2=Menu(menu,tearoff=0)
    file_menu2.add_command(label="Help?")
    file_menu2.add_command(label="Quitter",command=fenetre.quit)
    menu.add_cascade(label="Action",menu=file_menu2)

    #configuration du menu et affichage sur la fenetre
    fenetre.config(menu=menu)

    #creation de la frame qui contiendra le label title
    frame_title=Frame(fenetre,bg='#99FF99') 

    #creation du label title
    label_title=Label(frame_title,text="Application de diagnostic des plantes de mais",font=("TimeNewRoman",20,"italic"),bg='#99FF99',fg='#003333')

    #chargement du label title
    label_title.pack(ipady=10,ipadx=10)

    #chargement de la frame dans la fenetre
    frame_title.pack(fill=X)

    #creation de la frame qui contiendra mes boutons
    frame_form=Frame(fenetre,bg='#9999FF')

    canvas = Canvas(frame_form,width = 100,height = 100,bg = 'black',highlightthickness = 0)
    
    img = PhotoImage(width = 100, height = 100)
    myimage = ImageTk.PhotoImage(file = photo)
    canvas.config(height = myimage.height(), width = myimage.width())
    canvas.create_image(0,0,image = myimage, anchor = NW)
    canvas.pack()
    frame_form.pack(padx = 20, pady = 20, side = "top")


    #creation du formulaire
##    label_nom=Label(frame_form,text="Nom",font=("TimeNewRoman",14,"italic"),bg='#99FF99',fg='white')
##    label_nom.pack(padx = 10, pady = 10)
##
##    textfield=Entry(frame_form,width=20)
##    textfield.pack(padx = 10,pady = 10)
##
##    #textfield.grid(row=0,column=1)
##    #creation du premier bouton sur la frame_form
##    bouton_connection=Button(frame_form,text="Connection",font=("TimeNewRoman",14,"italic"),bg='#99FF99',fg='white',command=fen)
##    bouton_connection.pack(padx = 10, pady = 10)
##
##    bouton_connection=Button(frame_form,text="Load Image",font=("TimeNewRoman",14,"italic"),
##                             bg='#99FF99',fg='white')
##    bouton_connection.pack(padx = 10, pady = 10)
##
##    #bouton_connection.grid(row=1,column=0)
##
##    #chargement du frame dans la fenetre
##    frame_form.pack(side="right")

    #affichage de la fenetre
    fenetre.mainloop()




server_socket = socket.socket()
server_socket.bind(('192.168.43.94', 8000))  # ADD IP HERE
server_socket.listen(0)
buffer_stream = []
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

try:
    img = None
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0) # recherche l'image donnee dans le fichier de sequence
        
        image = Image.open(image_stream)
        image.load()
        buffer_stream.append(image)
        #fen(image_stream)
        
        if img is None:
            img = pl.imshow(image)
        else:
            img.set_data(image)
        
        pl.pause(0.01)
        pl.draw() # redessine la figure courante

        
       
        print('Image is %dx%d' % image.size)
        image.verify()
        print('Image is verified')
finally:
    connection.close()
    server_socket.close()

pl.close()

buffer_image = []

print("contenu du buffer {} ".format(buffer_stream))
for i, image in enumerate(buffer_stream):
    image.save("photo{}.jpeg".format(i))
    #fen("photo{}.jpeg".format(i))
    buffer_image.append("photo{}.jpeg".format(i))

compteur = -1    
print(buffer_image)


def inverser_valeur(tab):
    taille = len(tab)
    for i in range(0,taille):
        tab[i] = 255 - tab[i]


def inverser_composantRVB(filename,filename_output):

    image = img.open(filename)
    image_rvb = image.convert("RGB")
    data = np.asarray(image)
    i = 0
    red = []
    green = []
    bleu = []

    largeur_image = data.shape[0]
    hauteur_image = data.shape[1]

    for y in range(hauteur_image):
        for x in range(largeur_image):
            r,g,b = image_rvb.getpixel((x,y))
            red.append(r)
            green.append(g)
            bleu.append(b)
            r1 = 255-r
            g1 = 255-g
            b1 = 255-b
            image.putpixel((x,y),(r1,g1,b1))
            #print(" rouge : ", r , " vert : ", g , " bleu : ", b)
            i = i+1
            
    image.save(filename_output)
    #image.show()

    #print(" \n rouge liste : ", red)

    print(" \nvaleur de i est :", i)




def permuter_table(tab1,tab2):
    taille =  len(tab1)
    for i in range(0, taille):
        tmp = tab1[i]
        tab1[i] = tab2[i]
        tab2[i] = tmp
        
def permutation_composanteRVB(filename,filename_output):

    image = img.open(filename)
    image_rvb = image.convert("RGB")
    data = np.asarray(image)
    i = 0
    red = []
    green = []
    bleu = []

    largeur_image = data.shape[0]
    hauteur_image = data.shape[1]

    for y in range(hauteur_image):
        for x in range(largeur_image):
            r,g,b = image_rvb.getpixel((x,y))
            red.append(r)
            green.append(g)
            bleu.append(b)
            r1 = 255-r
            g1 = 255-g
            b1 = 255-b
            permuter_table(r1,g1)
            image.putpixel((x,y),(r1,g1,b1))
            #print(" rouge : ", r , " vert : ", g , " bleu : ", b)
            i = i+1
            
    image.save(filename_output)
    #image.show()

    #print(" \n rouge liste : ", red)

    print(" \nvaleur de i est :", i)


        



#creation de la fenetre
fenetre=Tk()
#N = IntVar()
#global myimage
fenetre.title("Mon application")
fenetre.geometry("720x480")
fenetre.minsize(580,460)
fenetre.config(background='#9999FF')

#creation d'un menu
menu=Menu(fenetre)

#creation d'un premier menu
file_menu=Menu(menu,tearoff=0)
file_menu.add_command(label="RVB")
file_menu.add_command(label="Hyperspectral")
menu.add_cascade(label="Type d'image",menu=file_menu)

#creation du second menu
file_menu1=Menu(menu,tearoff=0)
file_menu1.add_command(label="Individuelle")
file_menu1.add_command(label="Groupee")
menu.add_cascade(label="Selection d'image",menu=file_menu1)

#creation du troisieme menu
file_menu2=Menu(menu,tearoff=0)
file_menu2.add_command(label="Help?")
file_menu2.add_command(label="Quitter",command=fenetre.quit)
menu.add_cascade(label="Action",menu=file_menu2)

#configuration du menu et affichage sur la fenetre
fenetre.config(menu=menu)

#creation de la frame qui contiendra le label title
frame_title=Frame(fenetre,bg='#99FF99') 

#creation du label title
label_title=Label(frame_title,text="Application de diagnostic des plantes de mais",font=("TimeNewRoman",20,"italic"),bg='#99FF99',fg='#003333')

#chargement du label title
label_title.pack(ipady=10,ipadx=10)

#chargement de la frame dans la fenetre
frame_title.pack(fill=X)

#creation de la frame qui contiendra mes boutons
frame_form=Frame(fenetre,bg='#9999FF')

canvas = Canvas( width = 100,height = 100,bg = '#9999FF',highlightthickness = 0)


##img = ImageTk.PhotoImage(file = "photo0.jpeg", width = 50, height = 50)
##item = canvas.create_image(0,0,image = img, anchor = NW)
canvas.pack()

#myimage = ImageTk.PhotoImage(file = 'icone.bmp')

#canvas.config(height = myimage.height(), width = myimage.width())
#canvas.create_image(0,0,image = myimage, anchor = NW)
#canvas.pack()
#frame_form.pack(padx = 20, pady = 20, side = "top")

def changer_photo():
    
    global compteur,buffer_image
    compteur = compteur + 1
    print("La valeur du compteur est : " , compteur)
    #i = compteur
    #buffer_stream = test()
    
    taille_buffer_stream = len(buffer_image)
    if compteur < taille_buffer_stream:
        canvas.delete("all")
        #global item
        photo = ImageTk.PhotoImage(file = buffer_image[compteur])
        canvas.create_image(0,0,image = photo, anchor = NW)
        canvas.image = photo
        return buffer_image[compteur]
    else:
        print("termine")
        compteur = -1
        return 0
        
            
    
def changer_photo2():
    canvas.delete("all")
    #global item
    photo = ImageTk.PhotoImage(file = "photo0.jpeg")
    canvas.create_image(0,0,image = photo, anchor = NW)
    canvas.image = photo


frame_form.pack(padx = 10, pady = 10)

canvas1 = Canvas( width = 100,height = 100,bg = '#9999FF',highlightthickness = 0)
canvas1.pack()

def permutation_composanteRVB1():

    filename = changer_photo()
    image = Image.open(filename)
    image_rvb = image.convert("RGB")
    data = np.asarray(image)
    i = 0
    red = []
    green = []
    bleu = []

    largeur_image = data.shape[0]
    hauteur_image = data.shape[1]

    for y in range(hauteur_image):
        for x in range(largeur_image):
            r,g,b = image_rvb.getpixel((x,y))
            red.append(r)
            green.append(g)
            bleu.append(b)
            r1 = 255-r
            g1 = 255-g
            b1 = 255-b
            permuter_table(r1,g1)
            image.putpixel((x,y),(r1,g1,b1))
            #print(" rouge : ", r , " vert : ", g , " bleu : ", b)
            i = i+1
            
    #image.save(filename_output)
    #image.show()
    canvas.delete("all")
    photo = ImageTk.PhotoImage(file = image)
    canvas1.create_image(0,0,image = photo, anchor = NW)
    canvas1.image = photo

    #print(" \n rouge liste : ", red)

    #print(" \nvaleur de i est :", i)


def inverser_composantRVB1():

    filename = changer_photo()
    image = Image.open(filename)
    image_rvb = image.convert("RGB")
    data = np.asarray(image)
    i = 0
    red = []
    green = []
    bleu = []

    largeur_image = data.shape[0]
    hauteur_image = data.shape[1]

    for y in range(hauteur_image):
        for x in range(largeur_image):
            r,g,b = image_rvb.getpixel((x,y))
            red.append(r)
            green.append(g)
            bleu.append(b)
            r1 = 255-r
            g1 = 255-g
            b1 = 255-b
            image.putpixel((x,y),(r1,g1,b1))
            #print(" rouge : ", r , " vert : ", g , " bleu : ", b)
            i = i+1

    canvas.delete("all")
    photo = ImageTk.PhotoImage(file = image)
    canvas1.create_image(0,0,image = photo, anchor = NW)
    canvas1.image = photo
       
    #image.save(filename_output)
    #image.show()

    #print(" \n rouge liste : ", red)

    #print(" \nvaleur de i est :", i)



#creation du formulaire
label_nom=Label(frame_form,text="Nom",font=("TimeNewRoman",14,"italic"),bg='#99FF99',fg='white')

label_nom.pack(padx = 10, pady = 10)

textfield=Entry(frame_form,width=20)

textfield.pack(padx = 10,pady = 10)

#textfield.grid(row=0,column=1)

#creation du premier bouton sur la frame_form

b1 = tk.Button(frame_form, text = "Connection",font=("TimeNewRoman",14,"italic"), bg="#99FF99",fg= "white")
b1.pack(padx = 10, pady = 10)

b2 = tk.Button(frame_form,text="Load Image",
                    font=("TimeNewRoman",14,"italic"),
                         bg="#99FF99",fg="white",command=changer_photo)
b2.pack(padx = 10, pady = 10)

b3 = tk.Button(frame_form,text="Load Image2",
                         font=("TimeNewRoman",14,"italic"),
                         bg="#99FF99",fg="white",command=test)

b3.pack(padx = 10, pady = 10)   

b4 = tk.Button(frame_form,text="Traitement",
                         font=("TimeNewRoman",14,"italic"),
                         bg="#99FF99",fg="white",command=permutation_composanteRVB1)

b4.pack(padx = 10, pady = 10)   

b5 = tk.Button(frame_form,text="Inversion_image",
                         font=("TimeNewRoman",14,"italic"),
                         bg="#99FF99",fg="white",command=inverser_composantRVB1)

b5.pack(padx = 10, pady = 10)   



#bouton_connection.grid(row=1,column=0)

#chargement du frame dans la fenetre
frame_form.pack(side="left")

#affichage de la fenetre
fenetre.mainloop()



    
