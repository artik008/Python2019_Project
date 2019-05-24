# Игра "Battle City"
Проект для курса PythonDevelopment2019

# Постановка задачи
Реализовать игру по аналогии с игрой "Танчики" с использованием tkinter.

# Описание
Цель игры: найти спрятанное сокровище и наехать на него танком.

У игрока есть возможность перемещаться по полю с помощью стрелок ВВЕРХ/ВНИЗ/ВЛЕВО/ВПРАВО, стрелять по кнопке ПРОБЕЛ

Поле содержит три типа блоков:
 - Трава - неразрушина, можно проходить насквозь
 - Кирпичи - можно разрушить пулей, непроходим
 - Сталь - нельзя разрушить, непроходим

Также на поле есть сокровище, которе может быть спратано под Травой или Кирпичами. Для завершения игры необходимо найти и наехать на него.

Время игры ограничено.

## Стартовый экран / экран конца игры

<p align="left">
  <img src=images/menu.png width="500" title="menu">
</p>

<p align="left">
  <img src=images/exit.png width="500" title="exit">
</p>

## Игровой экран

<p align="left">
  <img src=images/tanks.gif width="500" title="game">
</p>

# Запуск игры
`python3 tanki.py`

# Запуск автотестов
`python -m unittest test.py`

# Сторонняя документация
Link to [documentation](https://htmlpreview.github.io/?https://raw.githubusercontent.com/artik008/Python2019_Project/master/docs/_build/html/index.html)(documentation)
