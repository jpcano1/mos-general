*************************************************************************
***      Ejercicio 2                                                  ***
***                                                                   ***
***      Autor: Daniel Serrano y Juan Pablo Cano                      ***
*************************************************************************
$ontext
Un sistema de multiprocesamiento consta de una cantidad m de procesadores de
los cuales se requieren transmitir cierto número de procesos hasta otra cantidad
 n de procesadores para luego ser almacenados en memoria. Suponga que el costo
por transmitir un proceso desde un procesador i hasta un procesador j es cij.
Adicionalmente, asuma que la oferta de procesos desde un procesador i es ai y
que la demanda de procesos desde un procesador j es bj. De acuerdo a la anterior
información, debe encontrarse la cantidad de procesos que deben ser transportados
 desde un procesador i hasta un procesador j de manera que el costo total de
transporte sea mínimo.
$offtext
Sets
         o  origen /o1, o2, o3/
         d destino /d1, d2, d3, d4/

Table t(o,d) costos
         d1       d2       d3       d4
o1       8        6        10       9
o2       9        12       13       7
o3       14       9        16       5;

Parameters

n(o) paquetes origen
         /o1 300, o2 500, o3 200/
m(d) paquetes destino
         /d1 200, d2 300, d3 100, d4 400/

Variables
x(o,d)
z;

Equations
funcObjetivo                 Funcion Objetivo
resFilas(o)                     Una maquina solo puede hacer un trabajo
resColumnas(d)                  Un trabajo solo puede ser realizado por una máquina
resPositivo(o,d)                 Valores positivos;

funcObjetivo     ..      z =e= sum((o,d), t(o,d)*x(o,d));
resFilas(o)         ..      sum((d), x(o,d)) =l= n(o);
resColumnas(d)  ..        sum((o), x(o,d)) =e= m(d);
resPositivo(o,d) .. x(o,d) =g= 0;

Model model1 /all/ ;

option mip=CPLEX;
Solve model1 using mip minimizing z;

Display x.l;
Display z.l;

