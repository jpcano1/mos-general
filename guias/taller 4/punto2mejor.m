  
syms x y;

y = x^5 - 8*x^3 + 10*x + 6;
d1_y = diff(y);
d2_y = diff(d1_y);
figure;
ezplot(y);
xlim([-3 3]);
ylim([-10 20]);
grid("on");

% Newton - Raphson
alpha = 1;
conv = 0.0001;
vals_x = [];
vals_y = [];

for i=-3:3
    x_i = i;
    eval_d1 = subs(d1_y, x, x_i);
    while abs(eval_d1) > conv
        eval_d1 = subs(d1_y, x, x_i);
        eval_d2 = subs(d2_y, x, x_i);
        x_j = x_i - alpha * (eval_d1 / eval_d2);
        x_i = x_j;
    end
    eval = subs(y, x, x_i);
    vals_x = [vals_x x_i];
    vals_y = [vals_y eval];
end

result_max = find(vals_y == max(vals_y));
result_min = find(vals_y == min(vals_y));
xmin = vals_x(result_min)
ym = subs(y, [x], xmin);
ymin = double(ym);
xmax = vals_x(result_max)
ym = subs(y, [x], xmax);
ymax = double(ym);
fprintf("Maximo global: %f\n", xmax);
fprintf("Minimo global: %f", xmin);
hold on;
plot(xmax,ymax,'o-','MarkerFaceColor','red','MarkerEdgeColor','red');
hold on;
plot(xmin,ymin,'o-','MarkerFaceColor','red','MarkerEdgeColor','red');