*************************************************************************
***      Ejercicio 5                                                 ***
***                                                                   ***
***      Autor: Daniel Serrano y Juan Pablo Cano                      ***
*************************************************************************
$ontext
Los trabajadores deben desempeñar sus cargos 5 días consecutivos y
descansar 2 días. Por ejemplo, un trabajador que labora de martes a
sábado, descansaría el domingo y el lunes.

$offtext
Sets

t  trabaja /Lunes, Martes , Miercoles, Jueves, Viernes, Sabado, Domingo/
alias(c, t);
*comienza

Parameter r(t) /Lunes 17 , Martes  13, Miercoles  15, Jueves  19, Viernes 14, Sabado  16, Domingo  11/;

Table d(c,t) dias de trabajo
            Lunes   Martes  Miercoles       Jueves  Viernes Sabado  Domingo
Lunes       1       1       1               1       1       0       0
Martes      0       1       1               1       1       1       0
Miercoles   0       0       1               1       1       1       1
Jueves      1       0       0               1       1       1       1
Viernes     1       1       0               0       1       1       1
Sabado      1       1       1               0       0       1       1
Domingo     1       1       1               1       0       0       1

Positive Variable x(c)
Variable z;

Equations
funcObjetivo                      Funcion Objetivo
resDia(t);

funcObjetivo                      ..      z =e= sum(t, x(t));
resDia(t)                         ..      sum((c), d(c,t)* x(c)) =g= r(t);

Model model1 /all/ ;

option mip=CPLEX;
Solve model1 using mip minimizing z;
Display x.l;
Display z.l;


