# Proyecto MACTI 2.0
#Por: Brenda Lizette De la Rosa Espinoza

from ipywidgets import Layout, interact, IntSlider
import ipywidgets as widgets
from IPython.display import display, HTML
import os
from sys import platform
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import seaborn as sns
from matplotlib import animation, rc
from time import time


class SimuladorGeo:
    """Clase que contiene los métodos para el funcionamiento y visualización de resultados de un simulador de convección termohalina"""
    def __init__(self, rayleigh = 100, radio=10, angulo=10, pasos=1000, sor_param= 1.2, solver=1 ):
        """Construtor de la clase que recibe como argumento los parámetros de entrada. si no se definen inicialmente se generan los parametros por default"""
        self.rayleigh = rayleigh
        self.radio = radio
        self.angulo = angulo
        self.pasos = pasos
        self.sor_param= sor_param
        self.solver= solver 
       
   
    def IniciarEjercicio(self):
        """Método que permite seleccionar el tipo de solucionador que el usuario desea correr"""
        
        print('Elige el tipo de solucionador que deseas correr:\nEscribe 1 para Gradiente Conjugado\nEscribe 2 para Gauss-Seidel\nEscribe 3 para SOR.\n')
        
        solver= int(input('Solucionador: '))
        self.solver=solver
        
        if solver == 1 or solver == 2:
            print('Define los parametros de entrada para generar la simulación\n')
            self.interfazGrafica()
            
            
        elif solver == 3:
            print('Define los parametros de entrada para generar la simulación, incluyendo el parámetro de relajación\n')
            self.interfazGrafica()
            
         
        else:
            print('Vuelve a intentarlo')
            
        return

    def interfazGrafica(self):
        """Método que permite al usuario ingresar los parámetros de entrada para la simulación de manera dinámica"""
        ## Selecciona el numero de Rayleigh
        rayleigh = widgets.FloatSlider(
            value=100,
            min=0,
            max=250.0,
            step=1.0,
            description='',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
            layout=widgets.Layout(width='100%'))

        ## Selecciona el radio de Bouyancy
        radio = widgets.FloatSlider(
            value=-10.0,
            min=-10.0,
            max=10.0,
            step=1.0,
            description='',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
            layout=widgets.Layout(width='100%'))

        ## Selecciona el ángulo de inclinacion en grados
        grados = widgets.IntSlider(
            value=10,
            min=0,
            max=30,
            step=1,
            description='',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            layout=widgets.Layout(width='100%'))

        ## Número de pasos de tiempo
        pasos = widgets.IntSlider(
            value=1000,
            min=100,
            max=100000,
            step=100,
            description='',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            layout=widgets.Layout(width='100%'))

         ## Selecciona el parametro de relajación if solver == 3
        sor_param= widgets.FloatSlider(
                value=1.2,
                min=0.1,
                max=1.9,
                step=0.1,
                description='',
                disabled=False,
                continuous_update=False,
                orientation='horizontal',
                readout=True,
                readout_format='.1f',
                layout=widgets.Layout(width='100%'))
        
        button = widgets.Button(
            description='Confirma cambios',
            disabled=False,
            button_style='success',
            tooltip='Click me',
            icon='check',
            layout = widgets.Layout(width='40%',
                                    margin='20px 0px 0px 0px'))

        output = widgets.Output()
        

        titulo = widgets.HTML(
            value="<h3>Definición de parámetros</h3>",
            layout = widgets.Layout(margin='0px 0px 30px 0px'))

        parametro1 = widgets.Label(value= "Número de rayleigh")
        parametro2 = widgets.Label(value= "Relación de flotación")
        parametro3 = widgets.Label(value= "Inclinación del ángulo en grados")
        parametro4 = widgets.Label(value= "Número de pasos de tiempo")
        parametro5 = widgets.Label(value= "Parámetro de relajación SOR")
        
        if self.solver == 1 or self.solver == 2:
            def on_button_clicked(b):
                with output:
                    button.disabled = True
                    self.rayleigh = rayleigh.value
                    self.radio = radio.value
                    self.angulo = grados.value
                    self.pasos = pasos.value
                    button.disabled = False 
                    self.generaInput() 
            button.on_click(on_button_clicked)

            items = [titulo, parametro1, rayleigh, parametro2, radio, parametro3, grados, parametro4, pasos, button]
         
        elif self.solver == 3:
            def on_button_clicked(b):
                with output:
                    button.disabled = True
                    self.rayleigh = rayleigh.value
                    self.radio = radio.value
                    self.angulo = grados.value
                    self.pasos = pasos.value
                    self.sor_param = sor_param.value
                    button.disabled = False 
                    self.generaInput()
            button.on_click(on_button_clicked)

            items = [titulo, parametro1, rayleigh, parametro2, radio, parametro3, grados, parametro4, pasos, parametro5, sor_param, button]

        box_layout = widgets.Layout(display='flex',
                            flex_flow='column',
                            align_items='center',
                            padding = '5%',
                            border='solid',
                            width='60%')

        pantallaselec = widgets.GridBox(items, layout = box_layout)

        display(pantallaselec, output)
    
        
    def generaInput(self):
        """Método que a partir de los parámetros definidos, genera un archivo .inp que sirve como input del simulador"""
        
        f= open("in_param.inp","w+")
        
        if self.solver == 1 or self.solver == 2:
            
            f.write("Input parameters GEOThermohaline Simulator:\nRayleigh number between 0 and 250:\nRa="+str(self.rayleigh)+"\nBuoyancy ratio between -10 and 10:\nBR="+str(self.radio)+"\nInclination angle in degrees (integer between 0 and 30)\nAngle (degrees)="+str(self.angulo)+"\nNumber of time steps (multiples of 100, max 100000):\nTime steps="+str(self.pasos)+'\nSelected solver (1: Conjugate gradient; 2: Gauss-Seidel; 3: SOR)\nsolver='+str(self.solver))
            f.close()
            print('Se escribió correctamente el archivo de entrada con los siguientes parámetros: \n\nNúmero de Rayleigh (Ra): '+str(self.rayleigh)+'\nRelación de flotación (N): '+str(self.radio)+'\r\nÁngulo de inclinación (θ): '+str(self.angulo)+'°'+'\nNúmero de pasos de tiempo (𝑛Δ𝑡): '+str(self.pasos)+'\nSolucionador: '+str(self.solver))
        
        elif self.solver == 3:
            f.write("Input parameters GEOThermohaline Simulator:\nRayleigh number between 0 and 250:\nRa="+str(self.rayleigh)+"\nBuoyancy ratio between -10 and 10:\nBR="+str(self.radio)+"\nInclination angle in degrees (integer between 0 and 30)\nAngle (degrees)="+str(self.angulo)+"\nNumber of time steps (multiples of 100, max 100000):\nTime steps="+str(self.pasos)+'\nSelected solver (1: Conjugate gradient; 2: Gauss-Seidel; 3: SOR)\nsolver='+str(self.solver)+'\nParámetro de relajación SOR (entre 0.1 Y 1.9)\nsor_param='+str(self.sor_param))
            f.close()
            print('Se escribió correctamente el archivo de entrada con los siguientes parámetros: \n\nNúmero de Rayleigh (Ra): '+str(self.rayleigh)+'\nRelación de flotación (N): '+str(self.radio)+'\r\nÁngulo de inclinación (θ): '+str(self.angulo)+'°'+'\nNúmero de pasos de tiempo (𝑛Δ𝑡): '+str(self.pasos)+'\nSolucionador: '+str(self.solver)+'\nParámetro de relajación SOR: '+str(self.sor_param))

        BtnEjecuta= widgets.Button(
            description='Ejecuta Simulador',
            disabled=False,
            button_style='success',
            tooltip='Click me',
            icon='check',
            layout = widgets.Layout(width='40%',
                                    margin='20px 0px 0px 0px'))
        def button_clicked(b):
            self.ejecutaSimulador()
        
        BtnEjecuta.on_click(button_clicked)
        display(BtnEjecuta)

        
    def ejecutaSimulador(self):
        """Método que ejecuta el simulador a segun el sistema operativo"""
        start_time = time()
        
        if platform == "darwin":
          print('Comienza la simulación')
          os.system('executables/GEOThermohaline_macos')
        elif platform == "linux":
          print('Comienza la simulación')
          os.system('executables/GEOThermohaline_linux')         
        elif platform == "win32":
            print('Lo sentimos, aún no tenemos versión para windows')
        
        elapsed_time = time() - start_time
        print("Simulación concluida. Tiempo transcurrido: %.5f segundos."  % elapsed_time)
        
        self.graficaSolucion()
    
        
    def graficaSolucion(self):
        """Método que grafica los resultados de la simulación: el Tiempo vs Numero de Nusselt, Sherwood y Saturación así como el número de iteraciones para las ecuaciones de velocidad, masa y calor"""
        
        fileObj = open('output/run_log.txt',"r")
        lines = fileObj.readlines()
        A = []
        del lines[0:6]
        for line in lines:
            A.append(line.split())
    
        datos = np.array(A, dtype=np.float32)
        
        plt.rcParams['axes.grid'] = True
        
        BtnGrafica= widgets.Button(
            description='Grafica Nu(t), Sh(t) y Sa(t)',
            disabled=False,
            button_style='success',
            tooltip='Click me',
            icon='check',
            layout = widgets.Layout(width='40%',
                                    margin='20px 0px 0px 0px'))
         
        BtnDesempeño= widgets.Button(
            description='Grafica el desempeño del solver',
            disabled=False,
            button_style='success',
            tooltip='Click me',
            icon='check',
            layout = widgets.Layout(width='40%',
                                    margin='20px 0px 0px 0px'))
      
        
        def button_clicked(b):
      
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16,5))
        
            ax1.plot(datos[:,0], datos[:,1], '-', color='skyblue', linewidth=3)
            ax1.set_xlabel('Tiempo')
            ax1.set_ylabel('Número de Nusselt')
        
            ax2.plot(datos[:,0], datos[:,2]*(-1), '-', color='skyblue', linewidth=3)
            ax2.set_xlabel('Tiempo')
            ax2.set_ylabel('Número de Sherwood')
        
            ax3.plot(datos[:,0], datos[:,3], '-', color='skyblue', linewidth=3)
            ax3.set_xlabel('Tiempo')
            ax3.set_ylabel('Saturación')
            
            resultados=plt.show()
            
            display(BtnDesempeño)
            
            return resultados
  
        
        BtnGrafica.on_click(button_clicked)
        display(BtnGrafica)
        
        def buttonClickedDesempeño(c):
            
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16,5))
            
            ax1.plot(datos[:,0], datos[:,4], '-', color='springgreen', linewidth=3)
            ax1.set_xlabel('Tiempo')
            ax1.set_ylabel('Iteraciones Ec. de Calor')
        
            ax2.plot(datos[:,0], datos[:,5], '-', color='springgreen', linewidth=3)
            ax2.set_xlabel('Tiempo')
            ax2.set_ylabel('Iteraciones Ec. de Masa')
        
            ax3.plot(datos[:,0], datos[:,6], '-', color='springgreen', linewidth=3)
            ax3.set_xlabel('Tiempo')
            ax3.set_ylabel('Iteraciones Ec. de Velocidad')
        
            desempeño=plt.show
            
            return desempeño
        
        BtnDesempeño.on_click(buttonClickedDesempeño)
      
        
    def graficaSimulacion(self):
        """Método que lee los datos de concentración y temperatura y genera las gráficas de la simulación"""
        datac=np.loadtxt('output/concentration.txt', dtype='float', skiprows=5)
        
        steps= int(self.pasos/100)
        
        conc=np.zeros(((steps,102,102)), dtype= np.float32)
        for k in range(steps):
            conc[k,:,:]=datac[(103*k)+1: (103*k)+103, 1:]
    
        y1=np.zeros((102,102),dtype= np.float32)
        for j in range(102):
            y1[:,j]=datac[0,1:]


        x1=np.zeros((102,102), dtype= np.float32)
        for i in range(102):
            x1[i,:]=datac[0,1:]
        
        datat=np.loadtxt('output/temperature.txt', dtype='float', skiprows=5)

        temp=np.zeros(((steps,102,102)), dtype= np.float32)
        for k in range(steps):
            temp[k,:,:]=datat[(103*k)+1: (103*k)+103, 1:]
    
    
        y2=np.zeros((102,102),dtype= np.float32)
        for j in range(102):
            y2[:,j]=datat[0,1:]
    
    
        x2=np.zeros((102,102), dtype= np.float32)
        for i in range(102):
            x2[i,:]=datat[0,1:]
        
        print('leyendo datos de la simulación...'+'\nGenerando las gráficas de la simulación')
        
        plt.style.use('ggplot')
        
        mycolors= sns.blend_palette(['blue', 'orange' ,'yellow'], as_cmap=True)
        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,6))
        plt.suptitle('Ra='+str(self.rayleigh)+'  N='+str(self.radio)+'  θ='+str(self.angulo)+' Δt='+str(self.pasos), fontsize=10, fontweight='bold')
        plt.subplots_adjust(left=0.13, right=0.93, bottom= 0.27)
        
        cax1 = ax1.pcolormesh(x1, y1, conc[1,:,:],
                      vmin=0, vmax=1, cmap= mycolors, 
                      shading='gouraud')
        fig.colorbar(cax1, ax=ax1)
        ax1.set_title("Concentración",fontsize=12, pad=10)


        cax2 = ax2.pcolormesh(x2, y2, temp[1,:,:],
                    vmin=0, vmax=1, cmap='plasma', 
                    shading='gouraud')
        fig.colorbar(cax2, ax=ax2)
        ax2.set_title("Temperatura", fontsize=12, pad=10)
        plt.close(fig)
        
        cax=[cax1, cax2]
        
        ## Función que genera una animación para vizualisar la simulación
        def animate(frame):
            cax[0].set_array(conc[frame,:,:].flatten())
            cax[1].set_array(temp[frame,:,:].flatten())
        
        anim= animation.FuncAnimation(fig, animate, frames=steps, interval=100)
        #video=HTML(anim.to_html5_video()) #changed on 17 feb 2024
        video=HTML(anim.to_jshtml())
        return video
