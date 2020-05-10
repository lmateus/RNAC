#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 18:40:56 2018

@author: leonardo
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylatex as pl
from pylatex import Document, Section, Figure, NoEscape, Math, Subsection, Tabular, TikZ, Axis, \
    Plot, Matrix, Alignat, LongTable,MultiColumn

class ErrorEstacion2():

    def __init__(self,nombre):
        
        self.name = nombre
        self.errores()
          
    def errores(self):
		       
        datos = pd.read_csv("Aceleraciones.csv",header=0)
        df = pd.DataFrame(datos)

        #Filtra el listado de acuerdo al nombre de la estacion
        
        estacion = df[df['Nombre Estación'].str.contains(self.name)]
                
        PGA_00 = estacion[estacion['Localizador'] == 00]
        PGA_E00 = PGA_00["PGA EW [cm/s^2]"].max()
        PGA_N00 = PGA_00["PGA NS [cm/s^2]"].max()
        PGA_Z00 = PGA_00["PGA Z [cm/s^2]"].max()
        
        PGA_10 = estacion[estacion['Localizador'] == 10]
        PGA_E10 = PGA_10["PGA EW [cm/s^2]"].max()
        PGA_N10 = PGA_10["PGA NS [cm/s^2]"].max()
        PGA_Z10 = PGA_10["PGA Z [cm/s^2]"].max()
        
        #Calcula el error por componente
        
        if (PGA_E00 == 0 or PGA_E10 ==0):
            self.error_E = np.nan
        else:
            self.error_E = abs(round((100*(PGA_E10 - PGA_E00)/PGA_E10),2))
            
        if (PGA_N00 == 0 or PGA_N10 ==0):
            self.error_N = np.nan
        else:            
            self.error_N = abs(round((100*(PGA_N10 - PGA_N00)/PGA_N10),2))
        
        if (PGA_Z00 == 0 or PGA_Z10 ==0):
            self.Z = np.nan
        else:
            self.error_Z = abs(round((100*(PGA_Z10 - PGA_Z00)/PGA_Z10),2))
        
        self.er=[self.name,self.error_E,self.error_N,self.error_Z]
        
       
class Calcula():
    
    def __init__ (self,nombre):
        self.name = nombre
        
    def figura(self):
        
        nombre_estacion = np.array([
                                   ["APAC","Apartado, Antioquia, Colombia"],
                                   ["ARMEC","Armenia, Quindio"],
                                   ["ARGC",'Ariguani, Magdalena, Colombia'],
                                   ["BAR2","Barichara, Santander, Colombia"],
                                   ["SOL","Bahia Solano, Choco, Colombia"],
                                   ["BAR2","Barichara, Santander, Colombia"],
                                   ["DBB",'Dabeiba, Antioquia, Colombia'],
                                   ["DRL04","Patio Geologia"],
                                   ["GUA","San Jose del Guaviare, Guaviare, Colombia"],
                                   ["GUY2C",'Villamaria, Caldas, Colombia'],
                                   ["JAMC","Jamundi, Valle del Cauca, Colombia"],                                   
                                   ["OCA",'Ocana, Norte de Santander, Colombia'],
                                   ["ORTC",'Ortega, Tolima, Colombia'],
                                   ["PAL","San Jose del Palmar, Choco, Colombia"],
                                   ["PAM","Pamplona, Norte de Santander, Colombia"],
                                   ["ROSC",'El Rosal, Cundinamarca, Colombia'],
                                   ["SJC","San Jacinto, Bolivar, Colombia"],
                                   ["SPBC",'San Pablo de Borbur, Boyaca, Colombia'],
                                   ["TAM",'Tame, Arauca, Colombia'],
                                   ["URE", 'San Jose de Ure, Cordoba, Colombia'],
                                   ["VIL",'Villavicencio, Meta, Colombia'],
                                   ["YPLC",'Yopal, Casanare, Colombia'],
                                   ["YOT","Yotoco, Valle, Colombia"],
                                   ["ZAR","Zaragoza, Antioquia, Colombia"],
                                   ])

        errorEW = np.array([])
        errorNS = np.array([])
        errorZ = np.array([])
        
        numero_estaciones=len(nombre_estacion)

        for i in range (numero_estaciones):
           
            errorEst = ErrorEstacion2(nombre_estacion[i,1])
                        
            errorEW = np.append(errorEW,errorEst.error_E)
            errorNS = np.append(errorNS,errorEst.error_N)
            errorZ = np.append(errorZ,errorEst.error_Z)
          
        #print(errorEW,errorNS,errorZ)
        
        station = pd.DataFrame(nombre_estacion,columns=["Nombre estacion","estacion"])
        
        ErrorEW = pd.DataFrame(errorEW,columns=["Error EW"])
        ErrorNS = pd.DataFrame(errorNS,columns=["Error NS"])
        ErrorZ = pd.DataFrame(errorZ,columns=["Error Z"])
        
        df=pd.concat([station,ErrorEW,ErrorNS,ErrorZ], axis=1)
                
        df_sin_nan = df.dropna(how='any')
        df_sin_nan.plot.bar(x="Nombre estacion",width=0.7)
        #df.plot.bar(x="Nombre estacion",width=0.8)
        plt.ylabel("Error (%)")
        plt.grid()
        plt.title(self.name)
        plt.plot()
        
        print(df_sin_nan)

class GenerarDocumento():
    
    def __init__(self, fname, mag,fecha):
        
        self.fname=fname
        self.magnitud=mag
        self.fecha=fecha
        
    def documento(self):
        
        x = Calcula(self.fname)
                
        width = r'1\textwidth'
        geometry_options = {"tmargin": "1cm", "lmargin": "2cm","head": "40pt"}
        doc = Document(self.fname, geometry_options=geometry_options)
        
        doc.append('''Se presenta un análisis de las aceleraciones registradas en el sismo de {0} de magnitud {1} en la fecha {2}.
                   '''.format(self.fname,self.magnitud,self.fecha))
    
    
        with doc.create(Section('Análisis de errores de aceleraciones')):
            doc.append('''Se estiman los errores entre la aceleración determinada con un sensor de aceleración y uno de velocidad
                       con la ecuación (1):''')
            
            with doc.create(Alignat(numbering=2, escape=False)) as agn:
                (agn.append(r"Error=\frac{PGA_{10}-PGA_{00}}{PGA_{10}} "))
    
            with doc.create(Figure(position='htbp')) as plot:
                
                x.figura()
                plot.add_plot(width=NoEscape(width))
                plot.add_caption('Errores relativos de aceleraciones.')
                     
        doc.generate_pdf(clean_tex=False)
    

d1= GenerarDocumento("LOS SANTOS", 2, "2018-01-05")
d1.documento()

