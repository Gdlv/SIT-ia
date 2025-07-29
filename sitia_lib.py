import cv2
import pandas as pd
import numpy as np
import random
import torch
import torch.nn as nn
import torchvision
from torchvision.transforms import transforms
from PIL import Image
import matplotlib.colors as colors

# Agregar la ruta de instalación personalizada a PythonPATH
#import sys
#sys.path.append("D:/Documentos/PostDocUY/tesistas/Luciano_Smith/SITIA/_internal")
from ant_colony import AntColonyLS as ACLS 



#import matplotlib.pyplot as plt



class InsectClassifier(torch.nn.Module):
    def __init__(self, output_units):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding='same') # 144 x 144
        self.pool1 = torch.nn.MaxPool2d(kernel_size=2, stride=2) # 72 x 72
        self.conv2 = torch.nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding='same')
        self.pool2 = torch.nn.MaxPool2d(kernel_size=2, stride=2) # 36 x 36
        self.conv3 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding='same')
        self.pool3 = torch.nn.MaxPool2d(kernel_size=2, stride=2) # 18 x 18
        self.conv4 = torch.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding='same')
        self.pool4 = torch.nn.MaxPool2d(kernel_size=2, stride=2) # 9 x 9
        self.fc1 = torch.nn.Linear(in_features=128*9*9, out_features=512)       ## MODIF
        #output_units = 1 ## MODIF 
        self.fc2 = torch.nn.Linear(in_features=512, out_features=output_units)  

    def forward(self, x):
        x = self.pool1(torch.relu(self.conv1(x)))
        x = self.pool2(torch.relu(self.conv2(x)))
        x = self.pool3(torch.relu(self.conv3(x)))
        x = self.pool4(torch.relu(self.conv4(x)))
        x = torch.flatten(x, 1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        #return x
        return torch.sigmoid(x) ## MODIF         

# Definir la transformación de datos para el conjunto de prueba
#transform = transforms.Compose([
#    transforms.Resize((ANCHO_IMAGENES, ALTO_IMAGENES)),
#    transforms.ToTensor(),
#])

def preprocesar_imagen(array_img, w, h):

    array_img = array_img[:, :, ::-1]       # 7/11/2024 cambia a RGB
    #imgplot = plt.imshow(array_img)
    #plt.show()
    #print(array_img.shape)
    #print(w, h)


    transformacion = torchvision.transforms.Compose([
        torchvision.transforms.Resize(size=(w, h)),
        torchvision.transforms.ToTensor(),
        #torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    imagen = Image.fromarray(array_img)
    #imagen = Image.open(imagen_path)
    imagen = transformacion(imagen)
    imagen = imagen.unsqueeze(0)  # Agregar dimensión batch
    return imagen

def predecir_imagen(array_img, modelo, w, h):
    
    imagen = preprocesar_imagen(array_img, w, h)

    with torch.no_grad():
        salida = modelo(imagen)
    output = salida.numpy()
    
    c = (max(output[0][0], output[0][1])/(output[0][0] + output[0][1]))

    _, indice_prediccion = torch.max(salida, 1)
    
    return indice_prediccion.item(), c

class sitia():

    def __init__(self, model, cfg) -> None:
        self.set_params(cfg)
        # inicializa el modelo de IA
        self.model = InsectClassifier(self.classes_num)
        # Cargar los pesos entrenados
        self.model.load_state_dict(torch.load(model)) # '01_nn1_modelo_insectos2000.pth'
        self.model.eval()  # Establecer el modelo en modo de evaluación

    def set_img(self, img) -> None:
        self.img_orig = img.copy()

    def set_params(self, cfg) -> None:

        self.classes_num = int(cfg["others"]["classes_num"])
        self.y_text = int(cfg["others"]["y_text"])
        self.target_line_width = int(cfg["others"]["target_line_width"])
        self.route_line_width = int(cfg["others"]["route_line_width"])
        self.bb_line_width = int(cfg["others"]["bb_line_width"])
        self.color_route = tuple([int(255*x) for x in colors.hex2color(cfg["others"]["color_route"])])
        self.color_target = tuple([int(255*x) for x in colors.hex2color(cfg["others"]["color_target"])])
        self.target_size = int(cfg["others"]["target_size"])
        self.target_center_size = int(cfg["others"]["target_center_size"])
        
        self.img_width = int(cfg["usr_cfg"]["width"])
        self.img_height =int( cfg["usr_cfg"]["height"])
        self.rect = int(cfg["usr_cfg"]["img_size"])

        self.color_detected = cfg["usr_cfg"]["color_detected"]
        self.color_overlapped = cfg["usr_cfg"]["color_overlapped"]
        self.color_out_of_bounds1 = cfg["usr_cfg"]["color_out_of_bounds"]
        self.color_out_of_bounds2 = cfg["usr_cfg"]["color_out_of_bounds"]
        self.color_female = cfg["usr_cfg"]["color_female"]
        self.color_male= cfg["usr_cfg"]["color_male"]
        self.color_ommited = cfg["others"]["color_ommited"]
        self.lower_color_eyes = cfg["usr_cfg"]["lower_color_eyes"]
        self.upper_color_eyes = cfg["usr_cfg"]["upper_color_eyes"]

        self.bin_bright =  int(cfg["usr_cfg"]["bin_bright"])
        self.gaussian_blur =  int(cfg["usr_cfg"]["gaussian_blur"])
        self.lower_limit = int( cfg["usr_cfg"]["lower_limit"])
        self.upper_limit =  int(cfg["usr_cfg"]["upper_limit"])
        
        self.dilation_int =  int(cfg["usr_cfg"]["dilation_int"])
        self.erosion_int =  int(cfg["usr_cfg"]["erosion_int"])
        self.kernel_size = int( cfg["usr_cfg"]["kernel_size"])

        self.target_kernel =  int(cfg["usr_cfg"]["target_kernel"])
        self.target_int =  int(cfg["usr_cfg"]["target_int"])
        self.classify_threshold =  float(cfg["usr_cfg"]["classify_threshold"])  # si la confianza no supera el umbral la considera hembra

        self.threshold_1 =  int(cfg["usr_cfg"]["threshold_1"])
        self.threshold_min =  int(cfg["usr_cfg"]["threshold_min"])
        self.threshold_max =  int(cfg["usr_cfg"]["threshold_max"])
        
        self.draw_bbox = int(cfg["checkbox"]["bbox"])  # draw bounding boxes
        self.draw_objn = int(cfg["checkbox"]["objn"])  # draw object number
        self.draw_conf = int(cfg["checkbox"]["conf"])  # draw confidence
        self.draw_targ = int(cfg["checkbox"]["targ"])  # draw target
        
        
        
        self.draw_rout = int(cfg["checkbox"]["rout"])  # draw route 
        

        self.route_opt =  int(cfg["usr_cfg"]["route_opt"])  

        self.draw_clas = 1
        self.draw_over = 1
        self.draw_outs = 1
        self.draw_male = 1
        self.draw_fema = 1

        self.laser_x0 =  int(cfg["usr_cfg"]["laser_x0"])
        self.laser_y0 =  int(cfg["usr_cfg"]["laser_y0"])

        self.columns = ['obj_id', 'pixels' ,'x', 'y', 'sex', 'state', 'targetX', 'targetY', 'conf', 'sexf']
        self.drosophila = pd.DataFrame(columns=self.columns) # crea el dataframe
        
        self.path = pd.DataFrame(columns=['obj_id', 'targetX', 'targetY'])                                                   # path para el laser
        self.path.loc[len(self.path.index)] = [-2, self.laser_x0, self.laser_y0] # agrega la posicion del laser 
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX    
        
    def increase_brightness(self, img, value):
        # incrementa el brillo de la imagen
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        return img
    
    def image_threshold(self, img, br, gb, li, ls):
        # binarizacion, br cantidad de brillo, gb = kernel del gaussian blur, li y ls limites superior e inferior del theadhold
        img_b = self.increase_brightness(img, value=br)
        img_b  = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
        img_b = cv2.GaussianBlur(img_b, (gb,gb), 0)
        _, img_c = cv2.threshold(img_b, li, ls, cv2.THRESH_BINARY)
        return img_c
    
    def image_erodil(self, img, d_iter, e_iter, k):
        # Morphological Operations: erosiona y dilata ... k tamano del kernel, d_iter, e_iter iteraciones en dilatacion y erosion
        # erossion and dilatation
        kernel = np.ones((k,k), np.uint8)

        img = cv2.dilate(img, kernel, iterations = d_iter)
        img = cv2.erode(img, kernel, iterations = e_iter)
        return  img
    
    def image_overlap(self, img):
        # VERIFICAR
        temp_cont, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ret = 'sin clasificar'
        if (len(temp_cont)>1):                      # cuenta contornos en temp_img
            ret = 'overlaped'

        return ret
    
    def image_addBoundingbox(self, img, x0, y0, ov, text, q, y_text, s = "n/a", conf = 0.0):
    
        c = (0,0,0)
        
        if ov == "sin clasificar":
            c = tuple([int(255*x) for x in colors.hex2color(self.color_detected)])  # verde 
            if self.draw_bbox==1:
                if self.draw_clas == 1:
                    cv2.rectangle(img, (x0, y0), (x0+self.rect, y0+self.rect), c, self.bb_line_width)

        if ov == "overlaped": 
            c = tuple([int(255*x) for x in colors.hex2color(self.color_overlapped)])  # rojo
            if self.draw_bbox==1:
                if self.draw_over == 1:            
                    cv2.rectangle(img, (x0, y0), (x0+self.rect, y0+self.rect), c, self.bb_line_width)

        if ov == "omitido": 
            c = tuple([int(255*x) for x in colors.hex2color(self.color_ommited)])          
            if self.draw_bbox==1:
                cv2.rectangle(img, (x0, y0), (x0+self.rect, y0+self.rect), c, self.bb_line_width)
                
        if ov == "fuera umbral 1": 
            c = tuple([int(255*x) for x in colors.hex2color(self.color_out_of_bounds1)])   
            if self.draw_bbox==1:
                if self.draw_outs == 1:            
                    cv2.rectangle(img, (x0, y0), (x0+self.rect, y0+self.rect), c, self.bb_line_width)

        if ov == "fuera umbral 2": 
            c = tuple([int(255*x) for x in colors.hex2color(self.color_out_of_bounds2)])  
            if self.draw_bbox==1:
                if self.draw_outs == 1:            
                    cv2.rectangle(img, (x0, y0), (x0+self.rect, y0+self.rect), c, self.bb_line_width)        
        
        if ov == "classified": 
            if s == "f":
                c = tuple([int(255*x) for x in colors.hex2color(self.color_female)])      
                if self.draw_bbox==1:
                    if self.draw_fema == 1:            
                        cv2.rectangle(img, (x0, y0), (x0+self.rect, y0+self.rect), c, self.bb_line_width)        
            if s == "m":
                c = tuple([int(255*x) for x in colors.hex2color(self.color_male)])  
                if self.draw_bbox==1:
                    if self.draw_male == 1:            
                        cv2.rectangle(img, (x0, y0), (x0+self.rect, y0+self.rect), c, self.bb_line_width)        

        if (text==True) and (self.draw_objn==1):
            cv2.putText(img, str(q), (x0, y0-y_text), self.font, 1, c, 2, cv2.LINE_AA)

        if (conf>0) and (self.draw_conf==1):
            cv2.putText(img, f"{conf:.2f}", (x0+100, y0-y_text), self.font, .8, c, 2, cv2.LINE_AA)

        return img

    def image_contours(self, img_t, img_o, writePNG, t, rect, pMin, pMax):
        # detecta y analiza contornos, t? rect: tamanno del recuadro, pMin, pMax: % maximo y minimo de pixes ocupados    
        img_t = cv2.bitwise_not(img_t)
        contornos, _ = cv2.findContours(img_t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_fin = img_o.copy()

        hmin = 20
        wmin = 20
        hmax = 120
        wmax = 120
        y_text = 10

        cont = 0
        p = 0
        for c in contornos:
            if len(c)>t:                                # que carajos es t??? y este proc???

                (x, y, w, h) = cv2.boundingRect(c)                          # realiza el bounding box

                x0 = int((x + w/2) - (rect/2))                              # localiza la coordenada x0 basado en el tamaño del recuadro
                y0 = int((y + h/2) - (rect/2))                              # localiza la coordenada y0 basado en el tamaño del recuadro
                
                cont = cont + 1                                             # incrementa la cantidad de objetos encontrados
                
                if ((h>hmin) and (w>wmin)) and ((h<hmax) and (w<wmax)):     # tamaño minimo y maximo del recuadro

                    roi1 = img_t[y0:y0+rect, x0:x0+rect]                    # roi de imagen binarizada
                    q = cv2.countNonZero(roi1)                              # calculo de % de pixels ocupados
                    p = round((q/(rect*rect))*100, 1)
                    
                    if (p>pMin) and (p<pMax):                               # seleccion de % minimo y maximo

                        ov = self.image_overlap(roi1)                            # verifica superposición de imagenes
                    
                        if writePNG:
                            roi = img_o[y0:y0+rect, x0:x0+rect] 
                            cv2.imwrite(str(cont)+'.png', roi)
                        
                    else:

                        ov = "fuera umbral 1"
                    
                else:

                    ov = "fuera umbral 2"
                

                img_fin = self.image_addBoundingbox(img_fin, x0, y0, ov, True, cont, self.y_text)

                self.drosophila.loc[len(self.drosophila.index)] = [cont, p, x0, y0, "n/a", ov, 0, 0, 0.0, "n/a"]   # registra el roi


        return img_fin    

    def roi_target(self, roi, img, x0, y0, cross, draw = True):
        # marca el centro de masa, cross tamaño de la mira
        
        c = int(cross/2)                         #  la cruz tiene 2*cross de lado
        
        eyes_lo=tuple([int(255*x) for x in colors.hex2color(self.lower_color_eyes)])   # np.array([90,60,60])
        eyes_hi=tuple([int(255*x) for x in colors.hex2color(self.upper_color_eyes)])   # np.array([125,85,85])
        

        mask=cv2.inRange(roi, eyes_lo, eyes_hi)
        M = cv2.moments(mask)
    
        # calculate x,y coordinate of center
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
    
        x = x0 + x
        y = y0 + y
    
        #cv2.putText(img, "target", (x - 25, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        if draw:
            cv2.circle(img, (x, y), self.target_center_size,self.color_target, -1)
            cv2.line(img, (x, y-c), (x, y+c), self.color_target, self.target_line_width) 
            cv2.line(img, (x-c, y), (x+c, y), self.color_target, self.target_line_width) 

        return x, y, img
    
    def roi_target_plus(self, roi, img, x0, y0, cross, draw = True):
        # marca el centro de masa, cross tamaño de la mira (teniendo en cuenta que son boundingboxes con errores)
        c = int(cross/2)                         #  la cruz tiene 2*cross de lado

        roi = cv2.bitwise_not(roi)

        
        kernel = np.ones((self.target_kernel,self.target_kernel), np.uint8)
        roi = cv2.erode(roi, kernel, iterations = self.target_int)

        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)     #AGREGADO
        contornos, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) ### ACA ERROR!!!!

        for contor in contornos:
            (x, y, w, h) = cv2.boundingRect(contor) 
            x = int(x + w/2) + x0
            y = int(y + h/2) + y0

            # put text and highlight the center
            if draw:
                cv2.circle(img, (x, y), self.target_center_size, self.color_target, -1)    
                cv2.line(img, (x, y-c), (x, y+c), self.color_target, self.target_line_width) 
                cv2.line(img, (x-c, y), (x+c, y), self.color_target, self.target_line_width) 
                self.path.loc[len(self.path.index)] = [-1, x, y] 

        return x, y, img
    
    def xyRepair(self, x0, y0, rect):
    
        # faltaria cubrir si se pasa de la imagen, es decir si x+150 > ancho de la imagen
        x1 = x0
        y1 = y0
        x2 = x0 + rect
        y2 = y0 + rect

        if ((x0<0) or (y0<0)):
            if (y0<0):
                y1 = 0
                y2 = rect+y0
            if (x0<0):
                x1 = 0
                x2 = rect+x0

        return x1,y1,x2,y2

    def img_ramdom_classify(self, img):
        sex = random.choice(["f", "m"])
        conf = 1.00
        return sex, conf
    
    def img_yolonas_classify(img):
        pass
        #    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #    cv2.imwrite('temp.png' , img)
        #    pa = 'temp.png'
        #    p = best_model.predict(pa, max_predictions=1, fuse_model=False)
        #    conf = p.prediction.confidence[0]
        #    if (p.prediction.labels[0]==1) or (conf<=0.65): 
        #        sex = 'f' 
        #    else: 
        #        sex = 'm'
        #    print(sex, conf)
        #    return sex, conf

    def img_nn_classify(self, img):
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        p, c = predecir_imagen(img, self.model, self.img_width, self.img_height)

        if (p==0) or (c<=self.classify_threshold): 
            sex = 'f' 
        else: 
            sex = 'm'
        #print(sex, c)
        return sex, c

    def img_classification(self, img):
        #sex, conf = self.img_ramdom(img)
        sex, conf = self.img_nn_classify(img)
        return sex, conf

    def image_classification(self, img_de):

        # recorre el dataset de las que estan en estado "sin clasificar"
        img_f = self.img_orig.copy()

        for _, row in self.drosophila.iterrows():

            x0 = int(row.x)
            y0 = int(row.y)

            roi = self.img_orig[y0:y0+self.rect, x0:x0+self.rect]  
            st = row.state

            s = 'n/a'
            conf = 0.0
            if (row.state == 'sin clasificar'):
                s, conf = self.img_classification(roi)                                            
                st = 'classified'
                
            # actualiza el dataframe
            self.drosophila.loc[self.drosophila['obj_id'] == row.obj_id, ['state']] = st
            self.drosophila.loc[self.drosophila['obj_id'] == row.obj_id, ['sex']] = s
            self.drosophila.loc[self.drosophila['obj_id'] == row.obj_id, ['sexf']] = s
            self.drosophila.loc[self.drosophila['obj_id'] == row.obj_id, ['conf']] = conf
            
            # redibuja boundingboxes
            self.img_f = self.image_addBoundingbox(img_f, x0, y0, st, True, row.obj_id, self.y_text, s, conf)

        return self.img_f

    def repath(self):
        self.path = self.path[0:0]
        self.path.loc[len(self.path.index)] = [-2, self.laser_x0, self.laser_y0] # agrega la posicion del laser!!! 
        for _, row in self.drosophila.iterrows():
            ##### CORREGIR
            if (row.sexf=='f' or row.state!='classified'):
                if (row.state!="eliminado"):
                    self.path.loc[len(self.path.index)] = [row.obj_id, row.targetX, row.targetY]
            ##### CORREGIR

    def insect_targeting(self, img):

        img_f = self.img_orig.copy()

        
        ##### CORREGIR
        for _, row in self.drosophila.iterrows():

            if ((row.targetX>0) or (row.targetY>0)):
                if ((row.sexf=="f") or (row.sexf=="n/a")) and (row.state!="eliminado"):   # SI ES UNA MOSCA QUE YA TIENE COORDENADAS LA DIBUJA ... PERO UNICAMENTE SI ES F o PARA ELIMINAR
                    # dibuja directamente
                    c = int(self.target_size/2)  
                    cv2.circle(img_f, (row.targetX, row.targetY), self.target_center_size, self.color_target, -1)        
                    cv2.line(img_f, (row.targetX, row.targetY-c), (row.targetX, row.targetY+c),self.color_target, self.target_line_width) 
                    cv2.line(img_f, (row.targetX-c, row.targetY), (row.targetX+c, row.targetY),self.color_target, self.target_line_width) 
                    if (self.path[self.path.obj_id == row.obj_id].obj_id.count()==0):
                        self.path.loc[len(self.path.index)] = [row.obj_id, row.targetX, row.targetY] 

            else:   # ambas coordenadas son cero
                # calcula y dibuja
                targetX = 0 
                targetY = 0 

                x0 = int(row.x)
                y0 = int(row.y)
                roi = self.img_orig[y0:y0+self.rect, x0:x0+self.rect]  
                conf = 0.0                

                x1, y1, x2, y2 = self.xyRepair(x0, y0, self.rect)

                if (row.sexf=="f") and (row.state!="eliminado"):                                                                       # si es "f" 
                    roi = self.img_orig[y1:y2, x1:x2]  
                    targetX, targetY, img_f = self.roi_target(roi, img_f, x1, y1, self.target_size)                    # encuentra punto de target de moscas ok y dibuja
                    self.path.loc[len(self.path.index)] = [row.obj_id, targetX, targetY]                 # registra el target

                if (row.state != "classified") and (row.state!="eliminado"):                                                          # elimina la resto (no machos)
                    roi = img[y1:y2, x1:x2]         
                    targetX, targetY, img_f = self.roi_target_plus(roi, img_f, x1, y1, self.target_size)    # encuentra punto de target de moscas con problemas

                if (row.sexf=="m") and (row.state!="eliminado"): 
                    roi = img[y1:y2, x1:x2]
                    targetX, targetY, img_f = self.roi_target(roi, img_f, x1, y1, self.target_size, False)                     

                # actualiza el dataframe
                self.drosophila.loc[self.drosophila['obj_id'] == row.obj_id, ['targetX']] = targetX
                self.drosophila.loc[self.drosophila['obj_id'] == row.obj_id, ['targetY']] = targetY
                self.drosophila.loc[self.drosophila['obj_id'] == row.obj_id, ['conf']] = conf
        ##### CORREGIR    
        return img_f




    def insect_detection(self):

        # detecta los insectos (ubicacion y bounding boxes)
        img_pre = self.image_threshold(self.img_orig, self.bin_bright, self.gaussian_blur, self.lower_limit, self.upper_limit)

        #plt.figure(figsize = (200,20))
        #plt.imshow(img_pre) 

        img_de = self.image_erodil(img_pre, self.dilation_int, self.erosion_int, self.kernel_size)

        #plt.figure(figsize = (200,20))
        #plt.imshow(img_de) 

        img_c = self.image_contours(img_de, self.img_orig, False , self.threshold_1, self.rect, self.threshold_min, self.threshold_max) 
    
        #plt.figure(figsize = (200,20))
        #plt.imshow(img_c) 
    
        return img_c, img_de
    
    def no_optimization(self, img_f):

        # rutea según el orden del id
        x0 = xf = int(self.path.targetX.iloc[0])
        y0 = yf = int(self.path.targetY.iloc[0])

        for _, row in self.path.iterrows():
            
            x1 = int(row.targetX)
            y1 = int(row.targetY)
            
            if self.draw_rout: cv2.line(img_f, (x0, y0), (x1, y1), self.color_route, self.route_line_width) 
            x0 = x1
            y0 = y1

            if self.draw_targ: img_f = self.draw_target(img_f, x1, y1)
            
        if self.draw_rout: cv2.line(img_f, (x0, y0), (xf, yf),self.color_route, self.route_line_width)

        return img_f, [i for i in range(len(self.path))]

    def generate_matdist(self):
        # calcula la matriz de distancias

        n = len(self.path)
        adj_mat = np.ones((n,n)) * np.inf  # genera una matriz adj_mat llena de infinito
        for i in range(n):
            for j in range(i, n):
                if (i!=j):
                    point1 = np.array([self.path.iloc[i].targetX, self.path.iloc[i].targetY])
                    point2 = np.array([self.path.iloc[j].targetX, self.path.iloc[j].targetY])
                    dist = np.linalg.norm(np.subtract(point1, point2))
                    adj_mat[i][j] = adj_mat[j][i] = dist     # calcula la distancia euclidiana

        return adj_mat

    def greedy(self, img_f):
        
        mat = self.generate_matdist()

        # GREEDY

        #mat = adj_mat.copy()
        g_path = []
        g_path.append(0)
        i = 0
        d = 0

        while (np.min(mat)<np.inf):
            j = np.where(mat[i]==np.min(mat[i]))[0][0]
            d = d + np.min(mat[i])
            mat[i, :] = mat[:, i] = np.inf
            g_path.append(j)
            i = j

        g_path.append(0)

        img_laser = self.draw_route(img_f, g_path)
        
        return img_laser, g_path, d
    
    def draw_route(self, img_f, opt_path):
        
        
        img_laser = img_f.copy()
        ##### CORRECCION
        
        x0 = xf = int(self.path.iloc[opt_path[0]].targetX) 
        y0 = yf = int(self.path.iloc[opt_path[0]].targetY)

        for i in range(len(opt_path)):

            x1 = int(self.path.iloc[opt_path[i]].targetX)
            y1 = int(self.path.iloc[opt_path[i]].targetY)

            if self.draw_rout: cv2.line(img_laser, (x0, y0), (x1, y1), self.color_route, self.route_line_width) 
            
            if self.draw_targ == 1: img_laser = self.draw_target(img_laser, x1, y1)
            
            x0 = x1
            y0 = y1

        cv2.line(img_laser, (x0, y0), (xf, yf), self.color_route, self.route_line_width)

        ##### CORRECCION
        return img_laser

    def local_search(self, img_f):

        #  local search 

        _, g_path, d = self.greedy(self.img_f)

        s = []
        for i in range(len(g_path)-1):
            s.append((g_path[i],g_path[i+1]))
        
        sg = (s, d)

        adj_mat = self.generate_matdist()

        ls = ACLS(adj_mat, len(sg), 1, 100, 0.95, 1, 1)     

        sp = ls.local_search(sg)

        ls_path = []

        for i in range(len(sp[0])):
            ls_path.append(sp[0][i][0])

        ls_path.append(0)

        img_laser = self.draw_route(img_f, ls_path)

        return img_laser, ls_path

    def ant_colony_optimization(self, img_f):

        # ANT COLONY OPTIMIZATION

        adj_mat = self.generate_matdist()

        ant_colony_ls = ACLS(adj_mat, 10, 5, 50, 0.95, 1, 1)        

        sp = ant_colony_ls.run()

        aco_path = []

        for i in range(len(sp[0])):
            aco_path.append(sp[0][i][0])

        aco_path.append(0)

        img_laser = self.draw_route(img_f, aco_path)

        return img_laser, aco_path

    ##### CORRECCION
    def route(self, d_route):

        self.draw_rout = d_route
        ##### CORRECCION

        # Eliminar duplicados 
        self.path = self.path.drop_duplicates(['targetX','targetY'])
        
        if self.route_opt == 1:
            img, opt_path = self.no_optimization(self.img_f)
        if self.route_opt == 2:
            img, opt_path, _ = self.greedy(self.img_f)
        if self.route_opt == 3:
            #local search
            img, opt_path = self.local_search(self.img_f)
        if self.route_opt == 4:
            #ant colony optimization
            img, opt_path = self.ant_colony_optimization(self.img_f)

        return img, opt_path
          
    def draw_target(self, img, x, y):

        c = int(self.target_size/2)   
        
    
        cv2.circle(img, (x, y), self.target_center_size, self.color_target, -1)
        cv2.line(img, (x, y-c), (x, y+c), self.color_target, self.target_line_width) 
        cv2.line(img, (x-c, y), (x+c, y), self.color_target, self.target_line_width) 

        return img

    def draw_insect_info(self, status=0):
        ###### CORRECCION
        # recorre el dataset y redibuja los bounding boxes
        self.img_f = self.img_orig.copy()                          
        for _, row in self.drosophila.iterrows():
            if row.state=="classified":
                self.img_f = self.image_addBoundingbox(self.img_f, row.x, row.y, row.state, True, row.obj_id, self.y_text, row.sexf, row.conf)
            elif row.state=="eliminado":
                pass
            else:
                self.img_f = self.image_addBoundingbox(self.img_f, row.x, row.y, row.state, True, row.obj_id, self.y_text)

            if row.state!="eliminado":
                if self.draw_targ and (row.targetX>0 or row.targetY>0) and (row.sexf!='m'):
                    self.img_f = self.draw_target(self.img_f, row.targetX, row.targetY)    

        
        if (status==3) and (self.draw_rout) and (self.path.obj_id.count()>0):    
            self.img_f = self.route(self.draw_rout)
        ###### CORRECCION
            
        return self.img_f

    def change_insect(self, id, data, status):
        # cambia un parámetro del insecto según el id y el data
        if (data=='m'):
            self.drosophila.loc[self.drosophila.obj_id==id, "sexf"] = 'm'
        elif (data=='f'):
            self.drosophila.loc[self.drosophila.obj_id==id, "sexf"] = 'f'
        else:
            self.drosophila.loc[self.drosophila.obj_id==id, "state"] = data
        # redibuja el canvas
        img = self.draw_insect_info(status)
        return img
