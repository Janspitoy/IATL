% =========================================================================
% ЧАСТИНА 2: СТВОРЕННЯ НЕЧІТКОЇ СИСТЕМИ СУГЕНО (З ВИПРАВЛЕННЯМ)
% =========================================================================
clc;
clear;
close all;

disp('Частина 2: Створення системи Сугено...');

% --- Визначення змінних ---
x1_range = [-7 3];
x2_range = [-4.4 1.7];
[X1, X2] = meshgrid(linspace(x1_range(1), x1_range(2), 15), ...
                    linspace(x2_range(1), x2_range(2), 15));

% --- Створення об'єкта FIS типу 'sugeno' ---
fis_sugeno = sugfis('Name', 'SugenoSystem');

% --- Додавання вхідних змінних ---
% --- Вхідна змінна x1 ---
fis_sugeno = addInput(fis_sugeno, x1_range, 'Name', 'x1');
fis_sugeno = addMF(fis_sugeno, 'x1', 'trimf', [-7, -7, -3], 'Name', 'Low');
fis_sugeno = addMF(fis_sugeno, 'x1', 'trimf', [-6, -2, 2], 'Name', 'Mid');
fis_sugeno = addMF(fis_sugeno, 'x1', 'trimf', [-1, 3, 3], 'Name', 'High');

% --- Вхідна змінна x2 ---
fis_sugeno = addInput(fis_sugeno, x2_range, 'Name', 'x2');
fis_sugeno = addMF(fis_sugeno, 'x2', 'trimf', [-4.4, -4.4, -2.3], 'Name', 'Low');
fis_sugeno = addMF(fis_sugeno, 'x2', 'trimf', [-3.79, -1.35, 1.09], 'Name', 'Mid');
fis_sugeno = addMF(fis_sugeno, 'x2', 'trimf', [-0.5, 1.7, 1.7], 'Name', 'High');

% --- Додавання вихідної змінної ---
fis_sugeno = addOutput(fis_sugeno, [0 1], 'Name', 'y');

% --- Функції належності для виходу ---
fis_sugeno = addMF(fis_sugeno, 'y', 'constant', 50, 'Name', 'out_50');
fis_sugeno = addMF(fis_sugeno, 'y', 'linear', [4, -1, 0], 'Name', 'out_4x1_m_x2');
fis_sugeno = addMF(fis_sugeno, 'y', 'linear', [2, 2, 1], 'Name', 'out_2x1_p_2x2_p_1');
fis_sugeno = addMF(fis_sugeno, 'y', 'linear', [8, 2, 8], 'Name', 'out_8x1_p_2x2_p_8');
fis_sugeno = addMF(fis_sugeno, 'y', 'constant', 0, 'Name', 'out_0');

% --- База правил ---

ruleList = [
    2 0 5 1 1;   % Якщо x1 = Mid → y = out_0
    3 3 3 1 1;   % Якщо x1 = High і x2 = High → y = out_2x1_p_2x2_p_1
    3 1 2 1 1;   % Якщо x1 = High і x2 = Low → y = out_4x1_m_x2
    1 2 4 1 1;   % Якщо x1 = Low і x2 = Mid → y = out_8x1_p_2x2_p_8
    1 1 1 1 1;   % Якщо x1 = Low і x2 = Low → y = out_50
    1 3 1 1 1;   % Якщо x1 = Low і x2 = High → y = out_50
];

fis_sugeno = addRule(fis_sugeno, ruleList);

% --- Виведення інформації про систему ---
disp('Нечітка система Сугено створена:');
disp(fis_sugeno);

% --- Візуалізація структури ---
figure('Name', 'Структура системи Сугено', 'NumberTitle', 'off');
plotfis(fis_sugeno);

% --- Обчислення поверхні відгуку ---
Y_sugeno = evalfis(fis_sugeno, [X1(:), X2(:)]);
Y_sugeno = reshape(Y_sugeno, size(X1));

figure('Name', 'Поверхня відгуку системи Сугено', 'NumberTitle', 'off');
surf(X1, X2, Y_sugeno);
xlabel('x1');
ylabel('x2');
zlabel('y');
title('Поверхня відгуку системи Сугено');
colorbar;

disp('Систему Сугено створено та візуалізовано.');
