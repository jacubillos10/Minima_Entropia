#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

numDato=4;
elSeniorArchivo="OGLE-LMC-CEP-0004.dat";
datos=np.genfromtxt(elSeniorArchivo,delimiter=' ');
ts=datos[:,0];
u_s=datos[:,1];
tini=ts[0];
tfin=ts[-1]-ts[0];
def transformar_ts(tp,t_datos,t0):
	phis=[];
	for i in range(len(t_datos)):
		phi=(t_datos[i]-t0)/tp;
		if phi>1:
			phiN=phi-int(phi);
		else:
			phiN=phi;
		#fin if
		phis.append(phiN);
	#fin for
	resp=np.array(phis);
	return resp
#fin transformar tiempos  ***---> check :) ... bueno casi... el orden va bien pero veo valores repetidos (parece que ya se corrigió el problema)

def generar_grilla(dimensiones,phis,us):
	N=len(phis);
	Grilla=np.zeros((dimensiones[0],dimensiones[1]));
	phis_front=np.linspace(0,1,dimensiones[0]+1);
	us_front=np.linspace(min(us),max(us),dimensiones[1]+1);
	for n in range(len(phis)):
		for i in range(dimensiones[0]):
			if phis[n]>=phis_front[i] and phis[n]<phis_front[i+1]:
				indice_i=i;
			#fin if
		#fin for
		for j in range(dimensiones[1]):
			if us[n]>=us_front[j] and us[n]<us_front[j+1]:
				indice_j=j;
			#fin if
		#fin for
		Grilla[indice_i,indice_j]=Grilla[indice_i,indice_j]+1;
	#fin for
	resp=(1/N)*Grilla
	return resp
#fin generar grilla  ***---> chack :) siempre que lo corro la suma de los elementos suma 400. 


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

#PARTE 3: Haga la gráfica de entropías en función de los periodos
#Es decir meta todo el sancocho anterior en un ciclo for

def generar_grafica(lim_periodos,Nperiodos,t_datos,t0,u_s,dimensiones):
	losPeriodos=np.linspace(lim_periodos[0],lim_periodos[1],Nperiodos);
	S=[];
	for i in range(Nperiodos):
		phis=transformar_ts(losPeriodos[i],t_datos,t0);
		cuadro=generar_grilla(dimensiones,phis,u_s);
		entropia=entropitometro(cuadro);
		S.append(entropia);
	#fin for 
	S=np.array(S);
	resp=[losPeriodos,S];
	return resp
#fin generar grafica
dimGrilla=[8,8];
tp_prueba=3.3;
phis=transformar_ts(tp_prueba,ts,ts[0]);
grilla1=generar_grilla(dimGrilla,phis,u_s);
entropia_muestra=entropitometro(grilla1);
print("La entropía en ",tp_prueba," es de ",entropia_muestra);
print("********************************************************************");
print("El número de la estrella procesada fue: ",numDato);
print("Esperar no un poquito a que se calculen las entropías (son muchas!)");

tpini=0.4;
tpfin=200;
PhisyS=generar_grafica([tpini,tpfin],3000,ts,tini,u_s,dimGrilla);
tps=PhisyS[0];
entropias=PhisyS[1];
fig1=plt.figure();
ax1=fig1.add_subplot(111);
ax1.plot(tps,entropias);
tituloGrafica="Entropía vs periodo, datos número :"+str(numDato)+" grilla de "+str(dimGrilla[0])+"x"+str(dimGrilla[1]);
ax1.set_title(tituloGrafica);
ax1.set_xlabel("Periodo en días");
ax1.set_ylabel("Entropía [adimensional]");
nombreFoto="Gráfica_entropía_datos_"+str(numDato)+".png";
plt.savefig(nombreFoto);
print("Listo !!!!!!"); 
print("... por favor abra el archivo de la gráfica");
print("El valor de la entropia mínima fue de : ", min(entropias));
indice=entropias.argmin();
print(indice);
print("El valor del periodo correspondiente a esa entripía: ",tps[indice]);
phis_def=transformar_ts(tps[indice],ts,tini);
phi_def_2=phis_def+1;
fig2=plt.figure();
ax1=fig2.add_subplot(111);
phis_T=np.r_[phis_def,phi_def_2];
u_sN=np.r_[u_s,u_s];
ax1.scatter(phis_T,u_sN);
tituloGrafica2="Curvas de luz, datos número :"+str(numDato);
ax1.set_title(tituloGrafica2);
ax1.set_xlabel("t_adimensional (t-t0)/tp");
ax1.set_ylabel("Variable u(t)");
ax1.set_ylim(ax1.get_ylim()[::-1]);
nombreFoto2="Curva_de_luz_datos_"+str(numDato)+".png";
plt.savefig(nombreFoto2);
print("CUrvas de luz generadas");
