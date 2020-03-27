syms x y z;

z = (1 - x)^2 + 100 * (y - x^2)^2;
grad_z = gradient(z);
hess_z = hessian(z);

ezsurf(z);
grid("on");