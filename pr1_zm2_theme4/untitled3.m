% =========================================================================
% ЧАСТИНА 3: СТВОРЕННЯ НЕЧІТКОЇ СИСТЕМИ МАМДАНІ (НОВИЙ СИНТАКСИС)
% =========================================================================
disp('Частина 3: Створення системи Мамдані...');

% --- Створення нового об'єкта FIS типу 'mamdani' ---
fis_mamdani = mamfis('Name', 'MamdaniSystem');

% --- Додавання вхідних змінних ---
% (використовуємо ті самі діапазони, що й у системі Сугено)
fis_mamdani = addInput(fis_mamdani, x1_range, 'Name', 'x1');
fis_mamdani = addMF(fis_mamdani, 'x1', 'trimf', [-7, -7, -3], 'Name', 'Низький');
fis_mamdani = addMF(fis_mamdani, 'x1', 'trimf', [-6, -2, 2], 'Name', 'Середній');
fis_mamdani = addMF(fis_mamdani, 'x1', 'trimf', [-1, 3, 3], 'Name', 'Високий');

fis_mamdani = addInput(fis_mamdani, x2_range, 'Name', 'x2');
fis_mamdani = addMF(fis_mamdani, 'x2', 'trimf', [-4.4, -4.4, -2.3], 'Name', 'Низький');
fis_mamdani = addMF(fis_mamdani, 'x2', 'trimf', [-3.79, -1.35, 1.09], 'Name', 'Середній');
fis_mamdani = addMF(fis_mamdani, 'x2', 'trimf', [-0.5, 1.7, 1.7], 'Name', 'Високий');

% --- Додавання вихідної змінної ---
fis_mamdani = addOutput(fis_mamdani, [-50 50], 'Name', 'y');
fis_mamdani = addMF(fis_mamdani, 'y', 'trimf', [-80 -50 -20], 'Name', 'Негативний');
fis_mamdani = addMF(fis_mamdani, 'y', 'trimf', [-30 0 30], 'Name', 'Нуль');
fis_mamdani = addMF(fis_mamdani, 'y', 'trimf', [20 50 80], 'Name', 'Позитивний');

% --- База правил (числовий формат)
% Формат: [x1_index, x2_index, y_index, weight, operator]
% operator = 1 (AND), weight = 1 (звичайна вага)
ruleList_mamdani = [
    1 1 3 1 1;  % Якщо x1=Низький і x2=Низький, то y=Позитивний
    1 3 3 1 1;  % Якщо x1=Низький і x2=Високий, то y=Позитивний
    2 0 2 1 1;  % Якщо x1=Середній, то y=Нуль
    3 1 1 1 1;  % Якщо x1=Високий і x2=Низький, то y=Негативний
    3 3 1 1 1;  % Якщо x1=Високий і x2=Високий, то y=Негативний
];
fis_mamdani = addRule(fis_mamdani, ruleList_mamdani);

% --- Виведення інформації про систему ---
disp('Нечітка система Мамдані створена:');
disp(fis_mamdani);

% --- Візуалізація структури системи ---
figure('Name', 'Структура системи Мамдані', 'NumberTitle', 'off');
plotfis(fis_mamdani);

% --- Обчислення поверхні відгуку ---
Y_mamdani = evalfis(fis_mamdani, [X1(:), X2(:)]);
Y_mamdani = reshape(Y_mamdani, size(X1));

% --- Побудова поверхні ---
figure('Name', 'Поверхня відгуку Мамдані', 'NumberTitle', 'off');
surf(X1, X2, Y_mamdani);
xlabel('x1');
ylabel('x2');
zlabel('y');
title('Поверхня відгуку системи Мамдані');
colorbar;

disp('Систему Мамдані створено та візуалізовано.');
disp('Виконання скрипту завершено.');
