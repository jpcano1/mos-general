*************************************************************************
***      Ejercicio 5                                                 ***
***                                                                   ***
***      Autor: Daniel Serrano y Juan Pablo Cano                      ***
*************************************************************************
$ontext
El entrenador de un equipo de básquetbol requiere escoger el equipo titular
 (5 de 7 jugadores) que jugará el siguiente partido. El equipo total consta
de siete jugadores que están clasificados (con una escala de 1=deficiente a
3= excelente) de acuerdo  a sus habilidades técnicas tales como: control del
balón, disparo, rebote y habilidades defensivas.

El equipo titular tiene que satisfacer los siguientes requerimientos:

1.        El equipo titular debe tener 5 jugadores.
2.        Por lo menos cuatro miembros deben ser capaces de jugar en la
defensiva, por lo menos dos jugadores deben jugar como atacantes y al menos
uno debe jugar en el centro.
3.        El nivel promedio de control del balón del equipo titular tiene que
ser por lo menos de dos.
4.        El nivel promedio de disparo del equipo titular tiene que ser por
lo menos de dos.
5.        El nivel promedio de rebotes del equipo titular tiene que ser por
lo menos de dos.
6.        En el equipo titular debe estar el jugador dos o el jugador tres,
es decir, solo uno de los dos debe ser titular.


$offtext
Sets

         j  jugadores /j1, j2, j3, j4, j5, j6, j7/
         r roles /ataque, centro, defensa/
         h habilidad /control, disparo, rebote, defensa/

Table p(j,r) posiciones
         ataque       centro      defensa
j1       1            0           0
j2       0            1           0
j3       1            0           1
j4       0            1           1
j5       1            0           1
j6       0            1           1
j7       1            0           1;

Table  m(j, h) habilidades
         control disparo rebote  defensa
j1       3       3       1       3
j2       2       1       3       2
j3       2       3       2       2
j4       1       3       3       1
j5       3       3       3       3
j6       3       1       2       3
j7       3       2       2       1
Binary Variable x(j)
Variable z;

Equations
funcObjetivo                      Funcion Objetivo
resNumeroJugadores                Se deben escoger 5 jugadores
resDefensa                        Por lo menos cuatro defensas
resAtaque                         Por lo menos dos jugadores atacantes
resCentro                         Al menos uno debe jugar en el centro
resPromedio(h)
resTitular                        2 o 3 deben ser titulares;
;
funcObjetivo                      ..      z =e= sum((j), m(j,"defensa")*x(j));
resNumeroJugadores                .. sum(j,x(j)) =e= 5;
resDefensa                     .. sum(j, p(j,"defensa") * x(j)) =g= 4;
resAtaque                      .. sum(j, p(j,"ataque") * x(j)) =g= 2;
resCentro                      .. sum(j, p(j,"centro") * x(j)) =g= 1;
resPromedio(h)                    .. sum((j), m(j,h)*x(j))/5 =g= 2;
resTitular                        .. x("j2")+ x("j3") =e= 1;
Model model1 /all/ ;

option mip=CPLEX;
Solve model1 using mip maximizing z;

Display x.l;
Display z.l;

