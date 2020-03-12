*************************************************************************
***      Ejercicio 2                                                  ***
***                                                                   ***
***      Autor: Daniel Serrano y Juan Pablo Cano                      ***
*************************************************************************
set j /n1*n20/
    i /p1*p7/
table t(i,j) conexiones entre baldosas
         n1      n2      n3      n4      n5      n6      n7      n8      n9      n10     n11     n12     n13     n14     n15     n16     n17     n18     n19     n20
p1       1       0       0       0       1       0       0       0       0       0       0       0       0       0       0       0       0       0       0       0
p2       0       1       1       0       0       1       1       0       0       0       0       0       0       0       0       0       0       0       0       0
p3       0       0       0       0       1       0       0       0       1       0       0       0       0       0       0       0       0       0       0       0
p4       0       0       0       0       0       0       0       0       1       1       0       0       1       1       0       0       0       0       0       0
p5       0       0       0       0       0       0       0       0       0       1       1       0       0       1       1       0       0       0       0       0
p6       0       0       0       0       0       0       0       1       0       0       0       1       0       0       0       1       0       0       1       1
p7       0       0       0       0       0       0       0       0       0       0       0       0       1       0       0       0       1       0       0       0
;

Binary variable x(j)
Variable z;

Equations
funcObjetivo                 Funcion Objetivo
materialTubos                Restringe el numero de baldosas levantadas
;

funcObjetivo .. z=e= sum((j),x(j));
materialTubos(i) ..  sum((j),x(j)*t(i,j))=g=1;

Model model1 /all/ ;

option mip=CPLEX;
Solve model1 using mip minimizing z;

Display x.l;