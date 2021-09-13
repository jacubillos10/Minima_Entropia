#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv

#Coloque aquí el tipo de estrella con el que se va a trabajar. OPCIONES= 'Cefeida', 'RR_Lyrae', 'BinariaECL'.
tipo_estrella='Cefeida';

#Importar los números de las estrellas desde el archivo csv:
ID_estrellas=np.loadtxt('numero_estrellas.csv',delimiter=',',dtype='str', skiprows=1);

vecCep=ID_estrellas[:,0];
vecRRLyr=ID_estrellas[:,1]; 
vecECL=ID_estrellas[:,2];

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if tipo_estrella=='Cefeida' or tipo_estrella==1:
	label_path='Datos/'+'1_Cefeidas'+'/I/OGLE-LMC-CEP-';
	numero_estrella=vecCep;
elif tipo_estrella=='RR_Lyrae' or tipo_estrella==2:
	label_path='Datos/'+'2_RR_Lyrae'+'/I/OGLE-LMC-RRLYR-';
	numero_estrella=vecRRLyr;
else:
	label_path='Datos/'+'3_BinariasEclipsantes'+'/I/OGLE-LMC-ECL-';
	numero_estrella=vecECL;
#fin if 
extension='.dat';

#-----------------------verificar que existen los archivos--------------------------
# ~ for k in range(len(numero_estrella)):
	# ~ elSeniorArchivo=label_path+numero_estrella[k]+extension;
	# ~ datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
	
# ~ #fin for 
# ~ print("EXISTEN");
#---------------------------------------------------------------------------------------------------
vint=np.vectorize(np.int);
def transformar_ts(tp,t0,t_datos):
	phi_raw=(1/tp)*(t_datos-t0);
	phi=phi_raw-vint(phi_raw);
	return phi;
# fin transformar phis

def generar_grilla(dimensiones,phis,us):
	N=len(phis);
	Grilla=np.zeros((dimensiones[0],dimensiones[1]));
	phis_front=np.linspace(0,1,dimensiones[0]+1);
	us_front=np.linspace(min(us),max(us),dimensiones[1]+1);
	for i in range(dimensiones[0]):
		for j in range(dimensiones[1]):
			cond1=phis>=phis_front[i];
			cond2=phis<phis_front[i+1];
			cond3=us>=us_front[j];
			if j==dimensiones[1]-1:
				cond4=us<=us_front[j+1];
			else:
				cond4=us<us_front[j+1];
			#fin if
			condicion=cond1*cond2*cond3*cond4;
			Grilla[i,j]=len(condicion[condicion==True]);
		#fin for 
	#fin for
	resp=(1/N)*Grilla;
	return resp;
#fin generar grilla

def entropitometro(Grilla):
	largo=len(Grilla[0,:]);
	alto=len(Grilla[:,0]);
	Suma=0;
	for i in range(alto):
		for j in range(largo):
			if Grilla[i,j]==0:
				pass;
			else:
				Entropia_ij=-Grilla[i,j]*np.log(Grilla[i,j]);
				Suma=Suma+Entropia_ij;
			#fin if
		#fin for
	#fin for
	resp=(1/np.log(largo*alto))*Suma;
	return resp
#fin hallar entropia

def generar_grafica(lim_periodos,Nperiodos,t_datos,t0,u_s,dimensiones):
	losPeriodos=np.linspace(lim_periodos[0],lim_periodos[1],Nperiodos);
	S=[];
	for i in range(Nperiodos):
		phis=transformar_ts(losPeriodos[i],t0,t_datos);
		cuadro=generar_grilla(dimensiones,phis,u_s);
		entropia=entropitometro(cuadro);
		S.append(entropia);
	#fin for 
	S=np.array(S);
	resp=[losPeriodos,S];
	return resp
#fin generar grafica

lista_estrellas=[];
lista_periodos=[];
lista_entropias=[];
for k in range(len(numero_estrella)):
	elSeniorArchivo=label_path+numero_estrella[k]+extension;
	datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
	t_dat=datos[:,0];
	us=datos[:,1];
	tini=t_dat[0];
	dimGrilla=[16,16];
	tpini=[2.2293,3.294,11.2475,4.80,3.10,0.8,2.06,3.5325,2.27,5.912,1,4.80,3.645,3.21,5.271,1.865,1.95,4.08,3.5705,2.86,3.58,4.096,0.8,0.8,2.173];
	tpfin=[2.2297,3.296,11.2600,4.82,.315,1,2.08,3.5335,2.30,5.915,1.5,4.85,3.650,3.22,5.274,1.870,1.96,4.10,3.5720,2.88,3.60,4.100,1,0.9,2.175];
	Finura=3000;
	PhisyS=generar_grafica([tpini[k],tpfin[k]],Finura,t_dat,tini,us,dimGrilla);
	tps=PhisyS[0];
	entropias=PhisyS[1];
	fig1=plt.figure();
	ax1=fig1.add_subplot(111);
	ax1.plot(tps,entropias);
	tituloGrafica="Entropía vs periodo de la estrella "+tipo_estrella+"#: "+numero_estrella[k]+" grilla de "+str(dimGrilla[0])+"x"+str(dimGrilla[1]);
	#ax1.set_title(tituloGrafica);
	ax1.set_xlabel("Periodo en días");
	ax1.set_ylabel("Entropía [adimensional]");
	nombreFoto="Gráfica_entropía_datos_estrella_"+tipo_estrella+"-"+numero_estrella[k]+".png";
	plt.savefig(nombreFoto);
	print("Gráfica de entropia en función de periodo generada"); 
	print("El valor de la entropia mínima fue de : ", min(entropias));
	indice=entropias.argmin();
	print("la posición del periodo donde está la entropía mínima es: ",indice);
	print("El valor del periodo correspondiente a esa entropía: ",tps[indice]);
	phis_def=transformar_ts(tps[indice],tini,t_dat);
	phi_def_2=phis_def+1;
	fig2=plt.figure();
	ax1=fig2.add_subplot(111);
	phis_T=np.r_[phis_def,phi_def_2];
	u_sN=np.r_[us,us];
	ax1.scatter(phis_T,u_sN);
	tituloGrafica2="Curvas de luz de la estrella:"+tipo_estrella+"#: "+numero_estrella[k];
	#ax1.set_title(tituloGrafica2);
	ax1.set_xlabel("fase");
	ax1.set_ylabel("Magnitud M_I");
	ax1.set_ylim(ax1.get_ylim()[::-1]);
	nombreFoto2="Curva_de_luz_de_"+tipo_estrella+"-"+numero_estrella[k]+".png";
	plt.savefig(nombreFoto2);
	print("Curvas de luz de la estrella "+tipo_estrella+"-"+numero_estrella[k]+" generada");
	LabelEstrella="Estella_"+tipo_estrella+"_"+numero_estrella[k]+"_ME";
	lista_estrellas.append(LabelEstrella);
	lista_periodos.append(tps[indice]);
	lista_entropias.append(min(entropias));
#fin for 
lista_estrellas=np.array(lista_estrellas);
lista_periodos=np.array(lista_periodos);
lista_entropias=np.array(lista_entropias);
datos_exportacion=np.c_[lista_estrellas,lista_periodos,lista_entropias];
encabezado=['Nombre_estrella','PeriodoLS [dias]','Entropía'];

with open('periodos_hallados.csv', 'w', encoding='UTF8', newline='') as f:
	writer=csv.writer(f);
	writer.writerow(encabezado);
	writer.writerows(datos_exportacion);
#fin with 
