# %%

# GUI Libraries
import tkinter as tk
import tkinter.messagebox
import customtkinter
import matplotlib.colors as colors

# App libraries
from PIL import Image, ImageEnhance, ImageTk
import cv2
from sitia_lib import sitia
from sitia_db import sitia_db
import pandas as pd
import numpy as np
from tkinter import filedialog as fd
from datetime import datetime
import json
import os



# estados de la app
null = -1
started = 0
detected = 1
classified = 2
routed = 3
executed = 4

class Login:
    def __init__(self, db):
        # Creación de la ventana principal
        self.db = db
        self.root = customtkinter.CTk() # Instancia
        self.root.title("SIT-ia Login") # Título
        carpeta_imagenes = 'imgs'
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "mosca_gera.ico")) # Icono
        self.root.geometry("400x500") # Tamaño de la ventana
        self.root.resizable(False,False) # Bloqueo de redimensión de ventana en alto y ancho
        # Contenido de la ventana principal
        # Carga de la imagen
        
        logo = customtkinter.CTkImage(
            light_image=Image.open((os.path.join(carpeta_imagenes, "img2_dark.png"))), # Imagen modo claro
            dark_image=Image.open((os.path.join(carpeta_imagenes, "img2_light.png"))), # Imagen modo oscuro
            size=(250, 250)) # Tamaño de las imágenes
            
        # Etiqueta para mostrar la imagen
        etiqueta = customtkinter.CTkLabel(master=self.root,
                               image=logo,
                               text="")
        etiqueta.pack(pady=15)
         # Campos de texto
        # Usuario
        customtkinter.CTkLabel(self.root, text="User").pack()
        self.usuario = customtkinter.CTkEntry(self.root)
        self.usuario.insert(0, "Name")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack()

        # Contraseña
        customtkinter.CTkLabel(self.root, text="Password").pack()
        ####################### CORRECCION
        self.contrasena = customtkinter.CTkEntry(self.root, show="*")
        ####################### CORRECCION
        self.contrasena.insert(0, "*******")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, 'end'))
        self.contrasena.pack()
        #Botón de envío
        customtkinter.CTkButton(self.root, text="Enter", command=self.validar).pack()
        # Bucle de ejecución
        self.root.mainloop()

    def validar(self):
        self.usr = self.usuario.get()
        pwd = self.contrasena.get()
        self.id = self.db.check_userPwd(self.usr, pwd)

        if self.id<0:
            customtkinter.CTkLabel(self.root, text="User or password incorrect.").pack()
        else:
            customtkinter.CTkLabel(self.root, text=f"Hola, {self.usr}. please wait...").pack()
            self.root.destroy()

