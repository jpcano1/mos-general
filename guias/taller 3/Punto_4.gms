$ontext
$offtext

Sets
        c canciones /c1*c8/
        t tipo /blues, rock/
Table g(c, t) generos
        blues       rock
c1      1           0
c2      0           1
c3      1           0
c4      0           1
c5      1           0
c6      0           1
c7      0           0
c8      1           1;

Parameter d (c) /c1 4, c2 5, c3 3, c4 2, c5 4, c6 3, c7 5, c8 4/
Binary Variable ladoA(c);
Binary Variable ladoB(c);
Variable z;

Equations
funcObjetivo        Funcion Objetivo
resBluesA        Restriccion de blues ladoA
resBluesB        Restriccion de blues ladoB
resRockA        Restriccion de rock ladoA
resSoloenUnLado Restriccion para que una canción solo esté en un lado
resCondUno       Si la canción 1 está en el lado A la canción 5 no debe estar en el lado A.
resCondDos       Si la canción 2 y 4 están en el lado A entonces la canción 1 debe estar en el lado B.
resDuracionMenorA        Restriccion de duracion ladoA
resDuracionMenorB        Restriccion de duracion ladoB
resDuracionMayorA        Restriccion de duracion ladoA
resDuracionMayorB        Restriccion de duracion ladoB
;

funcObjetivo        ..      z =e= sum(c, ladoA(c)) + sum(c, ladoB(c));
resBluesA        ..      sum(c, g(c, "blues")*ladoA(c)) =e=  2;
resBluesB        ..      sum(c, g(c, "blues")*ladoB(c)) =e=  2;
resRockA        ..      sum(c, g(c, "rock")*ladoA(c)) =g=  3;
resSoloenUnLado(c)  ..   ladoA(c) + ladoB(c) =e= 1;
resCondUno       ..      ladoA("c1") =l= (1-ladoA("c5"));
resCondDos       ..      ladoA("c2")+ ladoB("c4") - 1 =l= ladoB("c1");
resDuracionMenorA     ..       sum(c, d(c)*ladoA(c)) =l= 16;
resDuracionMenorB     ..       sum(c, d(c)*ladoB(c)) =l= 16 ;
resDuracionMayorA     ..       sum(c, d(c)*ladoA(c)) =g= 14;
resDuracionMayorB     ..       sum(c, d(c)*ladoB(c)) =g= 14;
Model model1 /all/;

option mip=CPLEX;
Solve model1 using mip maximizing z;

Display ladoA.l;
Display ladoB.l;
Display z.l;
