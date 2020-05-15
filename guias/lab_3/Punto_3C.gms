***      Author: Daniel Serrano y Juan Pablo Cano                     ***
*************************************************************************
Scalar DIST distancia /0/;
Sets
  i   nodos / n1*n7 /
alias(j,i);

Parameter x(i) coord x
         /n1 20, n2 22, n3 9, n4 3, n5 21, n6 29, n7 14/
Parameter y(i) coord y
         /n1 6, n2 1, n3 2, n4 25, n5 10, n6 2, n7 12/

Parameter c(i,j) costos

loop((i,j),

         DIST = sqrt(power(x(i)-x(j),2) + power(y(i)-y(j),2))
         if( DIST <= 20 and DIST > 0,
         c(i,j) = DIST
else
c(i,j) = 99999);
);


Variables
  v(i,j)      Indicates if the link i-j is selected or not.
  z           Objective function  ;

Binary Variable v;

Equations
objectiveFunction        objective function
sourceNode(i)            source node
destinationNode(j)       destination node
intermediateNode         intermediate node
suma;

objectiveFunction                                  ..  z =e= sum((i,j), c(i,j) * v(i,j));

sourceNode(i)$(ord(i) = 4)                         ..  sum((j), v(i,j)) =e= 1;

destinationNode(j)$(ord(j) = 2)                    ..  sum((i), v(i,j)) =e= 1;

intermediateNode(i)$(ord(i) <> 4 and ord(i) ne 2)  ..  sum((j), v(i,j)) - sum((j), v(j,i)) =e= 0;

suma                                               ..   v("n7", "n5") + v("n7", "n3") =e= 1;

Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display c;
Display v.l;
Display z.l;

