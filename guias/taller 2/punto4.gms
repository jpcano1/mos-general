Sets
  i   losas / n1*n20 /
alias(i,j);

Variables
  v(i)      Indica si se levanta una losa o no.
  z           Objective function  ;

Binary Variable v;

Equations
objectiveFunction        objective function
least_one_1              Al menos una losa
least_one_2              Al menos una losa
least_one_3              Al menos una losa
least_one_4              Al menos una losa
least_one_5              Al menos una losa
least_one_6              Al menos una losa
least_one_7              Al menos una losa;

objectiveFunction        ..      z =e= sum((i), v(i));
least_one_1              ..      v("n1") + v("n5") =g= 1;
least_one_2              ..      v("n2") + v("n3") + v("n6") + v("n7") =g= 1;
least_one_3              ..      v("n5") + v("n9") =g= 1;
least_one_4              ..      v("n9") + v("n10") + v("n13") + v("n14") =g= 1;
least_one_5              ..      v("n13") + v("n17") =g= 1;
least_one_6              ..      v("n10") + v("n11") + v("n14") + v("n15") =g= 1;
least_one_7              ..      v("n8") + v("n12") + v("n16") + v("n20") + v("n19") =g= 1;

Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display v.l;
Display z.l;
