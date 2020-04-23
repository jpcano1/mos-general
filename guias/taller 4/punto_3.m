clc, clear, close all
syms x y z;
z = (1 - x)^2 + 100 * (y - x^2)^2;
figure
ezsurf(x,y,z);
grid("on");
hold on;

xx = [];
yy = [];
zz = [];
xi = 5;
yi = 5;
xy = [xi; yi];
zi = double(subs(z, [x; y], xy));
alfa = 0.9;
convergencia = 0.001;

%GRADIENTE
grad_z = gradient(z);
grad_z_eval = subs(grad_z, [x; y], xy);
grad_z_eval_double = double(grad_z_eval);

%HESSIANO
hess_z = hessian(z);
hess_z_eval = subs(hess_z, [x; y], xy);
hess_z_eval_double = double(hess_z_eval);

%LOOP
while norm(abs(grad_z_eval_double)) > convergencia
    xyn = xy - alfa *(inv(hess_z_eval_double)*grad_z_eval_double);
    xy = xyn;
    grad_z_eval = subs(grad_z, [x; y], xy);
    grad_z_eval_double = double(grad_z_eval);
    hess_z_eval = subs(hess_z, [x; y], xy);
    hess_z_eval_double = double(hess_z_eval);
    zi = double(subs(z, [x; y], xy));
    xx = [xx, xy(1)];
    yy = [yy, xy(2)];
    zz = [zz, zi];
end

plot3(xx,yy,zz, 'o', 'MarkerFaceColor', 'c');
