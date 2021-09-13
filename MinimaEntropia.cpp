#include <iostream>
#include <fstream>
#include <cassert>
#include <cmath>
#include <algorithm>
#include <cstdlib>

double hallar_entropia(double tp_prueba, int dim_grilla[2], int N_datos, double t_dat[], double u_dat[]);
int main(int argc, char *argv[])
{
	std::string nombre_archivo = argv[1];
	double tp_menor = atof(argv[2]);
	double tp_mayor = atof(argv[3]);
	int dimension1 = atoi(argv[4]);
	int dimension2 = atoi(argv[5]);
	int Finura = atoi(argv[6]);
	int dimGrilla[2] = {dimension1,dimension2};
	std::ifstream read_file(nombre_archivo);
	assert(read_file.is_open());
	int N_filas=0;
	// Bien... hagamos lo siguiente. Es una chambonada pero va a funcionar. Hagamos una lectura del archivo primero y anotemos la cantidad de filas que tiene con un while
	// Una vez tengamos ese número vamos a escribir lo que hay en ese archivo en las variables t, u. 
	double tk, uk, delta_uk;
	while(!read_file.eof())
	{
		read_file >> tk >> uk >> delta_uk;
		N_filas++;
	}
	N_filas--;
	// Ahora que tenemos el número de filas podemos crear unos array que sabemos que tiene una longitud de N_filas
	//std::cout << "La longitud del array es: " << N_filas <<"\n";
	// Las dos siguientes lineas es pa pedirle al read_file que vuelva a empezar desde el puro principio
	read_file.clear();
	read_file.seekg(std::ios::beg);
	// ..................::::::.....:::::....:::...:::::::::::...::::.::::..:::..:::..:::.......::::....::..
	double t[N_filas], u[N_filas];
	double delta_u; // esta linea porque read_file se confunde si no le aclaramos que son 3 columnas 
	assert(read_file.is_open());
	for (int i=0; i<N_filas; i++)
	{
		read_file >> t[i] >> u[i] >> delta_u;
		assert(read_file.good());
	}
	//std::cout << "Los primeros elementos de t y u son: " << t[0] <<" y "<< u[0] << " \n";
	//std::cout << "Elementos intermedios de t y u son: " << t[200] <<" y "<< u[200] << " \n";
	//std::cout << "Los últimos elementos de t y u son: " << t[N_filas-1] <<" y "<< u[N_filas-1] << "\n";
	read_file.close();
	//double prueba2;
	double f_menor, f_mayor, periodo, entropia, frecuencia;
	//prueba2=hallar_entropia(tp_prueba, dimGrilla, N_filas, t, u);
	//std::cout << "La entropía para "<< tp_prueba<<" dias es " << prueba2 << " \n";
	f_menor=1/tp_mayor;
	f_mayor=1/tp_menor;
	int longitud_nombreAr=nombre_archivo.length();
	std::string nombre_nuevo="Entropia_";
	for (int j=0; j<longitud_nombreAr-4; j++){ nombre_nuevo=nombre_nuevo+nombre_archivo[j];}
	nombre_nuevo=nombre_nuevo+".csv";
	std::ofstream write_output(nombre_nuevo);
	assert(write_output.is_open());
	for (int k=0; k<=Finura; k++)
	{
		frecuencia=f_menor+((f_mayor-f_menor)/Finura)*k; //Bueno confío en que esto va a dar dado que hay dos double por aquí
		periodo=1/frecuencia;
		entropia=hallar_entropia(periodo,dimGrilla,N_filas,t,u);
		write_output << periodo << "," << entropia << " \n";
		write_output.precision(10);
		assert(write_output.good());
	}
	write_output.close();
	std::cout << "Archivo "<< nombre_nuevo <<" generado" << "\n";
	return 0;
}

double hallar_entropia(double tp_prueba, int dim_grilla[2], int N_datos, double t_dat[], double u_dat[])
{
	double phi[N_datos];
	double inf_u, sup_u, paso_phi, paso_u, entropia, entropia_norm;
	double *min_u, *max_u;
	int indice_i, indice_j;
	int cuenta_grilla[dim_grilla[0]][dim_grilla[1]];
	double grilla[dim_grilla[0]][dim_grilla[1]];
	for (int i=0; i<dim_grilla[0]; i++) { for (int j=0; j<dim_grilla[1]; j++) { cuenta_grilla[i][j]=0;}}
	// Aquí abajo vamos a hacer el equivalente de transformar_ts y clasificar los datos, de una, cada dato en cada una de las posiciones de la grilla
	// i es el índice que representa la cantidad de cuadros que tendrá el eje phi
	// j es el índice que represente la cantidad de cuadros que tendrá el eje u 
	// es decir dim_grilla debe colocarse así: {cuadros_phi, cuadros_u}
	min_u=std::min_element(u_dat,u_dat+N_datos); //Esto devuelve el pointer donde está el mínimo de u
	max_u=std::max_element(u_dat,u_dat+N_datos); //Esto devuelve el pointer donde está el máximo de u
	paso_phi=1.0/dim_grilla[0]; // Ojo al operar 2 int si no ponemos 1.0 sino solo 1, c++ redondea al int mas pequeño. 
	paso_u=(*max_u-*min_u)/dim_grilla[1];
	for (int l=0; l<N_datos; l++)
	{
		phi[l]=((t_dat[l]-t_dat[0])/tp_prueba)-floor((t_dat[l]-t_dat[0])/tp_prueba);
		for (int i=0; i<dim_grilla[0]; i++)
		{
			if (phi[l]>=(i*paso_phi) && phi[l]<((i+1)*paso_phi))
			{
				indice_i=i;
			}
		}
		for (int j=0; j<dim_grilla[1]; j++)
		{
			if (u_dat[l]>=(*min_u+j*paso_u) && u_dat[l]<(*min_u+(j+1)*paso_u))
			{
				indice_j=j;
			}
		}
		cuenta_grilla[indice_i][indice_j]++;
	}
	//QUE DOLOR DE PELOTAS FUE HALLAR ESA MATRIZ DE cuenta_grilla... PERO BUENO YA LO LOGRAMOS
	//...........................:::::::::::::::.....:::::::::....:::::::....:::::....::::....::::
	
	//Ahora que tenemos la grilla en números enteros, vamos a hallar la entropía correspondiente a esa grilla
	entropia=0;
	for (int i=0; i<dim_grilla[0]; i++)
	{
		for (int j=0; j<dim_grilla[1]; j++)
		{
			if (cuenta_grilla[i][j]==0){}
			else
			{
				entropia=entropia+(-((cuenta_grilla[i][j]+0.0)/N_datos)*log((cuenta_grilla[i][j]+0.0)/N_datos));
				//pero mirá que volviste a caer. Recuerda que si vas a operar dos int, tienes que agregar un +0.0 para que la respuesta te salga con decimales.
			}
		}
	}
	entropia_norm=(1.0/log(dim_grilla[0]*dim_grilla[1]))*entropia;
	return entropia_norm;
}
