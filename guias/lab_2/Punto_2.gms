*************************************************************************
***      Ejercicio 2                                                  ***
***                                                                   ***
***      Autor: Daniel Serrano y Juan Pablo Cano                      ***
*************************************************************************
$ontext
Suponga que un sistema de multiprocesamiento posee 3 procesadores origen
desde los cuales es necesario enviar procesos sin prioridad y con prioridad
a 2 procesadores destino.

En los procesadores origen 1, 2 y 3 se disponen de 60, 80 y 50 procesos
sin prioridad, y 80, 50 y 50 procesos con prioridad. En los procesadores
destino 1 y 2 se requieren respectivamente 100 y 90 procesos sin prioridad,
y 60 y 120 procesos con prioridad.



$offtext
Sets

         o  origen /o1, o2, o3/
         d destino /d1, d2/
* p1 no prioritario p2 prioritario
         p paquete /p1, p2/

Table c(o,d) costos
         d1       d2
o1       300      500
o2       200      300
o3       600      300;

Table  m(p, o) origen
         o1      o2      o3
p1       60      80      50
p2       80      50      50

Table n(p,d) destino
         d1      d2
p1       100     90
p2       60      120

Variables
x(o,d,p)
z;

Equations
funcObjetivo                      Funcion Objetivo
resFilas(o,p)                     Una procesador origen entrega maximo los paquetes que tiene
resColumnas(d,p)                  Un destino tiene que llegarle los paquetes que  solicita
resPositivo(o,d,p)                Valores positivos;

funcObjetivo     ..      z =e= sum((o,d,p), c(o,d)*x(o,d,p));

resFilas(o,p)         ..      sum((d), x(o,d,p)) =l= m(p,o);
resColumnas(d,p)  ..        sum((o), x(o,d,p)) =e= n(p,d);

resPositivo(o,d,p) .. x(o,d,p) =g= 0;

Model model1 /all/ ;

option mip=CPLEX;
Solve model1 using mip minimizing z;

Display x.l;
Display z.l;

