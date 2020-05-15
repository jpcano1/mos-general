function [sp, spcost, P] = dijkstra_v2(matriz_costo, s, d)
% This is an implementation of the dijkstra's algorithm, which finds the 
% minimal cost path between two nodes. It's supoussed to solve the problem on 
% possitive weighted instances.

% the inputs of the algorithm are:
%farthestNode: the farthest node to reach for each node after performing
% the routing;
% n: the number of nodes in the network;
% s: source node index;
% d: destination node index;

%For information about this algorithm visit:
%http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

%This implementatios is inspired by the Xiaodong Wang's implememtation of
%the dijkstra's algorithm, available at
%http://www.mathworks.com/matlabcentral/fileexchange
%file ID 5550

%Author: Jorge Ignacio Barrera Alviar. April/2007


n=size(matriz_costo,1);
S(1:n) = 0;     %s, vector, set of visited vectors
dist(1:n) = inf;   % it stores the shortest distance between the source node and any other node;
prev(1:n) = n+1;    % Previous node, informs about the best previous node known to reach each  network node 

dist(s) = 0;

P=1;
flag1=1;
while flag1==1
    while sum(S)~=n
        candidate=[];
        for i=1:n
            if S(i)==0
                candidate=[candidate dist(i)];
            else
                candidate=[candidate inf];
            end
        end
        
        %ger: detectar que no hay path
        contInf=0;
        for i=1:length(candidate)
            if candidate(i)==inf
                contInf=contInf+1;
            end
        end
        
        if contInf==length(matriz_costo) & S(d)==0
            P=0;
            break;
        end
        if contInf==length(matriz_costo) & S(d)==1             
            P=1;
            break;
        end
        
        
        [u_index u]=min(candidate);
        S(u)=1;
        for i=1:n
            if(dist(u)+matriz_costo(u,i))<dist(i)
                dist(i)=dist(u)+matriz_costo(u,i);
                prev(i)=u;
            end
        end
    end
    
    if P==0
        sp=0;
        spcost=0;
        break;
    end
    
    
    sp = [d];
    
    while sp(1) ~= s
        if prev(sp(1))<=n
            sp=[prev(sp(1)) sp];
        else
            error;
        end
    end;
    spcost = dist(d);
    flag1=0;
end