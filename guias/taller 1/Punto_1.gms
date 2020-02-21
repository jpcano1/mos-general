*************************************************************************
***      Ejercicio 1                                                  ***
***                                                                   ***
***      Autor: Daniel Serrano y Juan Pablo Cano                      ***
*************************************************************************
$ontext
Una compa��a posee cuatro m�quinas que deben completar cuatro trabajos.
Cada m�quina debe ser asignada para completar un �nico trabajo.
La compa��a desea minimizar el tiempo total requerido por las m�quinas para completar los cuatro trabajos.
$offtext
Sets
         m  maquinas /m1, m2, m3, m4/
         tr trabajos /tr1, tr2, tr3, tr4/

Table t(m,tr) tiempo
         tr1      tr2      tr3      tr4
m1       14       5        8        7
m2       2        12       6        5
m3       7        8        3        9
m4       2        4        6        10;




Variables
 x(m,tr) determina si se escoge la maquina m para el trabajo tr
 z       objective function;

Equations
funcObjetivo                 Funcion Objetivo
resFilas(m)                     Una maquina solo puede hacer un trabajo
resColumnas(tr)                  Un trabajo solo puede ser realizado por una m�quina;

funcObjetivo     ..      z =e= sum((m,tr), t(m,tr)*x(m,tr));
resFilas(m)         ..      sum((tr), x(m,tr)) =e= 1;
resColumnas(tr)  ..        sum((m), x(m,tr)) =e= 1;

Model model1 /all/ ;

option mip=CPLEX;
Solve model1 using mip minimizing z;

Display x.l;
Display z.l;

