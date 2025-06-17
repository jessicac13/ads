P = [0.6 0.4 0.0;
     0.2 0.5 0.3;
     0.2 0.4 0.4];

% Transpor e subtrair a identidade para montar o sistema (P' - I)
A = [P' - eye(3); ones(1,3)];
b = [zeros(3,1); 1];

% Resolver o sistema linear
steady_state = A \ b;

% Exibir o vetor de estado estacionário
disp("Vetor de estado estacionário:");
disp(steady_state');

rates = [0, 10, 50];  % Mbps para cada estado
mean_rate = steady_state' * rates';  % produto escalar


disp("Vazão média:");
disp(mean_rate);