class Config:
    def __init__(self) -> None:
        self.root = customtkinter.CTk() # Instancia
        self.root.title("configuration") # Título
        self.root.geometry("940x900") # Tamaño de la ventana
        self.root.resizable(False,False) # Bloqueo de redimensión de ventana en alto y ancho

        self.root.grid_columnconfigure((0, 1, 2), weight = 0)    
        self.root.grid_rowconfigure((0,1,2), weight=0)           
        self.root.grid_rowconfigure(3, weight=0)           


        f = open('sitia_conf.json', "r")
        self.cfg = json.load(f)
        f.close()

        #self.cfg.classify.model

        i = 20
        d = 32
        x0 = 200
        w = 80
        h0 = 300
        h1 = 170
        h2 = 300
        f2 = customtkinter.CTkFont(size=10)
        f1 = customtkinter.CTkFont(size=11, weight="bold")

        # IMAGENES
        panel1 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h0)
        panel1.grid(row=0, column=0, padx=(10,5), pady=(10,5))
        customtkinter.CTkLabel(panel1, text="IMÁGENES",font=f1).place(x=10, y=10)
        customtkinter.CTkLabel(panel1, text="ANCHO [PX]", font=f2,).place(x=10, y=i+(1*d))
        self.a1 = customtkinter.CTkEntry(panel1, placeholder_text="CTkEntry", width=w)
        self.a1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel1, text="ALTO [PX]", font=f2,).place(x=10, y=i+(2*d))
        self.a2 = customtkinter.CTkEntry(panel1, placeholder_text="CTkEntry", width=w)
        self.a2.place(x=x0, y=i+(2*d))
        customtkinter.CTkLabel(panel1, text="L FINAL PARA IA [PX]", font=f2,).place(x=10, y=i+(3*d))
        self.a3 = customtkinter.CTkEntry(panel1, placeholder_text="HOLA", width=w)
        self.a3.place(x=x0, y=i+(3*d))

        # DETECCION 
        panel3 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h1)
        panel3.grid(row=1, column=0, padx=(10,5), pady=5)
        customtkinter.CTkLabel(panel3, text="DETECCIÓN",font=f1).place(x=10, y=10)
        customtkinter.CTkLabel(panel3, text="UMBRAL", font=f2,).place(x=10, y=i+(1*d))
        self.b1 = customtkinter.CTkEntry(panel3, placeholder_text="CTkEntry", width=w)
        self.b1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel3, text="UMBRAL MIN", font=f2,).place(x=10, y=i+(2*d))
        self.b2 = customtkinter.CTkEntry(panel3, placeholder_text="CTkEntry", width=w)
        self.b2.place(x=x0, y=i+(2*d))
        customtkinter.CTkLabel(panel3, text="UMBRAL MAX", font=f2,).place(x=10, y=i+(3*d))
        self.b3 = customtkinter.CTkEntry(panel3, placeholder_text="CTkEntry",width=w)
        self.b3.place(x=x0, y=i+(3*d))

        # COLORES
        panel6 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h2)
        panel6.grid(row=2, column=0, padx=(10,5), pady=5)
        customtkinter.CTkLabel(panel6, text="Colors", font=f1,).place(x=10, y=10)
        customtkinter.CTkLabel(panel6, text="Detected", font=f2,).place(x=10, y=i+(1*d))
        self.c1 = customtkinter.CTkEntry(panel6, placeholder_text="CTkEntry",  width=w)
        self.c1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel6, text="Out of Range", font=f2,).place(x=10, y=i+(2*d))
        self.c2 = customtkinter.CTkEntry(panel6, placeholder_text="CTkEntry",  width=w)
        self.c2.place(x=x0, y=i+(2*d))
        customtkinter.CTkLabel(panel6, text="Overlap", font=f2,).place(x=10, y=i+(3*d))
        self.c3 = customtkinter.CTkEntry(panel6, placeholder_text="CTkEntry", width=w)
        self.c3.place(x=x0, y=i+(3*d))
        customtkinter.CTkLabel(panel6, text="Male", font=f2,).place(x=10, y=i+(4*d))
        self.c4 = customtkinter.CTkEntry(panel6, placeholder_text="CTkEntry",  width=w)
        self.c4.place(x=x0, y=i+(4*d))
        customtkinter.CTkLabel(panel6, text="Female", font=f2,).place(x=10, y=i+(5*d))
        self.c5 = customtkinter.CTkEntry(panel6, placeholder_text="CTkEntry", width=w)
        self.c5.place(x=x0, y=i+(5*d))

        # BINARIZACIÓN
        panel2 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h0)
        panel2.grid(row=0, column=1, padx=5, pady=(10,5))
        self.radio_var2 = tkinter.IntVar(0)
        customtkinter.CTkLabel(panel2, text="BINARIZACIÓN", font=f1,).place(x=10, y=10)
        customtkinter.CTkLabel(panel2, text="INCREMENTO DE BRILLO", font=f2,).place(x=10, y=i+(1*d))
        self.d1 = customtkinter.CTkEntry(panel2, placeholder_text="CTkEntry", width=w)
        self.d1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel2, text="GAUSSIAN BLUR", font=f2,).place(x=10, y=i+(2*d))
        self.d2 = customtkinter.CTkEntry(panel2, placeholder_text="CTkEntry",width=w)
        self.d2.place(x=x0, y=i+(2*d))
        customtkinter.CTkLabel(panel2, text="LIMITE INFERIOR", font=f2,).place(x=10, y=i+(3*d))
        self.d3 = customtkinter.CTkEntry(panel2, placeholder_text="CTkEntry", width=w)
        self.d3.place(x=x0, y=i+(3*d))
        customtkinter.CTkLabel(panel2, text="LIMITE SUPERIOR", font=f2,).place(x=10, y=i+(4*d))
        self.d4 = customtkinter.CTkEntry(panel2, placeholder_text="CTkEntry",  width=w)
        self.d4.place(x=x0, y=i+(4*d))
        customtkinter.CTkLabel(panel2, text="ITERACIONES DILATACION", font=f2,).place(x=10, y=i+(5*d))
        self.d5 = customtkinter.CTkEntry(panel2, placeholder_text="CTkEntry", width=w)
        self.d5.place(x=x0, y=i+(5*d))
        customtkinter.CTkLabel(panel2, text="ITERACIONES EROSION", font=f2,).place(x=10, y=i+(6*d))
        self.d6 = customtkinter.CTkEntry(panel2, placeholder_text="CTkEntry", width=w)
        self.d6.place(x=x0, y=i+(6*d))
        customtkinter.CTkLabel(panel2, text="TAMAÑO DEL KERNEL", font=f2,).place(x=10, y=i+(7*d))
        self.d7 = customtkinter.CTkEntry(panel2, placeholder_text="CTkEntry",  width=w)
        self.d7.place(x=x0, y=i+(7*d))

        
        # LASER
        panel4 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h1)
        panel4.grid(row=1, column=1, padx=5, pady=5)
        self.radio_var = tkinter.IntVar(0)
        customtkinter.CTkLabel(panel4, text="LASER", font=f1).place(x=10, y=10)
        self.e1 = customtkinter.CTkEntry(panel4, placeholder_text="CTkEntry", width=w)
        self.e1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel4, text="POSICION INICIAL X", font=f2,).place(x=10, y=i+(1*d))
        self.e2 = customtkinter.CTkEntry(panel4, placeholder_text="CTkEntry", width=w)
        self.e2.place(x=x0, y=i+(2*d))
        customtkinter.CTkLabel(panel4, text="POSICION INICIAL Y", font=f2,).place(x=10, y=i+(2*d))
        
        # CHECKBOX MEDIO
        panel7 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h2)
        panel7.grid(row=2, column=1, padx=5, pady=5)
        self.cb1 = customtkinter.CTkCheckBox(panel7, text="GRABAR MODIFICACIONES POR SEPARADO", font=f2)
        self.cb1.place(x=10, y=i+(0*d))

        # OJOS
        panel8 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h0)
        panel8.grid(row=0, column=2, padx=(5,10), pady=(10,5))
        self.radio_var = tkinter.IntVar(0)
        customtkinter.CTkLabel(panel8, text="OJOS", font=f1,).place(x=10, y=10)
        self.ff1 = customtkinter.CTkEntry(panel8, placeholder_text="CTkEntry", width=w)
        self.ff1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel8, text="COLOR 1", font=f2,).place(x=10, y=i+(1*d))
        self.ff2 = customtkinter.CTkEntry(panel8, placeholder_text="CTkEntry", width=w)
        self.ff2.place(x=x0, y=i+(2*d))
        customtkinter.CTkLabel(panel8, text="COLOR 2", font=f2,).place(x=10, y=i+(2*d))

        # TARGET PLUS
        panel9 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h1)
        panel9.grid(row=1, column=2, padx=(5,10), pady=5)
        self.radio_var = tkinter.IntVar(0)
        customtkinter.CTkLabel(panel9, text="TARGET PLUS", font=f1,).place(x=10, y=10)
        self.g1 = customtkinter.CTkEntry(panel9, placeholder_text="CTkEntry", width=w)
        self.g1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel9, text="KERNEL", font=f2,).place(x=10, y=i+(1*d))
        self.g2 = customtkinter.CTkEntry(panel9, placeholder_text="CTkEntry", width=w)
        self.g2.place(x=x0, y=i+(2*d))
        customtkinter.CTkLabel(panel9, text="ITERACIONES", font=f2,).place(x=10, y=i+(2*d))

        # CLASIFICACION
        panel5 = customtkinter.CTkFrame(self.root, corner_radius=5, width=300, height=h2)
        panel5.grid(row=2, column=2, padx=(5,10), pady=5)
        self.radio_var = tkinter.IntVar(0)
        customtkinter.CTkLabel(panel5, text="CLASIFICACIÓN", font=f1,).place(x=10, y=10)
        self.h1 = customtkinter.CTkEntry(panel5, placeholder_text="CTkEntry", width=w)
        self.h1.place(x=x0, y=i+(1*d))
        customtkinter.CTkLabel(panel5, text="UMBRAL DE CLASIFICACION", font=f2,).place(x=10, y=i+(1*d))
        customtkinter.CTkLabel(panel5, text="ALGORITMO OPTIMIZACION DE TRAYECTORIA", font=f2,).place(x=10, y=i+(2*d))
        customtkinter.CTkRadioButton(panel5, text="SIN OPTIMIZACIÓN", font=f2, command=self.radiobutton_event, variable= self.radio_var, value=1,).place(x=10, y=i+(3*d))
        customtkinter.CTkRadioButton(panel5, text="GREEDY", font=f2, command=self.radiobutton_event, variable= self.radio_var, value=2).place(x=10, y=i+(4*d))
        customtkinter.CTkRadioButton(panel5, text="LOCAL SEARCH", font=f2, command=self.radiobutton_event, variable= self.radio_var, value=3).place(x=10, y= i+(5*d))
        customtkinter.CTkRadioButton(panel5, text="ANT COLONY OPTIMIZATION", font=f2, command=self.radiobutton_event, variable= self.radio_var, value=4).place(x=10, y=i+(6*d))
        self.cb2 = customtkinter.CTkCheckBox(panel5, text="OPTIMIZAR EN CADA CAMBIO", font=f2)
        self.cb2.place(x=10, y=i+(7*d))

        # SET VALUES
        self.set_values()

        customtkinter.CTkButton(self.root, text="Valores predeterminados", command=self.default_values, width=200, fg_color="grey").grid(row=3, column=0, padx=20, pady=(20, 10), sticky = "sw")
        customtkinter.CTkButton(self.root, text="Cancelar", command=self.cancel, width=100, fg_color="red").grid(row=3, column=2, padx=(20,140), pady=(20, 10), sticky = "se")
        customtkinter.CTkButton(self.root, text="Grabar", command=self.save_config, width=100,fg_color="green").grid(row=3, column=2, padx=20, pady=(20, 10), sticky = "se")
    
        self.root.mainloop()

    def radiobutton_event(self):
        print("radiobutton toggled, current value:", self.radio_var.get())

    def save_config(self):

        # GET VALUES

        self.cfg["usr_cfg"]["width"] = self.a1.get()
        self.cfg["usr_cfg"]["height"] = self.a2.get()
        self.cfg["usr_cfg"]["img_size"] = self.a3.get()

        self.cfg["usr_cfg"]["threshold_1"] = self.b1.get()
        self.cfg["usr_cfg"]["threshold_min"] = self.b2.get()
        self.cfg["usr_cfg"]["threshold_max"] = self.b3.get()

        self.cfg["usr_cfg"]["color_detected"] = self.c1.get()
        self.cfg["usr_cfg"]["color_out_of_bounds"] = self.c2.get()
        self.cfg["usr_cfg"]["color_overlapped"] = self.c3.get()
        self.cfg["usr_cfg"]["color_male"] = self.c4.get()
        self.cfg["usr_cfg"]["color_female"] = self.c5.get()

        self.cfg["usr_cfg"]["bin_bright"] = self.d1.get()
        self.cfg["usr_cfg"]["gaussian_blur"] = self.d2.get()
        self.cfg["usr_cfg"]["lower_limit"] = self.d3.get()
        self.cfg["usr_cfg"]["upper_limit"] = self.d4.get()
        self.cfg["usr_cfg"]["dilation_int"] = self.d5.get()
        self.cfg["usr_cfg"]["erosion_int"] = self.d6.get()
        self.cfg["usr_cfg"]["kernel_size"] = self.d7.get()

        self.cfg["usr_cfg"]["laser_x0"] = self.e1.get()
        self.cfg["usr_cfg"]["laser_y0"] = self.e2.get()

        self.cfg["usr_cfg"]["lower_color_eyes"] = self.ff1.get()
        self.cfg["usr_cfg"]["upper_color_eyes"] = self.ff2.get()

        self.cfg["usr_cfg"]["target_kernel"] = self.g1.get()
        self.cfg["usr_cfg"]["target_int"] = self.g2.get()

        self.cfg["usr_cfg"]["classify_threshold"] = self.h1.get()
        
        self.cfg["usr_cfg"]["auto_save"] = self.cb1.get()
        self.cfg["usr_cfg"]["alwats_opt"] = self.cb2.get()

        self.cfg["usr_cfg"]["route_opt"] = self.radio_var.get()
        

        f = open('sitia_conf.json', "w")
        json.dump(self.cfg, f)
        f.close()

        self.root.destroy()

    def set_values(self):

        self.a1.delete(0,100)
        self.a2.delete(0,100)
        self.a3.delete(0,100)
        self.b1.delete(0,100)
        self.b2.delete(0,100)
        self.b3.delete(0,100)
        self.c1.delete(0,100)
        self.c2.delete(0,100)
        self.c3.delete(0,100)
        self.c4.delete(0,100)
        self.c5.delete(0,100)
        self.d1.delete(0,100)
        self.d2.delete(0,100)
        self.d3.delete(0,100)
        self.d4.delete(0,100)
        self.d5.delete(0,100)
        self.d6.delete(0,100)
        self.d7.delete(0,100)
        self.e1.delete(0,100)
        self.e2.delete(0,100)
        self.ff1.delete(0,100)
        self.ff2.delete(0,100)
        self.g1.delete(0,100)
        self.g2.delete(0,100)
        self.h1.delete(0,100)
        

        self.a1.insert(0, self.cfg["usr_cfg"]["width"])
        self.a2.insert(0, self.cfg["usr_cfg"]["height"])
        self.a3.insert(0, self.cfg["usr_cfg"]["img_size"])

        self.b1.insert(0, self.cfg["usr_cfg"]["threshold_1"])
        self.b2.insert(0, self.cfg["usr_cfg"]["threshold_min"])
        self.b3.insert(0, self.cfg["usr_cfg"]["threshold_max"])

        self.c1.insert(0, self.cfg["usr_cfg"]["color_detected"])
        self.c2.insert(0, self.cfg["usr_cfg"]["color_out_of_bounds"])
        self.c3.insert(0, self.cfg["usr_cfg"]["color_overlapped"])
        self.c4.insert(0, self.cfg["usr_cfg"]["color_male"])
        self.c5.insert(0, self.cfg["usr_cfg"]["color_female"])

        self.d1.insert(0, self.cfg["usr_cfg"]["bin_bright"])
        self.d2.insert(0, self.cfg["usr_cfg"]["gaussian_blur"])
        self.d3.insert(0, self.cfg["usr_cfg"]["lower_limit"])
        self.d4.insert(0, self.cfg["usr_cfg"]["upper_limit"])
        self.d5.insert(0, self.cfg["usr_cfg"]["dilation_int"])
        self.d6.insert(0, self.cfg["usr_cfg"]["erosion_int"])
        self.d7.insert(0, self.cfg["usr_cfg"]["kernel_size"])

        self.e1.insert(0, self.cfg["usr_cfg"]["laser_x0"])
        self.e2.insert(0, self.cfg["usr_cfg"]["laser_y0"])

        self.ff1.insert(0, self.cfg["usr_cfg"]["lower_color_eyes"])
        self.ff2.insert(0, self.cfg["usr_cfg"]["upper_color_eyes"])

        self.g1.insert(0, self.cfg["usr_cfg"]["target_kernel"])
        self.g2.insert(0, self.cfg["usr_cfg"]["target_int"])

        self.h1.insert(0, self.cfg["usr_cfg"]["classify_threshold"])
        
        if self.cfg["usr_cfg"]["auto_save"]==1: 
            self.cb1.select()
        else: self.cb1.deselect()

        if self.cfg["usr_cfg"]["alwats_opt"]==1: 
            self.cb2.select()
        else: self.cb2.deselect()

        self.radio_var.set(value=self.cfg["usr_cfg"]["route_opt"])
        
    def default_values(self):
        self.cfg["usr_cfg"]= self.cfg["default"]["usr_cfg"]
        self.set_values()

    def cancel(self):
        self.root.destroy()

