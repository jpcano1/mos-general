syms x y;

y = 3*x^3 - 10*x^2 - 56*x + 50;
d1_y = diff(y);
d2_y = diff(d1_y);
figure;
ezplot(y);
grid("on");

% Newton - Raphson

x_i = -8; % Valor inicial
alpha = 1;
conv = 0.0001;

eval_d1 = subs(d1_y, x, x_i);
hold on;
while abs(eval_d1) > conv
    eval_d1 = subs(d1_y, x, x_i);
    eval_d2 = subs(d2_y, x, x_i);
    x_j = x_i - alpha * (eval_d1 / eval_d2);
    x_i = x_j;
    eval = subs(y, x, x_i);
    plot(x_i, eval, 'or');
end

eval_1 = subs(y, x, x_i);
eval_2 = subs(y, x, x_i-1);
if eval_1 > eval_2
    fprintf("Maximo: %f", x_i);
else
    fprintf("Minimo: %f", x_i);
end

% Newton - Raphson con alpha = 0.6
x_i = -8;
alpha = 0.6;
conv = 0.001;
eval_d1 = subs(d1_y, x, x_i);
while abs(eval_d1) > conv
    eval_d1 = subs(d1_y, x, x_i);
    eval_d2 = subs(d2_y, x, x_i);
    x_j = x_i - alpha * (eval_d1 / eval_d2);
    x_i = x_j;
    eval = subs(y, x, x_i);
    plot(x_i, eval, 'og');
end