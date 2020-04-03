nodosX = zeros(100);
nodosY = zeros(100);
arcosX1 = [];
arcosX2 = [];
arcosY1 = [];
arcosY2 = [];
origenX = 0;
origenY = 0;
destinoX = 0;
destinoY = 0;
matriz_costo = zeros(100,100);

for i=1:100
    x = rand()*100;
    y = rand()*100;
    nodosX(i) = x;
    nodosY(i) = y;
end

for i=1:100
    x1 = nodosX(i);
    y1 = nodosY(i);
    for j=i+1:100
        x2 = nodosX(j);
        y2 = nodosY(j);
        dist = distance(x1, x2, y1, y2);
        if dist <= 14 && dist > 0
            fprintf("Arco desde x1: %f", x1);
            fprintf(" y1: %f", y1);
            fprintf(" hasta x2: %f", x2);
            fprintf(" y2: %f\n", y2);
            arcosX1 = [arcosX1 x1];
            arcosX2 = [arcosX2 x2];
            arcosY1 = [arcosY1 y1];
            arcosY2 = [arcosY2 y2];
            matriz_costo(i,j)=dist;
        else matriz_costo(i,j)=inf;
        end
    end
end

arcosX = [arcosX1; arcosX2];
arcosY = [arcosY1; arcosY2];
arcosX = arcosX';
arcosY = arcosY';
hold on;
grid("on");
plot(nodosX, nodosY, 'o', 'LineWidth', 1, 'MarkerEdgeColor', 'k', ...
    'MarkerFaceColor', 'k', 'MarkerSize', 7);

for i=1:100
    text(nodosX(i)-0.1, nodosY(i), num2str(i), 'FontSize', 10);
end
fprintf("Cantidad de arcos: %f", length(arcosX));

for i=1:length(arcosX)
    plot([arcosX(i, 1) arcosX(i, 2)], [arcosY(i, 1) arcosY(i, 2)], '--k');
end

indiceOrigen=randperm(length(nodosX),1);
origenX = nodosX(indiceOrigen);
origenY = nodosY(indiceOrigen);
indiceDestino=randperm(length(nodosX),1);
if indiceOrigen == indiceDestino
    indiceDestino=randperm(length(nodosX),1);
end
destinoX = nodosX(indiceDestino);
destinoY = nodosY(indiceDestino);
hold on;
plot(origenX, origenY, 'o', 'LineWidth', 1, 'MarkerEdgeColor', 'b', ...
    'MarkerFaceColor', 'b', 'MarkerSize', 7);
hold on;
plot(destinoX, destinoY, 'o', 'LineWidth', 1, 'MarkerEdgeColor', 'b', ...
    'MarkerFaceColor', 'b', 'MarkerSize', 7);
hold on; 
%Convertimos el grafo dirigido en no-dirigido.             
for i=1:length(matriz_costo)
    for j=1:length(matriz_costo)
        matriz_costo(j,i)=matriz_costo(i,j);
        if i == j
            matriz_costo(j,i)= inf;
        end
    end
end 
[sp, spcost,P] = dijkstra(matriz_costo, indiceOrigen, indiceDestino)
for i = 1:length(sp)
    x = nodosX(i);
    y = nodosY(i);
    plot(x, y, 'o', 'LineWidth', 1, 'MarkerEdgeColor', 'r', ...
    'MarkerFaceColor', 'r', 'MarkerSize', 7);
    hold on;
end
disp(matriz_costo)