class App(customtkinter.CTk):

    def __init__(self, db, usr, id):
        
        super().__init__()

        self.db = db
        self.usr = usr
        self.id = id

        # reads configuration file
        f = open('sitia_conf.json', "r")
        self.cfg = json.load(f)
        f.close()
        
        # create drosophila IA class
        self.ds = sitia(self.cfg["classify_model"], self.cfg)
        
        
        # configure app
        self.title("SIT-ia")
        self.state('zoomed')
        #self.attributes('-fullscreen', True)
        #self.iconbitmap('.ico')

        # configure grid main layout (3x1)
        self.grid_columnconfigure(0, weight = 0)    # column 1
        self.grid_columnconfigure(1, weight = 1)    # column 2
        self.grid_columnconfigure(2, weight = 0)    # column 3
        self.grid_rowconfigure(0, weight=1)         # row 0

        # set left panel
        self.set_left_panel()

        # set middle panel
        self.set_middle_panel()
                
        # set right panel
        self.set_right_panel()

        # configuration parameters
        self.set_params()

        # screen update
        self.update_midPanel_info()
        self.set_screen_buttons()

    def set_params(self):

        # set theme and color options
        customtkinter.set_appearance_mode(self.cfg["appearance_mode"])          # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme(self.cfg["color_theme"])          # Themes: "blue" (standard), "green", "dark-blue"

        self.status = null
        self.selected_id = -1
        self.z = False

        if self.cfg["checkbox"]["bbox"]==1: self.cb_bbox.toggle()
        if self.cfg["checkbox"]["objn"]==1: self.cb_objn.toggle()
        if self.cfg["checkbox"]["conf"]==1: self.cb_conf.toggle()
        if self.cfg["checkbox"]["targ"]==1: self.cb_targ.toggle()
        if self.cfg["checkbox"]["rout"]==1: self.cb_rout.toggle()

        self.cb_clas.configure(state="disabled")
        self.cb_fema.configure(state="disabled")
        self.cb_male.configure(state="disabled")
        self.cb_over.configure(state="disabled")
        self.cb_outs.configure(state="disabled")

    def set_left_panel(self):

        # create and locate the left panel frame
        self.left_panel = customtkinter.CTkFrame(self, corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="news")   
        self.left_panel.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=0)                     
        self.left_panel.grid_rowconfigure(9, weight=1)
        self.left_panel.grid_rowconfigure(10, weight=1)
        
        # get logo image
        image = "./imgs/mosca_gera.png"
        
        # left panel widgets
        print(image)
        self.logo_image = customtkinter.CTkImage(Image.open(image), size=(26, 26))
        # DA ERROR EN MAC *** self.logo_label = customtkinter.CTkLabel(self.left_panel, text="  SIT-IA", image=self.logo_image, compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.take_btn = customtkinter.CTkButton(self.left_panel, text="Take photo", command=self.take_image)
        self.detect_btn = customtkinter.CTkButton(self.left_panel, text = "Detect", command=self.detect)
        self.classify_btn = customtkinter.CTkButton(self.left_panel, text = "Classify", command=self.classify)
        self.route_btn = customtkinter.CTkButton(self.left_panel, text = "Path", command=self.route)
        self.process_btn = customtkinter.CTkButton(self.left_panel, text = "Process", command=self.laser_process)
        self.clear_btn = customtkinter.CTkButton(self.left_panel, text = "Delete", command=self.clear, hover_color="#EA999E", fg_color="#C46872")
        self.load_btn = customtkinter.CTkButton(self.left_panel, text="Upload photo", command=self.image_load)
        self.config_btn = customtkinter.CTkButton(self.left_panel, text = "Configuration", command=self.config)

        # left panel widget position
        # DA ERROR EN MAC *** self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky = "new")
        self.take_btn.grid(row=2, column=0, padx=20, pady=10, sticky = "new")
        self.detect_btn.grid(row=3, column=0, padx=20, pady=10, sticky = "new")
        self.classify_btn.grid(row=4, column=0, padx=20, pady=10, sticky = "new") 
        self.route_btn.grid(row=5, column=0, padx=20, pady=10, sticky = "new")
        self.process_btn.grid(row=6, column=0, padx=20, pady=10, sticky = "new")
        self.clear_btn.grid(row=7, column=0, padx=20, pady=10, sticky = "new")
        
        self.load_btn.grid(row=9, column=0, padx=20, pady=10, sticky = "sew")        
        self.config_btn.grid(row=10, column=0, padx=20, pady=(20,20), sticky = "sew")

    def set_middle_panel(self):

        # create and locate the midle panel 
        self.mid_panel = customtkinter.CTkFrame(self, corner_radius=0)
        self.mid_panel.grid(row=0, column=1, sticky="nsew")   
        self.mid_panel.grid_columnconfigure(0, weight = 1)
        self.mid_panel.grid_rowconfigure(0, weight = 0) 
        self.mid_panel.grid_rowconfigure(1, weight = 1)
        self.mid_panel.grid_rowconfigure(2, weight = 0)
        self.mid_panel.grid_rowconfigure(3, weight = 0) 

        # image title
        self.image_title = customtkinter.CTkLabel(self.mid_panel, text="[sin imagen]", text_color="grey")
        self.image_title.grid(row=0, column=0, padx=(10, 10), pady=(30, 5), sticky="nw")

        # main image area
        self.main_image = customtkinter.CTkLabel(self.mid_panel, text="", bg_color="#5E5E5E")
        self.main_image.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")
        # Asocia la función de click
        self.main_image.bind("<Button-1>", self.left_click_img)
        self.main_image.bind("<Double-Button-1>", self.doble_left_click_img)



        # zoom

        
        zoom_img = customtkinter.CTkImage(Image.open('imgs/zoom-in.png').resize((30,30)))
        #zoom_img = customtkinter.CTkImage(Image.open('imgs/zoom-in.png').resize((30,30), Image.ANTIALIAS))
        # DA ERROR EN MAC *** self.zoom = customtkinter.CTkButton(self.main_image, image=zoom_img, text="", command=self.zoom, fg_color="white", width=30, height=30, corner_radius=1, hover=False, border_width=1, border_color="grey51")
        # DA ERROR EN MAC *** self.zoom.place(in_=self.main_image, rely=0.99, relx=0.99, anchor = "se")


        # information panel
        self.information_panel = customtkinter.CTkFrame(self.mid_panel, fg_color="black")
        self.information_panel.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.information_panel.grid_columnconfigure(0, weight=1)
        self.information_panel.grid_columnconfigure(1, weight=1)
        self.information_panel.grid_columnconfigure(2, weight=1)
        self.information_panel.grid_columnconfigure(3, weight=1)
        self.information_panel.grid_columnconfigure(4, weight=1)
        self.information_panel.grid_columnconfigure(5, weight=1)
        self.information_panel.grid_columnconfigure(6, weight=1)
        self.information_panel.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        # information widgets
        self.label_11 = customtkinter.CTkLabel(master=self.information_panel, text="State", anchor="nw")
        self.label_12 = customtkinter.CTkLabel(master=self.information_panel, text="Detected", anchor="nw")
        self.label_13 = customtkinter.CTkLabel(master=self.information_panel, text="To Classify", anchor="nw")
        self.label_14 = customtkinter.CTkLabel(master=self.information_panel, text="Overlapped", anchor="nw")
        ######## CORRECCION
        self.label_15 = customtkinter.CTkLabel(master=self.information_panel, text="Out of range/omitted", anchor="nw")
        ######## CORRECCION
        self.label_status =                 customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)
        self.label_objects_count =          customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)
        self.label_objects_to_classify =    customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)
        self.label_objects_overlaped =      customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)
        self.label_objects_outside1 =       customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)
        

        self.cOverlap = tuple([int(255*x) for x in colors.hex2color(self.cfg["usr_cfg"]["color_overlapped"])])
        self.cOut = tuple([int(255*x) for x in colors.hex2color(self.cfg["usr_cfg"]["color_out_of_bounds"])])
        self.cDetected = tuple([int(255*x) for x in colors.hex2color(self.cfg["usr_cfg"]["color_detected"])])


        self.cb_clas = customtkinter.CTkCheckBox(master=self.information_panel, text="", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, hover=False, checkmark_color='#%02x%02x%02x' % self.cDetected, bg_color="black", fg_color='#%02x%02x%02x' % self.cDetected, command=self.checkbox_update)
        self.cb_over = customtkinter.CTkCheckBox(master=self.information_panel, text="", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, hover=False, checkmark_color='#%02x%02x%02x' % self.cOverlap, bg_color="black", fg_color='#%02x%02x%02x' % self.cOverlap, command=self.checkbox_update)
        self.cb_outs = customtkinter.CTkCheckBox(master=self.information_panel, text="", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, hover=False, checkmark_color='#%02x%02x%02x' % self.cOut, bg_color="black", fg_color='#%02x%02x%02x' % self.cOut, command=self.checkbox_update)

        self.label_21 = customtkinter.CTkLabel(master=self.information_panel, text="Classifieds", anchor="nw")
        self.label_22 = customtkinter.CTkLabel(master=self.information_panel, text="No Classifieds", anchor="nw")        
        self.label_23 = customtkinter.CTkLabel(master=self.information_panel, text="Males", anchor="nw")
        self.label_24 = customtkinter.CTkLabel(master=self.information_panel, text="Females", anchor="nw")
        self.label_25 = customtkinter.CTkLabel(master=self.information_panel, text="Individuals to be prosecuted", anchor="nw")

        self.cMale = tuple([int(255*x) for x in colors.hex2color(self.cfg["usr_cfg"]["color_male"])])
        self.cFemale = tuple([int(255*x) for x in colors.hex2color(self.cfg["usr_cfg"]["color_female"])])

        self.cb_male = customtkinter.CTkCheckBox(master=self.information_panel, text="", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, hover=False, bg_color="black", fg_color='#%02x%02x%02x' % self.cMale, checkmark_color='#%02x%02x%02x' % self.cMale, command=self.checkbox_update)
        self.cb_fema = customtkinter.CTkCheckBox(master=self.information_panel, text="", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, hover=False, bg_color="black", fg_color='#%02x%02x%02x' % self.cFemale, checkmark_color='#%02x%02x%02x' % self.cFemale, command=self.checkbox_update)
        
        self.label_objects_classified = customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)
        self.label_objects_not_classified = customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)        
        self.label_machos = customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw",  width=100)
        self.label_hembras = customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)
        self.label_objects_to_process = customtkinter.CTkLabel(master=self.information_panel, text="-", anchor="nw", width=100)


        self.cb_bbox = customtkinter.CTkCheckBox(master=self.information_panel, text="Box", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, checkmark_color="grey", hover=False, bg_color="black", fg_color="grey",  command=self.checkbox_update)
        self.cb_objn = customtkinter.CTkCheckBox(master=self.information_panel, text="ID", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, checkmark_color="grey", hover=False, bg_color="black", fg_color="grey", command=self.checkbox_update)
        self.cb_conf = customtkinter.CTkCheckBox(master=self.information_panel, text="Precision", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, checkmark_color="grey", hover=False, bg_color="black", fg_color="grey", command=self.checkbox_update)
        self.cb_targ = customtkinter.CTkCheckBox(master=self.information_panel, text="center of mass", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, checkmark_color="grey", hover=False, bg_color="black", fg_color="grey", command=self.checkbox_update)
        self.cb_rout = customtkinter.CTkCheckBox(master=self.information_panel, text="laser path", border_width=1, checkbox_height=10, checkbox_width=20, corner_radius=4, checkmark_color="grey", hover=False, bg_color="black", fg_color="grey",  command=self.checkbox_update)

        self.label_11.grid(row=0, column = 0, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_12.grid(row=1, column = 0, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_13.grid(row=2, column = 0, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_14.grid(row=3, column = 0, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_15.grid(row=4, column = 0, padx=(20, 10), pady=(5, 5), sticky="ew")

        self.label_status.grid(row=0, column = 1, padx=(20, 10), pady=(5, 5), sticky="w")
        self.label_objects_count.grid(row=1, column = 1, padx=(20, 10), pady=(5, 5), sticky="w")
        self.label_objects_to_classify.grid(row=2, column = 1, padx=(20, 10), pady=(5, 5), sticky="w")
        self.label_objects_overlaped.grid(row=3, column = 1, padx=(20, 10), pady=(5, 5), sticky="w")
        self.label_objects_outside1.grid(row=4, column = 1, padx=(20, 10), pady=(5, 5), sticky="w")
        
        self.cb_clas.grid(row=2, column = 2, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.cb_over.grid(row=3, column = 2, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.cb_outs.grid(row=4, column = 2, padx=(20, 10), pady=(5, 5), sticky="ew")

        self.label_21.grid(row=0, column = 3, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_22.grid(row=1, column = 3, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_23.grid(row=2, column = 3, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_24.grid(row=3, column = 3, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_25.grid(row=4, column = 3, padx=(20, 10), pady=(5, 5), sticky="ew")

        self.label_objects_classified.grid(row=0, column = 4, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_objects_not_classified.grid(row=1, column = 4, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_machos.grid(row=2, column = 4, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_hembras.grid(row=3, column = 4, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.label_objects_to_process.grid(row=4, column = 4, padx=(20, 10), pady=(5, 5), sticky="ew")

        self.cb_male.grid(row=2, column = 5, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.cb_fema.grid(row=3, column = 5, padx=(20, 10), pady=(5, 5), sticky="ew")

        self.cb_bbox.grid(row=0, column = 6, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.cb_objn.grid(row=1, column = 6, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.cb_conf.grid(row=2, column = 6, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.cb_targ.grid(row=3, column = 6, padx=(20, 10), pady=(5, 5), sticky="ew")
        self.cb_rout.grid(row=4, column = 6, padx=(20, 10), pady=(5, 5), sticky="ew")


        # LINEA DE CHAT ABAJO
        
        self.entry = customtkinter.CTkEntry(self.mid_panel, placeholder_text="Laser Info")
        self.entry.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

    def zoom(self):
        if self.z:
            self.z = False
            # desactiva boton
            self.zoom.configure(fg_color="white")
            self.main_image.unbind("<Motion>")
        else: 
            self.z = True
            # activa boton
            self.zoom.configure(fg_color="red")
            self.main_image.bind("<Motion>", self.move_zoom)

    def move_zoom(self, event):
            targetX = int((self.scaleX*event.x)-(self.ds.rect/2))
            targetY = int((self.scaleY*event.y)-(self.ds.rect/2))
            if targetX<0:targetX=0
            if targetY<0:targetY=0
            #if targetX>:targetX=
            #if targetY>:targetY=
            self.click_img = self.img_array[targetY:targetY+self.ds.rect, targetX:targetX+self.ds.rect]
            self.image_insect = customtkinter.CTkImage(light_image = Image.fromarray(self.click_img), size=(self.insect_view._current_width, self.insect_view._current_height))
            self.insect_view.configure(image = self.image_insect)
            self.bright_change(self.bright.get())

    def checkbox_update(self):
        # configure check boxes

        self.ds.draw_bbox = (1 if (self.cb_bbox.get()==1) else 0)
        self.ds.draw_objn = (1 if (self.cb_objn.get()==1) else 0)
        self.ds.draw_conf = (1 if (self.cb_conf.get()==1) else 0)
        self.ds.draw_targ = (1 if (self.cb_targ.get()==1) else 0)
        self.ds.draw_rout = (1 if (self.cb_rout.get()==1) else 0) ###
        self.ds.draw_clas = (1 if (self.cb_clas.get()==1) else 0)
        self.ds.draw_over = (1 if (self.cb_over.get()==1) else 0)
        self.ds.draw_outs = (1 if (self.cb_outs.get()==1) else 0)
        self.ds.draw_male = (1 if (self.cb_male.get()==1) else 0)
        self.ds.draw_fema = (1 if (self.cb_fema.get()==1) else 0)
        

        # redibuja la pantalla
        if self.status in (1, 2, 3, 4):
            self.set_image(self.ds.draw_insect_info(self.status))

    def set_right_panel(self):

        # create and locate the right top panel 
        self.right_panel = customtkinter.CTkFrame(self, corner_radius=0)
        self.right_panel.grid(row=0, column=2, sticky="news")   
        self.right_panel.grid_columnconfigure(0, weight = 1)
        self.right_panel.grid_rowconfigure(0, weight = 0) 
        self.right_panel.grid_rowconfigure(1, weight = 0) 
        self.right_panel.grid_rowconfigure(2, weight = 0) 
        self.right_panel.grid_rowconfigure(3, weight = 1) 

        # Usuario

        self.user = customtkinter.CTkLabel(self.right_panel, text=self.usr + " ["+str(self.id)+"]", text_color="white")
        self.user.grid(row=0, column=0, padx=(10, 10), pady=(30, 5), sticky="ne")

        # zoom insect image
        self.insect_view = customtkinter.CTkLabel(self.right_panel, width=300, height=300, text="", bg_color="#5E5E5E")
        self.insect_view.grid(row=1, column=0, pady=(0,0), padx=(0,10), sticky="new")

        self.insect_sex = customtkinter.CTkButton(master=self.insect_view, 
                                                  fg_color="transparent", 
                                                  text="n/a", 
                                                  width=100, 
                                                  height=20,
                                                  border_width=1, 
                                                  #text_color=("gray10", "#DCE4EE"), 
                                                  font=customtkinter.CTkFont(size=10, weight="bold"),
                                                  command=self.change_sex, 
                                                  corner_radius=0,
                                                  state="disabled"
                                                  )
        

        self.insect_sex.place(in_=self.insect_view, 
                              rely=0.92, 
                              relx=0.009)

        self.insect_sex.place_forget()

        # insect data panel
        self.insect_data = customtkinter.CTkFrame(self.right_panel, corner_radius=4)
        self.insect_data.grid(row=2, column=0, sticky="news")   
        self.insect_data.grid_columnconfigure(0, weight = 1)
        self.insect_data.grid_columnconfigure(1, weight = 1)   
        self.insect_data.grid_rowconfigure(0, weight = 1) 
        self.insect_data.grid_rowconfigure(1, weight = 1) 
        self.insect_data.grid_rowconfigure(2, weight = 1) 
        self.insect_data.grid_rowconfigure(3, weight = 1) 
        self.insect_data.grid_rowconfigure(4, weight = 1) 
        self.insect_data.grid_rowconfigure(5, weight = 1) 
        self.insect_data.grid_rowconfigure(6, weight = 1) 


        # botones de siguiente y anterior insecto seleccionado
        self.insect_selection = customtkinter.CTkFrame(self.insect_data, corner_radius=0)
        self.insect_selection.grid(row=0, column=0, sticky="news", columnspan=2)   
        self.insect_selection.grid_columnconfigure(0, weight = 1)
        self.insect_selection.grid_columnconfigure(1, weight = 1)
        self.insect_selection.grid_columnconfigure(2, weight = 1)
        self.insect_selection.grid_columnconfigure(3, weight = 1)
        self.insect_selection.grid_rowconfigure(0, weigh = 1) 

        self.button_left = customtkinter.CTkButton(master=self.insect_selection, fg_color="transparent", text="◁I", width=20, border_width=2, height=40, text_color=("gray10", "#DCE4EE"), command=self.change_move_left)
        self.button_right = customtkinter.CTkButton(master=self.insect_selection, fg_color="transparent", text="I▷", width=20, border_width=2, height=40, text_color=("gray10", "#DCE4EE"), command=self.change_move_right)
        self.button_left.grid (row=0, column=0, padx=(0, 0), pady=(5, 5), sticky="w")        
        self.button_right.grid(row=0, column=3, padx=(10, 10), pady=(5, 5), sticky="e")     



        self.label30 = customtkinter.CTkLabel(self.insect_selection, text="ID")
        self.label30.grid(row=0, column=1, padx=(10, 10), pady=(5, 5),sticky="ew") 

        self.insect_id = customtkinter.CTkLabel(self.insect_selection, text="[no id]", text_color="grey")
        self.insect_id.grid(row=0, column=2, padx=(10, 10), pady=(5, 5), sticky="ew")

        #self.label30 = customtkinter.CTkLabel(self.insect_data, text="ID")
        self.label31 = customtkinter.CTkLabel(self.insect_data, text="State")
        self.label32 = customtkinter.CTkLabel(self.insect_data, text="Precision")
        self.label33 = customtkinter.CTkLabel(self.insect_data, text="Area")
        self.label34 = customtkinter.CTkLabel(self.insect_data, text="Brightness")
               
        self.label31.grid(row=1, column=0, padx=(10, 10), pady=(5, 5),sticky="ew")        
        self.label32.grid(row=2, column=0, padx=(10, 10), pady=(5, 5),sticky="ew")
        self.label33.grid(row=3, column=0, padx=(10, 10), pady=(5, 5),sticky="ew")
        self.label34.grid(row=4, column=0, padx=(10, 10), pady=(5, 5),sticky="ew")
        
        self.insect_status = customtkinter.CTkLabel(self.insect_data, text="-", bg_color="grey")
        self.insect_confidence = customtkinter.CTkLabel(self.insect_data, text="-", bg_color="grey")
        self.a4 = customtkinter.CTkLabel(self.insect_data, text="-", bg_color="grey")
        
        self.bright = customtkinter.CTkSlider(self.insect_data, from_=0, to=2, number_of_steps=255, command=self.bright_change)

        
        self.insect_status.grid     (row=1, column=1, padx=(10, 10), pady=(5, 5),sticky="ew")        
        self.insect_confidence.grid (row=2, column=1, padx=(10, 10), pady=(5, 5),sticky="ew")
        self.a4.grid                (row=3, column=1, padx=(10, 10), pady=(5, 5),sticky="ew")
        self.bright.grid            (row=4, column=1, padx=(10, 10), pady=(5, 5), sticky="ew")

        # botones
        #self.button_change_sex = customtkinter.CTkButton(master=self.insect_data, fg_color="pink", text="Hembra", width=30, border_width=2, text_color=("gray10", "#DCE4EE"), command=self.change_sex)




        self.insect_toolbar = customtkinter.CTkFrame(self.insect_data, corner_radius=0)
        self.insect_toolbar.grid(row=6, column=0, sticky="news", columnspan=2)   
        self.insect_toolbar.grid_columnconfigure(0, weight = 1)
        self.insect_toolbar.grid_columnconfigure(1, weight = 1)
        self.insect_toolbar.grid_columnconfigure(2, weight = 1)
        self.insect_toolbar.grid_columnconfigure(3, weight = 1)
        self.insect_toolbar.grid_rowconfigure(0, weigh = 1) 

        self.button_ommit = customtkinter.CTkButton(master=self.insect_toolbar, fg_color="transparent", text="Ommit", border_width=2, width=80, text_color=("gray10", "#DCE4EE"), command=self.insect_to_ommit)
        self.button_classify = customtkinter.CTkButton(master=self.insect_toolbar, fg_color="transparent", text="Classify", border_width=2, width=80, text_color=("gray10", "#DCE4EE"), command=self.insect_to_classify)
        self.button_eliminar = customtkinter.CTkButton(master=self.insect_toolbar, fg_color="transparent", text="Zap", border_width=2, width=80, text_color=("gray10", "#DCE4EE"), command=self.insect_to_kill)



        #self.button_change_sex.grid(row=6, column=0, padx=(20, 20), pady=(20, 20))
        self.button_ommit.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="w")
        self.button_classify.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="w")
        self.button_eliminar.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="w")

        self.disabled_buttons()

        # boton
        self.main_button_1 = customtkinter.CTkButton(master=self.right_panel, text="Laser connected", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sew")

    def disabled_buttons(self):
        self.button_ommit.configure(state="disabled")
        self.button_classify.configure(state="disabled")
        self.button_left.configure(state="disabled")
        self.button_right.configure(state="disabled")
        self.bright.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.button_eliminar.configure(state="disabled")

    def enabled_buttons(self):
        self.button_ommit.configure(state="normal")

        ####################### CORRECCION
        if self.status == detected: self.button_classify.configure(state="normal")
        

        self.button_left.configure(state="normal")
        self.button_right.configure(state="normal")
        self.bright.configure(state="normal")
        self.button_eliminar.configure(state="normal")

        if self.status == routed:
        
            self.button_classify.configure(state="disabled")
            self.button_eliminar.configure(state="disabled")
            self.button_ommit.configure(state="disabled")
            

        ####################### CORRECCION
 
    def change_move_left(self):
        # cambia el insecto seleccionado a izquierda
        self.selected_id = self.selected_id - 1
        if self.selected_id==0: self.selected_id = app.ds.drosophila.obj_id.max()
        self.left_click_img(null, id = self.selected_id)        

    def change_move_right(self):
        # cambia el insecto seleccionado a izquierda o derecha
        self.selected_id = self.selected_id + 1
        if self.selected_id>app.ds.drosophila.obj_id.max(): self.selected_id = 1
        self.left_click_img(null, id = self.selected_id)        

    def insect_to_kill(self):
        ###### CORRECCION
        self.img_main = self.ds.change_insect(self.selected_id, "eliminated", self.status)
        self.clear_insect_info()
        wf, hf = self.getScaled(self.img_main)
        CtkImg = customtkinter.CTkImage(light_image = Image.fromarray(self.img_main), size=(wf,hf))
        self.main_image.configure(image = CtkImg)
        self.recalculate()
        ###### CORRECCION

    def insect_to_classify(self):
        
        self.img_main = self.ds.change_insect(self.selected_id, "unclassified", self.status)
        self.label_define("unclassified")
        
        wf, hf = self.getScaled(self.img_main)
        CtkImg = customtkinter.CTkImage(light_image = Image.fromarray(self.img_main), size=(wf,hf))
        self.main_image.configure(image = CtkImg)
        self.recalculate()

    def insect_to_ommit(self):
        self.img_main = self.ds.change_insect(self.selected_id, "omitted", self.status)
        self.label_define("omitted")
        wf, hf = self.getScaled(self.img_main)
        CtkImg = customtkinter.CTkImage(light_image = Image.fromarray(self.img_main), size=(wf,hf))
        self.main_image.configure(image = CtkImg)
        self.recalculate()

    def clear(self):
        self.status = null
        self.info_detected = 0
        self.info_to_classify = 0
        self.info_overlapped = 0
        self.info_error = 0
        self.info_classified = 0
        self.info_males = 0
        self.info_females = 0
        self.ds.path = self.ds.path[0:0]
        self.ds.drosophila = self.ds.drosophila[0:0]
        # ***********************************************************************************************************************************************************************************************************
        self.main_image.configure(image = '') 
        # ***********************************************************************************************************************************************************************************************************
        self.insect_sex.forget()
        self.image_title.configure(text = "[sin imagen]", text_color="grey")
        self.insect_id.configure(text = "[no id]", text_color="grey")

        if self.cb_fema.get()==1: self.cb_fema.toggle()
        if self.cb_male.get()==1: self.cb_male.toggle()
        if self.cb_over.get()==1: self.cb_over.toggle()
        if self.cb_outs.get()==1: self.cb_outs.toggle()

        self.cb_clas.configure(state="disabled")
        self.cb_fema.configure(state="disabled")
        self.cb_male.configure(state="disabled")
        self.cb_over.configure(state="disabled")
        self.cb_outs.configure(state="disabled")

        self.set_screen_buttons()
        self.update_midPanel_info()
        self.clear_insect_info()
        self.disabled_buttons()
        ##### CORRECCION
        self.ds.set_params(self.cfg)
        ##### CORRECCION

    def change_sex(self):
        
        if (self.insect_sex.cget("text") == "male"):
            print(self.selected_id)
            self.img_main = self.ds.change_insect(self.selected_id, "f", self.status)
            self.label_define('f')
        elif (self.insect_sex.cget("text") == "female"):
            print(self.selected_id)
            self.img_main = self.ds.change_insect(self.selected_id, "m", self.status)
            self.label_define('m')       

        wf, hf = self.getScaled(self.img_main)
        CtkImg = customtkinter.CTkImage(light_image = Image.fromarray(self.img_main), size=(wf,hf))
        self.main_image.configure(image = CtkImg)
        
        self.recalculate()

        self.label_objects_count.configure(text=f"{self.info_detected}")
        self.label_objects_to_classify.configure(text=f"{self.info_to_classify}")
        self.label_objects_overlaped.configure(text=f"{self.info_overlapped}")
        self.label_objects_outside1.configure(text=f"{self.info_error}")
        self.label_objects_classified.configure(text=f"{self.info_classified}")        
        self.label_objects_not_classified.configure(text=f"{self.info_overlapped+self.info_error}")
        self.label_machos.configure(text=f"{self.info_males} [{100*self.info_males/self.info_classified:.2f} %]")
        self.label_hembras.configure(text=f"{self.info_females} [{100*self.info_females/self.info_classified:.2f} %]")
        self.label_objects_to_process.configure(text=f"{self.info_overlapped+self.info_error+self.info_females}")


        if self.status==routed: 
            self.ds.repath()
            self.img_main = self.route()
        
    def getScaled(self, img):
        
        # Corrección de la proporción en relación con el contenedor
        rw = img.shape[1]/self.main_image._current_width
        rh = img.shape[0]/self.main_image._current_height
        e = img.shape[1]/img.shape[0]

        if rw>rh:
            wf = int(self.main_image._current_width)
            hf = int(wf/e)
        else:
            hf = int(self.main_image._current_height)
            wf = int(e*hf)
        
        # Calcula la corrección de escala
        self.scaleX = img.shape[1]/wf
        self.scaleY = img.shape[0]/hf

        return wf, hf

    def route(self):
        


        self.ds.insect_targeting(self.img_de)
        ##### CORRECCION


        import time
        start = time.time()

        img = self.ds.route(self.cb_rout.get())

        end = time.time()
        print(end - start)


        ##### CORRECCION
        wf, hf = self.getScaled(img)
        
        CtkImg = customtkinter.CTkImage(light_image = Image.fromarray(img), size=(wf,hf))
 
        self.main_image.configure(image = CtkImg)

        self.status = routed
        
        self.set_screen_buttons()

    def laser_process(self):

        # LASER


        # GRABA IMAGEN

        # BASE DE DATOS
        
        
        session_id = self.db.insert_session(self.img, self.cfg["classify_model"], str(self.cfg["usr_cfg"]["route_opt"]), self.id)

        for _, row in self.ds.drosophila.iterrows():
            self.db.insert_objHistory(session_id, self.id, row.obj_id, row.pixels, row.state, row.x, row.y, row.sex, row.conf, row.sexf)
  
    def bright_change(self, b):
        img = Image.fromarray(self.click_img)
        img = ImageEnhance.Brightness(img)
        img = img.enhance(b)

        #img = ImageEnhance.Contrast
        #img = ImageEnhance.Sharpness
        
        self.image_insect = customtkinter.CTkImage(light_image = img, size=(self.insect_view._current_width, self.insect_view._current_height))    
        self.insect_view.configure(image = self.image_insect)
        
    def doble_left_click_img(self, event):        
        if self.status == detected:
            #sure_window = customtkinter.CTkToplevel(self)
            #sure_window.title = "Crear nueva area"
            #sure_window.resizable(False, False)
            #sure_window.geometry = "400x200"
            
            #sure_window_label1 = customtkinter.CTkLabel(sure_window, text=f"      {event.x} {event.y}      ")
            #sure_window_label1.pack()
            #sure_window.
            
            id = self.ds.drosophila.obj_id.max()+1
            pixels = -1
            targetX = int(self.scaleX*event.x)
            targetY = int(self.scaleY*event.y)
                                                
            self.ds.drosophila.loc[len(self.ds.drosophila.index)] = [id, pixels, (int(self.scaleX*event.x))-int(self.ds.rect/2), (int(self.scaleY*event.y))-int(self.ds.rect/2), "n/a", 'unclassifed', targetX, targetY, 0.0, "n/a"]   

            # redibujar boxes
            self.set_image(self.ds.draw_insect_info(self.status))

            self.info_detected+=1
            self.info_to_classify+=1

            self.update_midPanel_info()
            
        #elif self.status == classified:
        #    self.change_sex()            

            # redibujar boxes
        #    self.set_image(self.ds.draw_insect_info())
        #    self.update_midPanel_info()

    def label_define(self, status):
        if status == 'f':
            self.insect_sex.place(in_=self.insect_view, rely=0.92, relx=0.009)
            self.insect_sex.configure(text="female", fg_color='#%02x%02x%02x' % self.cFemale, state="normal", text_color="white", border_color="white", hover=False)
        elif status == 'm':
            self.insect_sex.place(in_=self.insect_view, rely=0.92, relx=0.009)
            self.insect_sex.configure(text="male", fg_color='#%02x%02x%02x' % self.cMale, state="normal", text_color="white", border_color="white", hover=False)
        elif status == 'overlaped':
            self.insect_sex.place(in_=self.insect_view, rely=0.92, relx=0.009)
            self.insect_sex.configure(text="overlapped", fg_color='#%02x%02x%02x' % self.cOverlap, state="normal", text_color="white", border_color="white", hover=False)
        elif (status == 'out of bound 2' or status == 'out of bound 1'):
            self.insect_sex.place(in_=self.insect_view, rely=0.92, relx=0.009)
            self.insect_sex.configure(text="out of bounds", fg_color='#%02x%02x%02x' % self.cOut, state="normal", text_color="white", border_color="white", hover=False)
        elif status == 'unclassified':
            self.insect_sex.place(in_=self.insect_view, rely=0.92, relx=0.009)
            self.insect_sex.configure(text="to classify", fg_color='#%02x%02x%02x' % self.cDetected, state="normal", text_color="white", border_color="white", hover=False)
        elif status == 'omitted':
            self.insect_sex.place(in_=self.insect_view, rely=0.92, relx=0.009)
            self.insect_sex.configure(text="omitted", fg_color="grey", state="normal", text_color="white", border_color="white", hover=False)
        else:
            self.insect_sex.place_forget()
        ##### CORREGIDO
        if self.status == routed: self.insect_sex.configure(state="disabled")
        ##### CORREGIDO
    
    def left_click_img(self, event, id = 0):        

        if id==0:
            ##### CORREGIDO
            insect = self.ds.drosophila[(self.ds.drosophila.x<int(self.scaleX*event.x)) &
                            (self.ds.drosophila.y<int(self.scaleY*event.y)) &
                            (self.ds.drosophila.y+self.ds.rect>int(self.scaleY*event.y)) &
                            (self.ds.drosophila.x+self.ds.rect>int(self.scaleX*event.x)) & (self.ds.drosophila.state!="elminated")]
            ##### CORREGIDO
            if insect.obj_id.count()>0:

                #self.label_objects_to_process.configure(text=f"click en {insect.obj_id.item()} x: {event.x} y: {event.y} xr: {int(self.scaleX*event.x)} yr: {int(self.scaleY*event.y)}")
                rect = self.ds.rect
                if insect.y.item()<0: insect.y = 0
                if insect.x.item()<0: insect.x = 0
                self.click_img = self.ds.img_orig[insect.y.item():insect.y.item()+rect, insect.x.item():insect.x.item()+rect]
                self.image_insect = customtkinter.CTkImage(light_image = Image.fromarray(self.click_img), size=(self.insect_view._current_width, self.insect_view._current_height))
                self.insect_view.configure(image = self.image_insect)

                self.selected_id = insect.obj_id.item()
                self.set_right_insect_info()

                #self.insect_status.configure(text = insect.state.item())
                #self.insect_sex.configure(text = insect.sex.item())
                #self.insect_confidence.configure(text = insect.conf.item())

                
                #self.insect_id.configure(text = f"[{insect.obj_id.item()}]",text_color="white")
                
                #self.bright_change(self.bright.get())
                #self.label_define(insect.sex.item())

                self.enabled_buttons()
        else:
            if self.ds.drosophila[self.ds.drosophila.obj_id==id].obj_id.count()>0:
                insect = self.ds.drosophila[(self.ds.drosophila.obj_id==id)]
                if insect.obj_id.count()>0:
                    
                    rect = self.ds.rect
                    if insect.y.item()<0: insect.y = 0
                    if insect.x.item()<0: insect.x = 0
                    self.click_img = self.ds.img_orig[insect.y.item():insect.y.item()+rect, insect.x.item():insect.x.item()+rect]
                    self.image_insect = customtkinter.CTkImage(light_image = Image.fromarray(self.click_img), size=(self.insect_view._current_width, self.insect_view._current_height))
                    self.insect_view.configure(image = self.image_insect)
                    self.selected_id = insect.obj_id.item()
                    self.set_right_insect_info()

    def set_right_insect_info(self):

        if self.selected_id>0:

            insect = self.ds.drosophila[(self.ds.drosophila.obj_id==self.selected_id)]

            self.insect_status.configure(text = insect.state.item())
            self.insect_sex.configure(text = insect.sexf.item())            ## sexf o sex
            self.insect_confidence.configure(text = insect.conf.item())
            
            self.insect_id.configure(text = f"[{insect.obj_id.item()}]",text_color="white")
            
            self.bright_change(self.bright.get())

            if insect.state.item() == 'classified':
                self.label_define(insect.sexf.item())           ## sexf o sex
            else:
                self.label_define(insect.state.item())

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
        customtkinter.CTkInputDialog()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def config(self):
        c = Config()
        
        ##### CORRECCION
        f = open('sitia_conf.json', "r")
        self.cfg = json.load(f)
        f.close()

        self.ds.set_params(self.cfg)
        ##### CORRECCION

        #self.open_input_dialog_event()

    def image_load(self, event=None):

        filetypes = (
            ('fotos', ('*.jpeg', '*.jpg', '*.png', '*.gif')),
            ('todos los archivos', '*.*')
        )

        image_file = fd.askopenfilename(
            title='Cargar una foto',
            initialdir='/Users/lucianosmith/Documents/CEIA/',
            filetypes=filetypes)

    
        self.image_title.configure(text = f"[{image_file}]",text_color="white")
        img_orig = cv2.imread(image_file, cv2.COLOR_BGR2RGB) 
        img_orig = cv2.cvtColor(img_orig, cv2.COLOR_RGB2BGR)
        self.ds.set_img(img_orig)

        self.set_image(img_orig)
        
        self.status = started
        self.set_screen_buttons()
        self.clear_btn.configure(state="normal")

    def set_image(self, img):
        self.img_array = img.copy()
        wf, hf = self.getScaled(img)
        self.image = customtkinter.CTkImage(light_image = Image.fromarray(img), size=(wf, hf))
        self.main_image.configure(image = self.image)
        self.update_midPanel_info()

    def take_image(self, event=None):
        # reemplazar por la imagen tomada de la camara

        current_dateTime = datetime.now()
        self.img = str(current_dateTime.year) +"-"+ str(current_dateTime.month)+"-"+str(current_dateTime.day)+"_"+str(current_dateTime.hour)+"-"+str(current_dateTime.minute)+"-"+str(current_dateTime.second)+".jpg"


        #image_file = "/Users/lucianosmith/Downloads/DATASET/2024-10-10-14-44-51.png"
        image_file = "ds1.jpg"
        self.image_title.configure(text = f"[{self.img}]",text_color="white")
        img_orig = cv2.imread(image_file, cv2.COLOR_BGR2RGB) 
        img_orig = cv2.cvtColor(img_orig, cv2.COLOR_RGB2BGR)
        self.ds.set_img(img_orig)
        self.set_image(img_orig)
        self.status = started        
        self.set_screen_buttons()
        self.update_midPanel_info()
        self.clear_btn.configure(state="normal")
        
    def detect(self):

        # realiza la detección
        self.img_main, self.img_de = self.ds.insect_detection()

        # actualiza la imagen
        self.set_image(self.img_main)
        
        self.info_detected = self.ds.drosophila.obj_id.count()
        self.info_to_classify = self.ds.drosophila[self.ds.drosophila.state == 'unclassifed'].obj_id.count()
        self.info_overlapped = self.ds.drosophila[self.ds.drosophila.state == 'overlaped'].obj_id.count()
        self.info_error = self.ds.drosophila[self.ds.drosophila.state == 'out of bound 1'].obj_id.count()+self.ds.drosophila[self.ds.drosophila.state == 'out of bound 2'].obj_id.count()

        self.status = detected

        self.cb_clas.configure(state="normal")
        self.cb_over.configure(state="normal")
        self.cb_outs.configure(state="normal")


        ####################### CORRECCION
        if self.cb_clas.get()==False: self.cb_clas.toggle()
        if self.cb_over.get()==False: self.cb_over.toggle()
        if self.cb_outs.get()==False: self.cb_outs.toggle()
        ####################### CORRECCION

        self.update_midPanel_info()
        self.set_screen_buttons()

        # selecciona el #1
        if  self.ds.drosophila.obj_id.count()>0:
            insect = self.ds.drosophila[(self.ds.drosophila.obj_id==1)]
            if insect.obj_id.count()>0:
                self.click_img = self.ds.img_orig[insect.y.item():insect.y.item()+self.ds.rect, insect.x.item():insect.x.item()+self.ds.rect]
                self.image_insect = customtkinter.CTkImage(light_image = Image.fromarray(self.click_img), size=(self.insect_view._current_width, self.insect_view._current_height))
                self.insect_view.configure(image = self.image_insect)
                self.selected_id = insect.obj_id.item()
                self.set_right_insect_info()
                self.enabled_buttons()

    def set_screen_buttons(self):
        ######### CORRECCION
        if self.status == null:
            # left panel buttons   HOVER = 23476D
            self.load_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)
            self.take_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)
            self.detect_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.classify_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.route_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.process_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.config_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)

        elif self.status == started:
            # left panel buttons
            self.load_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.take_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.detect_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)
            self.classify_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.route_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.process_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.config_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)

        elif self.status == detected:
            # left panel buttons
            self.button_classify.configure(state="normal")
            self.load_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.take_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.detect_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.classify_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)
            self.route_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.process_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.config_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)

        elif self.status == classified:
            # left panel buttons
            
            self.button_classify.configure(state="disabled")
            
            self.load_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.take_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.detect_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.classify_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.route_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)
            self.process_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.config_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)

        elif self.status == routed:
            
            self.button_classify.configure(state="disabled")
            self.button_eliminar.configure(state="disabled")
            self.button_ommit.configure(state="disabled")
            
            # left panel buttons
            self.load_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.take_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.detect_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.classify_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.route_btn.configure(state="disabled", fg_color="transparent", border_width=1)
            self.process_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)
            self.config_btn.configure(state="normal", fg_color="#3669A0", border_width = 0)

        elif self.status == executed:
            pass
        else:
            pass
        ######### CORRECCION

    def recalculate(self):

        self.info_detected = self.ds.drosophila.obj_id.count()
        self.info_to_classify = self.ds.drosophila[self.ds.drosophila.state == 'unclassified'].obj_id.count()
        self.info_overlapped = self.ds.drosophila[self.ds.drosophila.state == 'overlaped'].obj_id.count()
        ##### CORRECCION
        self.info_error = self.ds.drosophila[self.ds.drosophila.state == 'out of bound 1'].obj_id.count()+self.ds.drosophila[self.ds.drosophila.state == 'out of bound 2'].obj_id.count()+self.ds.drosophila[self.ds.drosophila.state == 'omitido'].obj_id.count()
        ##### CORRECCION
        self.info_classified = self.ds.drosophila[self.ds.drosophila.state == 'classified'].obj_id.count()
        self.info_not_classified = self.ds.drosophila[self.ds.drosophila.state == 'unclassified'].obj_id.count()
        self.info_males = self.ds.drosophila[self.ds.drosophila.sexf == 'm'].obj_id.count()
        self.info_females = self.ds.drosophila[self.ds.drosophila.sexf == 'f'].obj_id.count()
        self.info_to_process = self.ds.drosophila[self.ds.drosophila.state == 'out of bound 2'].obj_id.count()

        self.update_midPanel_info()

    def classify(self):
        ###### CORRECCION
        if self.info_overlapped>0:
            result =  tkinter.messagebox.askyesno("Confirmación", "Existen insectos solapados ¿desea continuar con la clasificación?")
        else:
            result = True
        ###### CORRECCION
        if result:
            img_f = self.ds.image_classification(self.img_de)
            self.set_image(img_f)
            self.status = classified
            self.recalculate()
            # actualiza pantalla 
            self.update_midPanel_info()
            self.set_screen_buttons()


            if self.cb_clas.get()==1 :
                self.cb_clas.toggle()
                self.cb_clas.configure(state="disabled")

            self.cb_fema.configure(state="normal")
            self.cb_male.configure(state="normal")

            self.cb_male.toggle()
            self.cb_fema.toggle()


            self.img_de = img_f.copy()

    def update_midPanel_info(self):

        if self.status == null:
            self.label_25.configure(text="individuals to be prosecuted")
            self.label_status.configure(text="[N/A]")
            self.label_objects_count.configure(text="-")
            self.label_objects_to_classify.configure(text="-")
            self.label_objects_overlaped.configure(text="-")
            self.label_objects_outside1.configure(text="-")

            self.label_objects_classified.configure(text="-")        
            self.label_objects_not_classified.configure(text="-")
            self.label_machos.configure(text="-")
            self.label_hembras.configure(text="-")
            self.label_objects_to_process.configure(text="-")

        elif self.status == started:
            self.label_status.configure(text="[Iniciado]")

        elif self.status == detected:
            self.label_status.configure(text="[Detectado]")
            self.label_objects_count.configure(text=f"{self.info_detected}")
            self.label_objects_to_classify.configure(text=f"{self.info_to_classify}")
            self.label_objects_overlaped.configure(text=f"{self.info_overlapped}")
            self.label_objects_outside1.configure(text=f"{self.info_error}")

        elif self.status == classified:
            self.set_right_insect_info()
            self.label_status.configure(text="[Clasificado]")

            self.label_objects_classified.configure(text=f"{self.info_classified}")        
            self.label_objects_not_classified.configure(text=f"{self.info_overlapped+self.info_error}")
            self.label_machos.configure(text=f"{self.info_males} [{100*self.info_males/self.info_classified:.2f} %]")
            self.label_hembras.configure(text=f"{self.info_females} [{100*self.info_females/self.info_classified:.2f} %]")
            self.label_objects_to_process.configure(text=f"{self.info_overlapped+self.info_error+self.info_females}")
            ##### CORRECCION
            self.label_objects_outside1.configure(text=f"{self.info_error}")          
            self.label_objects_overlaped.configure(text=f"{self.info_overlapped}")  
            ##### CORRECCION

        elif self.status == routed:
            self.clear_insect_info()
            self.label_status.configure(text="[Ruteado]")

        elif self.status == executed:
            self.clear_insect_info()
            self.label_status.configure(text="[Procesado]")
            self.label_25.configure(text="individuos procesados")
            
    def clear_insect_info(self):
        # ***********************************************************************************************************************************************************************************************************
        self.insect_view.configure(image = '') # WARNING
        # ***********************************************************************************************************************************************************************************************************
        self.insect_status.configure(text = "-")
        self.insect_sex.configure(text = "-")
        self.insect_confidence.configure(text = "-")
        self.selected_id = -1
        self.insect_id.configure(text = "[no id]", text_color="grey")
        self.insect_sex.place_forget()

if __name__ == "__main__":     
    db = sitia_db()
    ventana_login = Login(db)
    app = App(db, ventana_login.usr, ventana_login.id)
    app = App(db, 'admin', 1)
    app.mainloop()
    
    app.cfg["checkbox"]["bbox"] = app.cb_bbox.get()
    app.cfg["checkbox"]["objn"] = app.cb_objn.get()
    app.cfg["checkbox"]["conf"] = app.cb_conf.get()
    app.cfg["checkbox"]["targ"] = app.cb_targ.get()
    app.cfg["checkbox"]["rout"] = app.cb_rout.get()
    
    f = open('sitia_conf.json', "w")
    json.dump(app.cfg, f)
    f.close()


    

# %%
app.ds.drosophila

# %%



