$ontext
$offtext

Sets
        c canciones /c1*c8/

Table g(c, g) generos
        blues       rock_n_roll
c1      1           0
c2      0           1
c3      1           0
c4      0           1
c5      1           0
c6      0           1
c7      0           0
c8      1           1;

Table d(c, t) duraciones
        duracion
c1      4
c2      5
c3      3
c4      2
c5      4
c6      3
c7      5
c8      4

Binary Variable ladoA(c)
Binary Variable laboB(c)
Variable z;

Equations
funcObjetivo        Funcion Objetivo;

funcObjetivo        ..      z =e= sum((c), d(c, "duracion")*ladoA(c)) + sum(c, d(c, "duracion")*ladoB(c));

