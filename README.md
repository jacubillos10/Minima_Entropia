# Minima Entropia
# Minimum Entropy
Este repositorio tiene el código en C++ y en python del algoritmo de mínima entropía para hallar el periodo de estrellas variables, método introducido en el trabajo de Cincotta [1]

This Repository has the C++ and python codes of minimum entropy method used to find variable stars periods. This method was introduced in Cincotta's work [1].

A=número de columas de la grilla/number of columns of the grid
B=múmero de filas de la grilla/number of rows of the grid
N=número de periodos a buscar/number of periods to search  
N_als=Número para filtar "aliases" usualmente =4/Number to filter aliases usually =4  
Usage/Modo de Uso: ./MinimaEntropia file.dat <periodo inicial/start period> <periodo final/end period> <A> <B> <N> <N_als> 

Example/Ejemplo:
  ./MinimaEntropia OGLE-LMC-RRLYR-02889.dat 0.15 1.2 5 6 100000 4

### Referencias
[1] P. M. Cincotta, M. Mendez, and J. A. Nuñez, “Astronomical Time Series Analysis. I. A Search for
Periodicity Using Information Entropy,” Astrophysical Journal., vol. 449, p. 231, Aug. 1995.
