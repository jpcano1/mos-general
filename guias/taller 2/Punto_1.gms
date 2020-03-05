*************************************************************************
***      Punto 1                                       ***
***                                                                   ***
***      Author: Daniel Serrano y Juan Pablo Cano                     ***
*************************************************************************
Sets
  i   nodos / n1*n6 /
alias(j,i);

Table t(i,j) tiempos
         n1      n2      n3      n4      n5      n6
n1       0       10      20      30      30      20
n2       10      0       25      35      20      10
n3       20      25      0       15      30      20
n4       30      35      15      0       15      25
n5       30      20      30      15      0       14
n6       20      10      20      25      14      0;

Parameter c(i,j) costos

loop((i,j),
         if( t(i,j) <= 15,
         c(i,j) = 1
else
c(i,j) = 0);
);


Variables
  v(i)      Indica si se construye una estación o no.
  z           Objective function  ;

Binary Variable v;

Equations
objectiveFunction        objective function
adyacente(i)            adyacentes;


objectiveFunction        ..  z =e= sum((i), v(i));

adyacente(i)             .. sum((j), v(j) * c(i,j)) =g= 1;



Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display c;
Display v.l;
Display z.l;

